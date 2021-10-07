import numpy as np
import pandas as pd
import json
from utils import frequencies, mean_abstract_level

import seaborn as sns
import matplotlib.pyplot as plt

# you should choose the path where you have downloaded the revisions
path = '/home/emath/Data Science/AI Lab-Research/Wikipedia Project/Data/biographies_rev_history_new.json'
with open(path, 'r') as read_file:
    revisions = json.load(read_file)

# We drop all the revisions that don't contain 'content'
for name in revisions.keys():
    print(name)
    counter = 0 # we keep track of how many revisions per biography have been deleted
    revisions_to_be_deleted = []
    for rev_id in revisions[name].keys():
        if len(revisions[name][rev_id]['content']) == 0:
            # delete all the revisions that don't have content
            # the content has been deleted prior to our analysis
            revisions_to_be_deleted.append(rev_id)
            counter += 1
    for rev_id in revisions_to_be_deleted:
        del revisions[name][rev_id]


# load the didaxto's dictionaries
# Dictionaries are provided so you can change the path below respectively
with open("/home/emath/Data Science/AI Lab-Research/Wikipedia Project/Data/neg_domain_words.txt", "rb") as read_file:
    neg_domain_words = set(line.decode(errors='ignore').strip() for line in read_file)
    
with open("/home/emath/Data Science/AI Lab-Research/Wikipedia Project/Data/pos_domain_words.txt", "rb") as read_file:
    pos_domain_words = set(line.decode(errors='ignore').strip() for line in read_file)

# Build lists to create a dataframe
columns = ['name', 'revision Id', 'Date', 'length', 
           'pos_words', 'neg_words', 'adjectives',
           'verbs', 'adverbs'] 
values = []
posTags = {}
for name in revisions.keys():
    i=0
    for revid in revisions[name].keys():
        content = revisions[name][revid]['content']
        pos, neg, adj, verbs, adverbs, length = frequencies(content, posTags, pos_domain_words, neg_domain_words)
        values.append([name, revid, revisions[name][revid]['timestamp'], length, pos, neg, adj, verbs, adverbs])
        i += 1

revisions_df = pd.DataFrame(data=values, columns=columns)
revisions_df['mean_abstract_level'] = mean_abstract_level(revisions_df)

# create a dataframe. Each row represents a revision for a specific biography
revisions_df['Date'] = pd.to_datetime(revisions_df['Date'])
revisions_df['pos_ratio'] = revisions_df['pos_words']/revisions_df['length']
revisions_df['neg_ratio'] = revisions_df['neg_words']/revisions_df['length']
revisions_df['adj_ratio'] = revisions_df['adjectives']/revisions_df['length']
revisions_df['vb_ratio'] = revisions_df['verbs']/revisions_df['length']
revisions_df['adv_ratio'] = revisions_df['adverbs']/revisions_df['length']

# We replace NaN values in "Mean Abstract Level" column with 0's
revisions_df["mean_abstract_level"] = revisions_df["mean_abstract_level"].fillna(0)

def gender(row: str):
    """
    Goes through all the names and returns 'm' if
    the name belong to a male or 'f' otherwise.
    """
    if row in  ["Recep Tayyip Erdoğan", "Emmanuel Macron", "Kyriakos Mitsotakis"]:
        return "m"
    else:
        return "f"

# Create a new column "Gender"
revisions_df["gender"] = revisions_df["name"].apply(gender) 
