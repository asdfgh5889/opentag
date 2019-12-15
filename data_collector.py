#https://data.gov.uz/ru/api/v1/json/sphere/1/dataset?access_key=f9f3d29f4fadb05e1d4efc0828a351c7
import json
import requests
from googletrans import Translator
from flask import Flask
from flask import render_template

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

def getUzbTags():
    f = open('uzb_tags.json', 'r')
    return json.loads(f.read())

app = Flask(__name__)
@app.route('/')
def index():
    dataset = getSampleJson()
    tags = getUzbTags()
    filtered = []
    return render_template('index.html', dataset=dataset)