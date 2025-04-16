import torch
import accelerate
from transformers import AutoProcessor, LlavaForConditionalGeneration
from PIL import *
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity
import clip
import os
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import pandas as pd
import pickle
import json
from datasets import Dataset, Image
from torch.utils.data import DataLoader
import torch.nn as nn
from typing import List, Union, Tuple
import faiss

## function for llava to caption an image
def caption_image(image, llava_model, processor):
    prompt = "This is a photo from my camera role. Please caption it in a way that a user would"
    caption = ""
    
    conversation = [
        {
    
          "role": "user",
          "content": [
              {"type": "text", "text": prompt},
              {"type": "image"},
            ],
        },
    ]
    prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
    inputs = processor(images=image, text=prompt, return_tensors="pt").to("cuda:0")
    # autoregressively complete prompt
    output = llava_model.generate(**inputs, max_new_tokens=30) ## might be good to play around with number of tokenz to see what is ideal for similarity. 
    #Naive make tokens == to user prompt lenth
    caption = processor.decode(output[0], skip_special_tokens=True)

    # Extract only the assistant's caption
    if "ASSISTANT:" in caption:
        caption = caption.split("ASSISTANT:")[-1].strip()
    else:
        caption = caption.strip()
    
    # print(processor.decode(output[0], skip_special_tokens=True))
    return caption

## function to calculate cosine similartity between caption and query
def image_similarity(caption, prompt="me playing basket ball at the local recreation center with my friends"):
    ##Similarirty with clip is much better than  TfIdf strat
    device = "cuda"
    clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)
    query_emb = clip_model.encode_text(clip.tokenize([prompt]).to(device)).detach().cpu().numpy()
    caption_emb = clip_model.encode_text(clip.tokenize([caption]).to(device)).detach().cpu().numpy()
    return cosine_similarity(query_emb, caption_emb)[0][0]