import random
import requests
import os

def downloadRandom(ids, count, directory):
    toDownload = random.sample(ids, count)
    for id in toDownload:
        image = requests.get().content
        filename = os.path.join(directory, f"pipa{id}.jpg")
        with open(filename, "wb") as imageFile:
            imageFile.write(image)

# Uses the following github repo to get example photos from flickr
# https://github.com/coallaoh/PIPA_dataset
def main():
    ids = []
    with open("./all_data.txt", "r") as file:
        for line in file:
            ids.append(line[:-1].split(" ")[1])

    print(ids)
    downloadRandom(ids, 800, "./examplePhotos/pipa")

if __name__ == "__main__":
    main()