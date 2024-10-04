import os
from keybert import KeyBERT
import pickle

filepath = "./starter/"
file_list = os.listdir(filepath)
i = 0
txts = []
for f in file_list:
    with open(filepath + f, 'r') as fh:
        txts.append([f, fh.read()])
    i = i + 1
    if i > 2:
        break

to_graph = []
kw_model = KeyBERT()
for file, txt in txts:
    to_graph.append({"file":file, "keywords":kw_model.extract_keywords(txt)})

#print(to_graph[0][0], to_graph[0][1])
with open("kw_list.pkl", "wb") as f:
    pickle.dump(to_graph, f)


with open("kw_list.pkl", "rb") as f:
    opened = pickle.load(f)

print(opened[0]["file"], opened[0]["keywords"])
