import json
import requests
import nltk
from googletrans import Translator
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

t = Translator()

def getTranlatedTitles():
    raw_data = open('translated.json', 'r')
    json_data = raw_data.read()
    raw_data.close()
    dataset = json.loads(json_data)
    return dataset

def getSampleJson():
    raw_data = open('sample.json', 'r')
    json_data = raw_data.read()
    raw_data.close()
    dataset = json.loads(json_data)
    return dataset

def getSampleTitles(dataset):
    titles = []
    for d in dataset:
        titles.append(d['title'])
    return titles

def writeTranslated(titles):
    translated_file = open('translated.json', 'w')
    print('Translating')
    tranlated = t.translate(titles, src='uz')
    print('Done tranlating')
    translated_file.write(json.dumps(list(map(lambda x: x.text, tranlated))))
    print('Done')
    translated_file.close()

def unionSearchTag(keys, tags, titles):
    key_indexes = set()
    result = []
    for k in keys:
        for v in tags[k]:
            key_indexes.add(v)
    return key_indexes

def interSearchTag(keys, tags, titles):
    if len(keys) == 0:
        return []
    
    key_indexes = set(tags[keys[0]])

    for k in keys:
        key_indexes = key_indexes.intersection(set(tags[k]))
    return key_indexes

def translateTags(tags):
    uzb_tags_list = []
    uzb_tags_val = []
    for k, v in tags.items():
        uzb_tags_list.append(k)
        uzb_tags_val.append(v)

    print("Translating back")
    t = Translator()
    uzb_tags_tra = t.translate(uzb_tags_list, dest='uz')
    uzb_tags_list = list(map(lambda x: x.text, uzb_tags_tra))
    print("Done")

    uzb_tags = {}

    for i, t in enumerate(uzb_tags_list):
        uzb_tags[t] = uzb_tags_val[i]
    return uzb_tags

def writeUzbTags(tags):
    f = open('uzb_tags.json', 'w')
    f.write(json.dumps(tags))
    f.close()

def getUzbTags():
    f = open('uzb_tags.json', 'r')
    return json.loads(f.read())

# tags = {}


# titles = getTranlatedTitles()
# text = ' '.join(titles).lower()
# regex = RegexpTokenizer(r'\w+')
# filtered = regex.tokenize(text)

# stop_words = set(stopwords.words('english'))
# filtered = [w for w in filtered if (not w in stop_words and len(w) > 3)]
# freq = nltk.FreqDist(filtered)

# for w in freq.most_common(len(filtered)):
#     for i, t in enumerate(titles):
#         if t.find(w[0]) != -1:
#             if tags.get(w[0]) == None:
#                 tags[w[0]] = [i]
#             else:
#                 tags[w[0]].append(i)

uzb_titles = getSampleTitles(getSampleJson())
uzb_tags = getUzbTags()

print("Enter tag: ")
keys = input().split(' ')
print('Union')
print(unionSearchTag(keys, uzb_tags, uzb_titles))
print('\nIntersection')
print(interSearchTag(keys, uzb_tags, uzb_titles))