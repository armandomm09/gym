import os
from autodistill_grounding_dino import GroundingDINO
from autodistill.detection import CaptionOntology
import cv2
import supervision as sv
import random
import matplotlib.pyplot as plt  
from utils import printProgressBar
plt.ion()  

class Coach():
    def __init__(self, ontology):
        """
        Initializes the Coach with a given ontology. Sets up the base model for automatic labeling
        using GroundingDINO and prepares a box annotator for visualization.
        """
        self.ontology_dict = ontology
        self.base_model = GroundingDINO(ontology=CaptionOntology(ontology))
        self.annotator = sv.BoxAnnotator()
        
    def autolabel_test(self, directory: str, number_of_test_images: int, out_directory: str = None, save: bool = False, show: bool = False):
        """
        Randomly selects a specified number of test images from a folder, runs detection on each,
        optionally saves and/or displays the annotated results. Progress is shown with a progress bar.
        """
        test_images = random.sample(os.listdir(directory), number_of_test_images)
        annotated_images = []
        total = len(test_images)
        printProgressBar(0, total, prefix="Progress", suffix="Completed", length=50)
        for i, image_name in enumerate(test_images, start=1):
            print(f"Processing image: {image_name}")
            image = cv2.imread(os.path.join(directory, image_name))
            predictions = self.base_model.predict(image)
            print("Predictions:", predictions)
            annotated_image = self.annotator.annotate(scene=image, detections=predictions)
            annotated_images.append(annotated_image)
            if out_directory is not None or not save:
                cv2.imwrite(os.path.join(out_directory, image_name), annotated_image)
            printProgressBar(i, total, prefix="Progress", suffix="Completed", length=50)
        if show:
            for annotated_image in annotated_images:
                sv.plot_image(annotated_image)
                plt.pause(0.001)
        plt.ioff()
        plt.show()
    
    def autolabel(self, input_folder, output_folder: str | None = None):
        """
        Performs automated labeling on all images within the input folder using the base model,
        and generates a `classes.txt` file with all the labels based on the ontology provided.
        """
        self.base_model.label(input_folder=input_folder, output_folder=output_folder)
        
        class_names = list(self.ontology_dict.values())  
        classes_txt_path = os.path.join(output_folder, 'train/classes.txt')

        with open(classes_txt_path, 'w') as f:
            for class_name in class_names:
                f.write(f"{class_name}\n")
