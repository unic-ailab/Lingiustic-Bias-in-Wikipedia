"""
Tools to build the dataset.
"""
import re
from collections import Counter
import json
import spacy
import nltk


def extracting_features(text: str, positive_words: set, negative_words: set,
                        state_verbs_list: list, strong_verbs_list: list,
                        action_verbs_list: list, partOfSpeech_dict: dict):
    """
    This function help us extract the values for our features.
    Params:
    text-> the revisions content
    Returns:
    pos-> num of positive words
    neg-> num of negative words
    stV-> num of state verbs
    aV-> num of action verbs
    strV-> num of strong verbs
    adj-> num of adjectives
    mean_abstract_level-> mean abstraction level
    length-> num of total words
    """

    # num of total words
    tokens = nltk.word_tokenize(text)
    length = len(tokens)

    words_occurrences = Counter(tokens)

    pos = 0
    neg = 0
    strV = 0
    stV = 0
    aV = 0
    adj = 0

    for word in words_occurrences:
        if word in positive_words:
            pos += words_occurrences[word]
        elif word in negative_words:
            neg += words_occurrences[word]

        if (word in partOfSpeech_dict.keys()) and (partOfSpeech_dict[word] == "ADJ"):
            adj += words_occurrences[word]
        elif word in set(state_verbs_list):
            stV += words_occurrences[word]
        elif word in set(strong_verbs_list):
            strV += words_occurrences[word]
        elif word in set(action_verbs_list):
            aV += words_occurrences[word]

    try:
        meanAbstractLevel = mean_abstraction_level(strV, aV, stV, adj)
    except ZeroDivisionError:
        print("Issue here")
        print(len(tokens))
        meanAbstractLevel = None
        
    return pos, neg, stV, aV, strV, adj, length, meanAbstractLevel


def mean_abstraction_level(nSV: int, nAV: int, nStV: int, nADJ: int):
    """Mean Abstract Level computes the level of abstraction on the
    snapshot. It is based on the paper 'When Do We Communicate
    Stereotypes?  Influence of the Social Context on the Linguistic
    Expectancy Bias' (http://dx.doi.org/10.1177/1368430205053939).

    $mean_abstract_level=\frac{nSV*1+nAV*2+nStV*3+nADJ*4}{nSV+nAV+nStV+nADJ}$

    Params:
    nSV-> num Of Strong Verbs
    nAV-> num Of Action Verbs
    nStV-> num Of State Verbs
    nADJ-> num Of Adjectives

    Returns:
    mean_abstract_level-> the measurement regarding the abstraction

    """
    mean_abstract_level = (nSV*1+nAV*2+nStV*3+nADJ*4)/(nSV+nAV+nStV+nADJ)
    return mean_abstract_level


def open_files(files: list):
    """
    Helper function. Takes as input a list of files and returns two
    list of domain specific words.

    Params:
    files-> is a list of files that should be in the cwd
    Return:
    pos_domain_words_list, neg_domain_words_list
    """
    pos_domain_words_list = []
    neg_domain_words_list = []
    for file in files:
        with open(file, 'r') as file_handle:
            if file == 'pos_domain_words.txt':
                for line in file_handle.readlines():
                    pos_domain_words_list.append(line.strip())
            else:
                for line in file_handle.readlines():
                    neg_domain_words_list.append(line.strip())

    return pos_domain_words_list, neg_domain_words_list


def revision_preprocessing(text: str):
    """
    Preprocessing revision's content.
    Params:
    text-> Revision's content to be processed
    Returns:
    clean_text-> the clean version of the revision
    """
    # remove html structure
    text = re.sub(r"thumb\|.*\|", " ", text)
    # remove punctuations
    text = re.sub(r"[^a-zA-Z]", " ", text)
    # lowercase and strip whitespaces
    clean_text = " ".join([word.lower().strip() for word in
                           text.split()])

    return clean_text


def load_revisions(file_path: str):
    """
    This function loads revisions history from file_path.
    Additionally, drops every entry that doesn't contain
    content.
    Params:
    file_path-> full path to the file
    Returns:
    revisions-> the cleaned version of revisions history
    """
    with open(file_path, "r") as f_reader:
        revisions = json.load(f_reader)

    for name in revisions.keys():
        print(name)
        counter = 0
        revisions_tobe_deleted = []
        for revId in revisions[name].keys():
            content = revisions[name][revId]["content"]
            if len(content) == 0:
                revisions_tobe_deleted.append(revId)
                counter += 1
            else:
                revisions[name][revId]["content"] = revision_preprocessing(content)
        for revId in revisions_tobe_deleted:
            del revisions[name][revId]
        print(f"{counter} revisions have been deleted")
        
    return revisions


def get_values_for_tables(revisions_history: dict, role: str, listOfFemales: list,
                          positive_words: set, negative_words: set,
                          state_verbs_list: list, strong_verbs_list: list,
                          action_verbs_list: list):
    """
    This function loops takes as inputs a dictionary of dictionaries.
    Each sub-dictionary represents a history of revisions for a person.
    It would be better if the dictionary is related to humans with specific
    role e.g scientists, politicians etc.
    Params:
    revisions_history-> dictionary of dictionaries with biographies
    role-> the specific role that characterize all the persons described
    in biographies. It should be lowercased.
    listOfFemales-> a list of names that corresponds to females
    Returns:
    values-> is a list of lists of values. Each sub-list corresponds to
    values for a specific snapshot.
    """
    role = role.lower()
    values = []
    nlp = spacy.load("en_core_web_sm")
    print(f"Feature Extraction - Begins - {role.capitalize()}s")
    
    for name in revisions_history.keys():
        print(name)
        i = 0
        if name in listOfFemales:
            gender = 'f'
        else:
            gender = 'm'
        for revid in revisions_history[name].keys():
            content = revisions_history[name][revid]["content"]
            # Every 250 revisions we build a new dictionary that contains
            # pairs of words and corresponded part of speech tags.
            if i % 250 == 0:
                print(i)
                tmp_dict = {}
                doc = nlp(content)
                for token in doc:
                    tmp_dict[token.text] = token.pos_
            role = role
            date = revisions_history[name][revid]["timestamp"]
            user = revisions_history[name][revid]["userId"]
            pos, neg, stV, aV, strV, adj, length, mal = extracting_features(content, positive_words, negative_words,
                                                                            state_verbs_list, strong_verbs_list,
                                                                            action_verbs_list, tmp_dict)
            values.append([name, revid, user, date, gender, role,
                           length, pos, neg, strV, aV, stV,
                           adj, mal])
            i += 1

    return values
