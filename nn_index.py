import numpy as np
import os 
import faiss                   
import json

from transformers import DistilBertTokenizer, DistilBertModel
from tqdm import tqdm

DATA_DIR = 'data/wsj'
VEC_DIM = 768
HARD_STOP = float('inf')
LOADED = True
K = 10

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained("distilbert-base-uncased")

def get_vector(text):
    encoded_input = tokenizer(text, return_tensors='pt')
    vec = model(**encoded_input)
    vec = vec.last_hidden_state.detach().numpy()
    vec = vec.reshape(vec.shape[1], vec.shape[2])
    vec = np.mean(vec, axis=0)
    return vec

all_articles = []

for fname in os.listdir(DATA_DIR): 
    full_fname = f'{DATA_DIR}/{fname}'
    with open(full_fname, 'r') as f: 
        new_articles = json.loads(f.read())
        all_articles.extend(new_articles)

all_articles = all_articles[::-1] # Most to least recent
        
if not LOADED: 
    print("Loading vectors...")
    vecs = []
    for i, article in tqdm(enumerate(all_articles)): 
        vec = get_vector(article['title'])
        vecs.append(vec)
        if i == HARD_STOP: break

    vecs = np.array(vecs)

    np.save('data.npy', vecs)

vecs = np.load('data.npy')

index = faiss.IndexFlatL2(VEC_DIM)   

index.add(vecs) 

for i, article in enumerate(all_articles):
    print()
    print()
    print()
    print(f"Searching article {article['title']}")
    vec = get_vector(article['title'])
    vec = vec.reshape(1, -1)
    d, inds = index.search(vec, K)
    inds = inds[0]
    j = 1
    for ix in inds:
        if ix == i: continue
        nbr = all_articles[ix]
        print(f"Neighbor {j}")
        print(f"Article title: {nbr['title']}")
        print()
        j += 1    
    breakpoint()

