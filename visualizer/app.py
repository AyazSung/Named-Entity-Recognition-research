from flask import Flask, request, jsonify, render_template
from flask import send_from_directory

ner_tag_descriptions = {
    'B-PERSON': 'Name of a person',
    'I-PERSON': 'Part of named entity that is name of a person',
    'B-ORGANIZATION': 'Name of an organization or group',
    'I-ORGANIZATION': 'Part of named entity that is name of an organization or group',
    'B-LOCATION': 'Location',
    'I-LOCATION': 'Part of named entity that is location',
    'B-GEO': "Geographical entity",
    'I-GEO': "Part of named entity that is geographical entity",
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
    'B-ART': 'Title of a creative work',
    'I-ART': 'Part of named entity that is title of a creative work',
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


def predict_using_RNN(text):
    global ner_tag_descriptions
    from approaches.NER_using_RNN.Predict_RNN import predict_rnn

    raw_pred = predict_rnn(text, "../approaches/NER_using_RNN")
    pred = {'text_blocks': []}
    text = text.split()
    for i, ent in enumerate(raw_pred):
        if i == len(text):
            break
        ent = ent.upper()
        if ent == 'O':
            pred['text_blocks'].append([text[i]])
        else:
            prob = 1.
            description_of_the_entity = ner_tag_descriptions[the_largest_pref(ent, ner_tag_descriptions.keys())]
            pred['text_blocks'].append([text[i], prob, description_of_the_entity])
    return pred


def predict_using_BERT_models(text, path_to_model):
    global ner_tag_descriptions

    raw_pred = predict_bert(text, path_to_model)
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


def predict_using_SPACY(text):
    from approaches.SPACY.model_class import SpacyTrained

    st = SpacyTrained('../approaches/SPACY/output_models')

    doc = st.predict_entities(text)
    entities = []
    prob = 1
    end = 0
    for ent in doc.ents:
        description_of_the_entity = ner_tag_descriptions[
            the_largest_pref("B-" + ent.label_.upper(), ner_tag_descriptions.keys())]
        nidx = text.index(ent.text, end)
        if nidx > end:
            entities.append([text[end:nidx]])
        end = nidx + len(ent.text)
        entities.append([ent.text, prob, description_of_the_entity])
    return {'text_blocks': entities}

@app.route('/perform_magic', methods=['POST'])
def perform_magic():
    data = request.json
    print(data)
    user_input = data.get('userInput')
    model = data.get('model')

    preds = None
    if model == 'BERT':
        preds = predict_using_BERT_models(user_input, "../approaches/Using_BERT_Transformer/best_model")
    elif model == "RNN":
        preds = predict_using_RNN(user_input)
    elif model == "DistilBERT":
        preds = predict_using_BERT_models(user_input, "../approaches/DistilBERT_uncased/model")
    elif model == "Albert":
        preds = predict_using_BERT_models(user_input, "../approaches/Albert_pre_trained/model")
    elif model == "Spacy":
        preds = predict_using_SPACY(user_input)
    return jsonify(preds)


app.run(debug=True)
