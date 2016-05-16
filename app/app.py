# andr
#
# make sure you setup DictAPIKey and GoogleTransAPIKey in the config.ini
#
# todo:
# - clean up code, use pep8

from flask import Flask, jsonify, make_response, request, abort, render_template
import xml.etree.ElementTree as ET
import ConfigParser
import requests, urllib

app = Flask(__name__)
config = ConfigParser.ConfigParser()
config.read('./config.ini')

dict_api_key=config.get('config', 'DictAPIKey')
google_trans_api_key=config.get('config', 'GoogleTransAPIKey')


# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
                           title='Home',
                           body="This is a WIP")

@app.route('/api/query', methods=['GET'])
def query_word():

    if not request.args['w'] or not request.args['t']:
        abort(400)

    word = request.args['w']
    #sLang = request.json['source_lang'] 
    sLang = 'en' #source has to be english
    tLang = request.args['t']
    resp=[]


    dictDefs = get_websters_def(word)

    # translate synonyms
    for dictDef in dictDefs:
        for x, sense in enumerate(dictDef['senses']):
            dictDef['senses'][x]['translated synonyms'] = googleTrans(sense['synonyms'], sLang, tLang)

    result = {
        'word': word,
        'definitions': dictDefs
    }

    return jsonify({'result': result}), 200

def googleTrans(syns, sLang, tLang):

    # build goolge translate query string from source synonyms
    q_string=''
    for s in syns:
        q_string += '&q=' + urllib.quote_plus(s.strip())
    
    google_trans_url = 'https://www.googleapis.com/language/translate/v2?key=' + google_trans_api_key + '&source=' + sLang + '&target=' + tLang + '&' + q_string.lstrip('&')
    r = requests.get(google_trans_url)
    response=r.json()
    
    tArray=[]
    for i in response['data']['translations']:
        tArray.append(i['translatedText'])

    return tArray

def get_websters_def(word):

    # make dictionary API call
    dict_url = 'http://www.dictionaryapi.com/api/v1/references/thesaurus/xml/' + word + '?key=' + dict_api_key
    r = requests.get(dict_url)
    root = ET.fromstring(r.content)

    dictDefs=[]

    # for each entry found for searched word, find all senses for each functional label
    for entry in root:

        fl=entry.find('fl').text

        dictDef = {
            'functional label': fl,
            'senses': []
        }

        # get definition, example and synonyms for each sense 
        for sense in entry.findall('./sens'):

            definition=sense.find('./mc').text
            syn=sense.find('./syn').text
            syns=[]
            for s in syn.split(','):
                syns.append(s.strip())
                


            example=''
            for i in sense.find('./vi').itertext():
                example += i

            DefSense = {
                'definition': definition,
                'example': example,
                'synonyms': syns
            }

            dictDef['senses'].append(DefSense)

        dictDefs.append(dictDef) 

    return dictDefs

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int("80"))
