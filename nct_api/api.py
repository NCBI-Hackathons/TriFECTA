from flask import Flask
from flask import request
import json
from pymongo import MongoClient
from bson.json_util import dumps

import sqlite3

client = MongoClient('localhost', 27017)
db = client['trifecta']

app = Flask(__name__)


def update(db, collection, query, update):
    collection = db[collection]
    return collection.find_one_and_update(query, update, return_document=pymongo.ReturnDocument.AFTER)


def read(db, collection, query, db_filter=None):
    collection = db[collection]
    cursor = collection.find(query, db_filter)
    result_list = []
    for result in cursor:
        result_list.append(result)
    return result_list


def save_tags(trial_id, structured_tags):
    query = {'trial_id': trial_id}
    # trial = read(client, 'trials', query)[0]
    update = {'$set': {'tags': structured_tags['tags']}}
    trial = update(trial_id, 'trials', query, update)
    return trial


def get_trial(trial_id):
    pass


@app.route('/')
def hello():
    return "Welcome to the Fantastical Emporium of Clinical Trial Assortments"


@app.route('/query', methods=['GET'])
def query_trials():
    tags = request.args.get('tags')
    if not tags:
        return dumps({"message": "No trials found"})
    query = {'tags': {'$in': tags.strip().split(',')}}


@app.route('/trial/<trial_id>', methods=['GET', 'PUT'])
def modify_trial(trial_id):
    if request.method == 'PUT':
        return dumps(save_tags(trial_id, request.get_json()))
    if request.method == 'GET':
        return dumps(get_trial(trial_id))
