import os
import random

def pretrain_test(directory: str, number_of_test: int):
    test_images = random.sample(os.listdir(directory), number_of_test)
    print(test_images)
    
pretrain_test("test_imgs/dataset", 3)

    
    