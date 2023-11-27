from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np
def predict_rnn(text, path_pref):

    model = load_model(f"{path_pref}/best_model")
    with open(f"{path_pref}/tokenizer.pickle", 'rb') as handle:
        tokenizer = pickle.load(handle)
    with open(f"{path_pref}/tag_tokenizer.pickle", 'rb') as handle:
        tag_tokenizer = pickle.load(handle)
    max_length = 89

    predictions = model.predict(pad_sequences(tokenizer.texts_to_sequences([text]),
                                              maxlen=max_length,
                                              padding="post"))
    pred_ner = np.argmax(predictions, axis=-1)
    NER_tags = [tag_tokenizer.index_word[num] for num in list(pred_ner.flatten())]

    return NER_tags


# print(predict_rnn("Washington avenue Grand Cathedral let's go to Google office at September 9",
#                    'best_model'))
