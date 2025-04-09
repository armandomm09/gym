import os
from autodistill_grounding_dino import GroundingDINO
from autodistill.detection import CaptionOntology
import cv2
import supervision as sv

model = GroundingDINO(ontology=CaptionOntology({"a teal ball": "ball"}))
model.label(input_folder="raw", output_folder="complete")