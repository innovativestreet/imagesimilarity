import os
from PIL import Image
import numpy as np
import torch
from image2vector.img_to_vec import Img2Vec
import sys
import pysolr
import pandas as pd
import requests

## Solr configuration.
SOLR_ADDRESS = 'http://localhost:8983/solr/image_cosine'
solr = pysolr.Solr(SOLR_ADDRESS, always_commit=True)

df = pd.read_csv('/Users/janeshmishra/Downloads/images.csv')

with torch.no_grad():
    for index, row in df.iterrows():
        try:
            image_location = row['file_path']
            query_response = row['reply_msg']
            img2vec = Img2Vec(model='densenet')
            img = Image.open(requests.get(image_location, stream=True).raw)
            vec = img2vec.get_vec(img)
            vector = vec.tolist()
            doc = {
                "id": str(index + 1),
                "image_path": image_location,
                "vector": vector,
                "query_response": query_response
            }
            solr.add(doc)
            print(f"{index + 1} Image Path: {image_location} Done")
        except Exception as e:
            print(f"{index + 1} Image Path: {image_location} Error: {str(e)}")
            continue

