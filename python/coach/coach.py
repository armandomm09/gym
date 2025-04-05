import os
from autodistill_grounding_dino import GroundingDINO
from autodistill.detection import CaptionOntology
import cv2
import supervision as sv
import random
import os
import matplotlib.pyplot as plt # type: ignore
import sys
from utils import printProgressBar
plt.ion()  # Activa el modo interactivo

class Coach():
    def __init__(self, ontologym):
        self.base_model = GroundingDINO(ontology=CaptionOntology(ontologym))
        self.annotator = sv.BoxAnnotator()
        

    def autolabel_test(self, directory: str, number_of_test_images: int, out_directory: str = None, save: bool = False, show: bool = False):
        """
        :param directory: Directory containing the images.
        :param number_of_test_images: Number of test images to process.
        :param out_directory: Directory where annotated images will be saved (if applicable).
        :param save: Boolean flag to indicate whether to save images.
        :param show: Boolean flag to indicate whether to display images.
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
        if output_folder is None:
            self.base_model.label(input_folder=input_folder)
        else:
            self.base_model.label(input_folder=input_folder, output_folder=output_folder)
            

    
        
