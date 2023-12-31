import streamlit as st
import numpy as np
from PIL import Image
import time
from scipy.spatial.distance import cdist
import requests
from get_images import generate_random_image, find_similar_image

_, fcol2, _ = st.columns(3)
scol1, scol2 = st.columns(2)

ch = scol1.button("Start / change")
fs = scol2.button("find similar")

if ch:
    random_image = generate_random_image()
    image_name = random_image.split("/")[-1]
    fcol2.image(Image.open(requests.get(random_image, stream=True).raw))
    st.session_state["disp_img"] = random_image
if fs:
    image_name = st.session_state["disp_img"]
    similar_images = find_similar_image(image_name)
    fcol2.image(Image.open(requests.get(image_name, stream=True).raw))
    if len(similar_images) != 0:
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.image(Image.open(requests.get(similar_images[1], stream=True).raw))
        c2.image(Image.open(requests.get(similar_images[2], stream=True).raw))
        c3.image(Image.open(requests.get(similar_images[3], stream=True).raw))
        c4.image(Image.open(requests.get(similar_images[4], stream=True).raw))
        c5.image(Image.open(requests.get(similar_images[5], stream=True).raw))
    else:
        root = "/Users/janeshmishra/Downloads/no_image.png"
        c1 = st.columns(1)
        c1.image(Image.open(root))
