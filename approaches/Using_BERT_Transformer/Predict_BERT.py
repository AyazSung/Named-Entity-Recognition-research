from transformers import pipeline


def predict_bert(text, model_path):

    ner = pipeline("token-classification",
                   model=model_path)
    return ner(text)


print(predict_bert("washington avenue Grand Cathedral let's go to Google office at September 9",
                   'best_model'))
