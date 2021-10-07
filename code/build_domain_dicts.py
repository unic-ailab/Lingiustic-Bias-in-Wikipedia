import os
import glob
from utils import open_files

# Build dictionaries for scientists - START HERE
os.chdir("/home/emath/GoogleDrive/LingBias_Ext/didaxTo/")
files = ["pos_domain_words.txt", "neg_domain_words.txt"]

foldernames = []

for folder in glob.glob("SCIENTISTS_*"):
    foldernames.append(folder)

pos_scientists_words_list = []
neg_scientists_words_list = []

for folder in foldernames:
    os.chdir("/home/emath/GoogleDrive/LingBias_Ext/didaxTo/"+folder)
    pos_list, neg_list = open_files(files)
    pos_scientists_words_list.extend(pos_list)
    neg_scientists_words_list.extend(neg_list)

scientists_pos_words_set = set(pos_scientists_words_list)
scientists_neg_words_set = set(neg_scientists_words_list)

# Build dictionaries for politicians - START HERE
os.chdir("/home/emath/GoogleDrive/LingBias_Ext/didaxTo/")
foldernames = []

for folder in glob.glob("BIO_*"):
    foldernames.append(folder)


pos_polit_words_list = []
neg_polit_words_list = []

for folder in foldernames:
    os.chdir("/home/emath/GoogleDrive/LingBias_Ext/didaxTo/"+folder)
    pos_list, neg_list = open_files(files)
    pos_polit_words_list.extend(pos_list)
    neg_polit_words_list.extend(neg_list)

politicians_pos_words_set = set(pos_polit_words_list)
politicians_neg_words_set = set(neg_polit_words_list)


# Build dictionaries for athletes - START HERE
os.chdir("/home/emath/GoogleDrive/LingBias_Ext/didaxTo/ATHLETSWITHSIXOLYMPICAPPEARANCES_DIDAXTO-dictionary/")
files = ["pos_domain_words.txt", "neg_domain_words.txt"]

pos_domain_words_list, neg_domain_words_list = open_files(files)

positive_words_set = set(pos_domain_words_list)
negative_words_set = set(neg_domain_words_list)

# Save dictionaries into txt documents
os.chdir("/home/emath/Data Science/Projects/LingBias_in_Wikipedia_ext/data/")

with open("pos_words_politics.txt", "w") as file_writer:
    for word in politicians_pos_words_set:
        file_writer.write(word)
        file_writer.write("\n")

with open("neg_words_politics.txt", "w") as file_writer:
    for word in politicians_neg_words_set:
        file_writer.write(word)
        file_writer.write("\n")
        
with open("pos_words_scientits.txt", "w") as file_writer:
    for word in scientists_pos_words_set:
        file_writer.write(word)
        file_writer.write("\n")
        
with open("neg_words_scientits.txt", "w") as file_writer:
    for word in scientists_neg_words_set:
        file_writer.write(word)
        file_writer.write("\n")

with open("pos_words_athletes.txt", "w") as file_writer:
    for word in positive_words_set:
        file_writer.write(word)
        file_writer.write("\n")

with open("neg_words_athletes.txt", "w") as file_writer:
    for word in negative_words_set:
        file_writer.write(word)
        file_writer.write("\n")
