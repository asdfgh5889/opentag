import json
import requests
import nltk
import hashlib
import goslate
import concurrent.futures
from googletrans import Translator
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

t = Translator()

def getDataFromUrl(URL):
    r = requests.get(URL, verify=False)
    data = r.json()
    return data

def saveDataFromUrl(data, filename):
    f = open(filename, 'w')
    f.write(json.dumps(data))
    f.close()


def getTranlatedTitles(filename):
    raw_data = open(filename, 'r')
    json_data = raw_data.read()
    raw_data.close()
    dataset = json.loads(json_data)
    return dataset

def getSampleJson(filename):
    raw_data = open(filename, 'r')
    json_data = raw_data.read()
    raw_data.close()
    dataset = json.loads(json_data)
    return dataset

def getSampleTitles(dataset):
    titles = []
    for d in dataset:
        titles.append(d['title'])
    return titles

def writeTranslated(titles, filename):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=200)
    gs = goslate.Goslate(executor=executor)
    # translate = Translator()
    translated_file = open(filename, 'w')
    print('Translating')
    # translated = translate.translate(titles, src='uz')
    translated = gs.translate(titles, 'en')
    print('Done translating')
    # translated_file.write(json.dumps(list(map(lambda x: x.text, translated))))
    translated_file.write(json.dumps(list(translated)))
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
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=200)
    gs = goslate.Goslate(executor=executor)
    for k, v in tags.items():
        uzb_tags_list.append(k)
        uzb_tags_val.append(v)

    print("Translating back")
    # t = Translator()
    # uzb_tags_tra = t.translate(uzb_tags_list, dest='uz')
    # uzb_tags_list = list(map(lambda x: x.text, uzb_tags_tra))
    uzb_tags_list = gs.translate(uzb_tags_list, 'uz')
    print("Done")

    uzb_tags = {}

    for i, t in enumerate(list(uzb_tags_list)):
        uzb_tags[t] = uzb_tags_val[i]
    return uzb_tags

def writeUzbTags(tags, filename):
    f = open(filename, 'w')
    f.write(json.dumps(tags))
    f.close()

def getUzbTags(filename):
    f = open(filename, 'r')
    return json.loads(f.read())

def getEnglishTags(filename):
    tags = {}
    titles = getTranlatedTitles(filename)
    text = ' '.join(titles).lower()
    regex = RegexpTokenizer(r'\w+')
    filtered = regex.tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered = [w for w in filtered if (not w in stop_words and len(w) > 3)]
    freq = nltk.FreqDist(filtered)

    for w in freq.most_common(len(filtered)):
        for i, t in enumerate(titles):
            if t.find(w[0]) != -1:
                if tags.get(w[0]) == None:
                    tags[w[0]] = [i]
                else:
                    tags[w[0]].append(i)
    return tags

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

# uzb_titles = getSampleTitles(getSampleJson())
# uzb_tags = getUzbTags()
#
# print("Enter tag: ")
# keys = input().split(' ')
# print('Union')
# print(unionSearchTag(keys, uzb_tags, uzb_titles))
# print('\nIntersection')
# print(interSearchTag(keys, uzb_tags, uzb_titles))

def init(URL):
    data = getDataFromUrl(URL)
    url_hash = str(hashlib.sha256(URL.encode()).hexdigest())
    filename = url_hash + "_sample.json"
    saveDataFromUrl(data, filename)
    uzb_titles = getSampleJson(filename)
    titles = getSampleTitles(uzb_titles)
    filename_titles = url_hash + '_translated.json'
    writeTranslated(titles, filename_titles)
    tags = getEnglishTags(filename_titles)
    uzb_tags = translateTags(tags)
    filename_uzb_tags = url_hash + '_uzb_tags.json'
    writeUzbTags(uzb_tags, filename_uzb_tags)
    print(getUzbTags(filename_uzb_tags))

init("https://data.gov.uz/ru/api/v1/json/sphere/5/dataset?access_key=f9f3d29f4fadb05e1d4efc0828a351c7")


