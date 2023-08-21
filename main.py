import os
from PIL import Image
import numpy as np
import torch
from image2vector.img_to_vec import Img2Vec
import sys
import pysolr

## Solr configuration.
SOLR_ADDRESS = 'http://localhost:8983/solr/image_cosine'
solr = pysolr.Solr(SOLR_ADDRESS, always_commit=True)

images = os.listdir("/Users/janeshmishra/Downloads/dog-cat")
images_path = "/Users/janeshmishra/Downloads/dog-cat/"

# all_names = []
# all_vecs = None

with torch.no_grad():
    for i, file in enumerate(images):
        try:
            image_location = images_path + file
            img2vec = Img2Vec(model='densenet')
            img = Image.open(image_location)
            vec = img2vec.get_vec(img)
            # if all_vecs is None:
            #     all_vecs = vec
            # else:
            #     all_vecs = np.vstack([all_vecs, vec])
            # all_names.append(file)
            vector = vec.tolist()
            doc = {
                "id": str(i),
                "image_path": image_location,
                "vector": vector
            }
            solr.add(doc)
            print(f"Image Path: {image_location} Done")
        except Exception as e:
            print(f"Image Path: {image_location} Error: {str(e)}")
            continue

# np.save("all_vecs.npy", all_vecs)
# np.save("all_names.npy", all_names)
