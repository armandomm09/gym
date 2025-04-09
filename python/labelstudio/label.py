import os
import json
import shutil
import subprocess
import zipfile
import label_studio.server
from label_studio_sdk import Client
import label_studio

class Labeler:
    def __init__(self, API_KEY, URL, proj_title):
        """
        Initializes the Labeler instance by setting environment variables needed for local file access
        and configuring the Label Studio client, project title, and data directories.
        """
        self.api_key = API_KEY
        self.url = URL
        self.title = proj_title
        
        os.environ['LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED'] = 'true'
        os.environ['LOCAL_FILES_SERVING_ENABLED'] = 'true'
        os.environ['LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT'] = '/Users/armando/Progra/python/ai/gym/python/complete'
        os.environ['LOCAL_FILES_DOCUMENT_ROOT'] = '/Users/armando/Progra/python/ai/gym/python/complete'
        os.environ['CONVERTER_DOWNLOAD_RESOURCES'] = '1'

        self.ls = Client(url=self.url, api_key=self.api_key)

        self.train_dir = '/Users/armando/Progra/python/ai/gym/python/complete/train'
        self.output_file = '/Users/armando/Progra/python/ai/gym/python/complete/annotations.json'

    def _find_project(self):
        """
        Checks if a project with the specified title already exists in Label Studio.
        Returns the project instance if found, otherwise returns None.
        """
        projects = self.ls.list_projects()
        for proj in projects:
            if proj.title == self.title:
                return self.ls.get_project(proj.id)
        return None

    def open_labeler(self):
        """
        Converts YOLO annotations to Label Studio format using label-studio-converter,
        creates a new project or reuses an existing one, sets the label config, 
        and imports annotation tasks and image storage.
        """
        converter_command = [
            'label-studio-converter', 'import', 'yolo',
            '-i', self.train_dir,
            '-o', self.output_file,
            '--image-root-url', '/data/local-files/?d=train/images'
        ]
        subprocess.run(converter_command, check=True)

        label_config = None
        try:
            with open(self.output_file.replace("json", "label_config.xml"), 'r') as f:
                converter_data = f.read()
                print("CONVERTER DATA:\n\n", str(converter_data))
                label_config = str(converter_data)
        except Exception as e:
            print(f"Error reading annotation config file: {e}")

        if not label_config:
            label_config = '''
            <View>
                <Image name="image" value="$image"/>
                <RectangleLabels name="label" toName="image">
                    <Label value="Objeto"/>
                </RectangleLabels>
            </View>
            '''

        project = self._find_project()
        if project:
            print("Project found. Reusing existing project.")
            project.delete_all_tasks()  
        else:
            print("No existing project found. Creating a new one using provided label_config.")
            project = self.ls.start_project(
                title=self.title,
                label_config=label_config,
                expert_instruction='Instrucciones para los anotadores.'
            )

        try:
            with open(self.output_file, 'r') as f:
                tasks = json.load(f)
            project.import_tasks(tasks)
        except Exception as e:
            print(f"Error importing tasks: {e}")

        project.connect_local_import_storage(
            "/Users/armando/Progra/python/ai/gym/python/complete/train/images",
        )

    def export_yolo(self):
        """
        Exports annotations from the project in YOLO format and extracts the data.
        Also copies the original images into the export directory to maintain compatibility.
        """
        project = self._find_project()
        if project is None:
            raise Exception("Project not found for export.")

        path_to_zip_file = "/Users/armando/Progra/python/ai/gym/python/labelstudio/images.zip"
        extract_dir = "/Users/armando/Progra/python/ai/gym/python/labelstudio/images"

        project.export_tasks("YOLO", download_all_tasks=True,
                             download_resources=True, export_location=path_to_zip_file)

        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        main_images_dir = os.path.join(self.train_dir, "images")
        if os.path.exists(main_images_dir):
            imgs = os.listdir(main_images_dir)
            for img in imgs:
                src = os.path.join(main_images_dir, img)
                dst = os.path.join(extract_dir, "images", img)
                shutil.copy(src, dst)
        else:
            print(f"Image directory not found: {main_images_dir}")
