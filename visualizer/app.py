from flask import Flask, request, jsonify, render_template
from flask import send_from_directory

ner_tag_descriptions = {
    'B-PERSON': 'Name of a person',
    'I-PERSON': 'Part of named entity that is name of a person',
    'B-ORGANIZATION': 'Name of an organization or group',
    'I-ORGANIZATION': 'Part of named entity that is name of an organization or group',
    'B-LOCATION': 'Location',
    'I-LOCATION': 'Part of named entity that is location',
    'B-GPE': 'Geopolitical entity (country, region, etc.)',
    'I-GPE': 'Part of named entity that is geopolitical entity',
    'B-DATE': 'Temporal expression, including a date',
    'I-DATE': 'Part of named entity that is temporal expression, including a date',
    'B-TIME': 'Time expression',
    'I-TIME': 'Part of named entity that is time expression',
    'B-MONEY': 'Monetary value',
    'I-MONEY': 'Part of named entity that is monetary value',
    'B-PERCENT': 'Percentage',
    'I-PERCENT': 'Part of named entity that is percentage',
    'B-QUANTITY': 'Measurement or quantity',
    'I-QUANTITY': 'Part of named entity that is measurement or quantity',
    'B-CARDINAL': 'Numerical value',
    'I-CARDINAL': 'Part of named entity that is numerical value',
    'B-ORDINAL': 'Ordinal number',
    'I-ORDINAL': 'Part of named entity that is ordinal number',
    'B-EVENT': 'Named event or occurrence',
    'I-EVENT': 'Part of named entity that is named event or occurrence',
    'B-WORK_OF_ART': 'Title of a creative work',
    'I-WORK_OF_ART': 'Part of named entity that is title of a creative work',
    'B-LAW': 'Legal reference or document',
    'I-LAW': 'Part of named entity that is legal reference or document',
    'B-LANGUAGE': 'Named language',
    'I-LANGUAGE': 'Part of named entity that is named language',
    'B-NORP': 'Nationality, religious affiliation, or political group',
    'I-NORP': 'Part of named entity that is nationality, religious affiliation, or political group'
}


def predict_bert(text, model_path):
    from transformers import pipeline
    ner = pipeline("token-classification",
                   model=model_path)
    return ner(text)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<path:path>')
def send_report(path):
    return send_from_directory('templates', path)


def the_largest_pref(string, list):
    for i in list:
        if i.startswith(string):
            return i


def predict_using_bert_model(text):
    global ner_tag_descriptions
    lens = [len(word) for word in text.split()]
    idx = [0]
    for ln in lens:
        idx.append(idx[-1] + ln + 1)
    del idx[-1]
    raw_pred = predict_bert(text, "../approaches/Using_BERT_Transformer/best_model")
    raw_pred.sort(key=lambda x: x['start'])
    pred = {'text_blocks': []}
    prev_end = 0
    for ent in raw_pred:
        prob = float(ent['score'])
        description_of_the_entity = ner_tag_descriptions[
            the_largest_pref(ent['entity'].upper(), ner_tag_descriptions.keys())]

        start = ent['start']
        end = ent['end']
        if prev_end < start:
            pred['text_blocks'].append([text[prev_end: start]])
        pred['text_blocks'].append([text[start:end], prob, description_of_the_entity])
        prev_end = end

    if prev_end != len(text):
        pred['text_blocks'].append([text[prev_end:]])

    return pred


@app.route('/perform_magic', methods=['POST'])
def perform_magic():
    data = request.json
    user_input = data.get('userInput')
    preds = predict_using_bert_model(user_input)
    return jsonify(preds)


app.run(debug=True)
