from transformers import pipeline


def predict_bert(text):
    ner = pipeline("token-classification",
                   model='model/checkpoint-13587')
    return ner(text)


print(predict_bert("washington avenue Grand Cathedral let's go to Goggle office at September 9"))
