import os
from PIL import Image
import numpy as np
import torch
from image2vector.img_to_vec import Img2Vec
import sys
import pysolr
import random
import json
import requests

images_path = "/Users/janeshmishra/Downloads/leaves/"
## Solr configuration.
SOLR_ADDRESS = 'http://localhost:8983/solr/image/select?fl=id,image_path,score'
solr = pysolr.Solr(SOLR_ADDRESS, always_commit=True)


def generate_random_image():
    random_index = random.randint(0, 500)
    header = {'Content-Type': 'application/json'}
    q = "id:" + str(random_index)
    query = {"query": q}
    query_response = json.loads(requests.post(url=SOLR_ADDRESS,
                                                data=json.dumps(query),
                                                headers=header).content)

    if query_response["response"]["numFound"] == 0:
        return "No image exists"

    for data in query_response["response"]["docs"]:
        return data["image_path"]

    print("Jai Mata Di")


def find_similar_image(image_location):
    img2vec = Img2Vec(model='densenet')
    img = Image.open(image_location)
    vector = img2vec.get_vec(img).tolist()
    similar_image = []

    if vector is not None:
        header = {'Content-Type': 'application/json'}
        knn = "{!knn f=vector topK=5}" + str(vector)
        query = {"query": knn}
        query_response = json.loads(requests.post(url=SOLR_ADDRESS,
                                                    data=json.dumps(query),
                                                    headers=header).content)

        if query_response["response"]["numFound"] == 0:
            return similar_image

        data = query_response["response"]["docs"]
        for index in range(len(data)):
            similar_image.append(data[index]["image_path"])

    return similar_image

    print("Jai Mata Di")


image = generate_random_image()
find_similar_image(image)
