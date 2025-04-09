from dataset_conf import insert_video_in_raw_dataset
import sys
import json 
from labelstudio import Labeler
import logging

logger = logging.getLogger('faker')
logger.setLevel(logging.NOTSET)

if len(sys.argv) > 1:
    if sys.argv[1] == "pretrain_test":
        from coach import Coach
        coach = Coach({"a teal ball": "ball"})
        print("Making pretrain test")
        _, _, dataset_path, img_num, out_path, save, show = sys.argv
        coach.autolabel_test(dataset_path, int(img_num), out_path, save == "True", show == "True")
    elif sys.argv[1] == "insert_video_in_raw":
        _, _, video_path, frames, dataset_path = sys.argv
        print("Inserting video", video_path)
        if video_path[-3:] == "avi" or video_path[-3:] == "mp4":
            insert_video_in_raw_dataset(video_path, dataset_path, int(frames))
    elif sys.argv[1] == "autolabel":
        from coach import Coach
        print(sys.argv)
        _, _, ontology, input_path, output_path = sys.argv
        ontology = json.loads(ontology)
        coach = Coach(ontology)
        coach.autolabel(input_path, output_path)
        print(ontology)
    elif sys.argv[1] == "label":
        print(sys.argv)
        labeler = Labeler(sys.argv[2], sys.argv[3], sys.argv[4])

        labeler.open_labeler()
        
# print(sys.argv)