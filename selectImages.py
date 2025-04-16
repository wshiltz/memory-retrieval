import random
import os
import shutil

# Randomly selects x images from one directory to move to another directory
def main():
    count = 2000
    datasetDir = "INSERT INITIAL DATASET DIRECTORY HERE"
    subsetDir = "INSERT DESTINATION DIRECTORY HERE"
    
    dataset = os.listdir(datasetDir)
    subset = random.sample(dataset, count)

    for image in subset:
        shutil.copy(f"{datasetDir}/{image}", f"{subsetDir}/{image}")
        print(f"Successfully copied {image}")

    print(f"Successfully copied {count} images")

if __name__ == "__main__":
    main()