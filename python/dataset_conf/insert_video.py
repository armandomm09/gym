import cv2
import os


def insert_video_in_raw_dataset(video_path, raw_dataset_path, every_how_many_frames=30):


    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error al abrir el video.")
        exit()

    frame_count = 0
    saved_frame_count = 0

    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        if frame_count % every_how_many_frames == 0:
            frame_filename = os.path.join(raw_dataset_path, f"frame_{saved_frame_count:04d}.jpg")
            
            cv2.imwrite(frame_filename, frame)
            
            # print(f"Guardado {frame_filename}")
            saved_frame_count += 1
        
        frame_count += 1

    cap.release()

    print(f"{saved_frame_count} images have been added to the dataset '{raw_dataset_path}'.")
