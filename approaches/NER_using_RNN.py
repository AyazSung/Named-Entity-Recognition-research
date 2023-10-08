from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, Bidirectional, LSTM, Embedding
from keras.models import Model
from keras.losses import SparseCategoricalCrossentropy
from keras.callbacks import EarlyStopping

def NER_RNN(df_train, df_test, train_epochs=5):
    train_targets = list(df_train.Tag.values)
    test_targets = list(df_test.Tag.values)

    tokenizer = Tokenizer(lower=False, oov_token="UNK")
    tokenizer.fit_on_texts(df_train['Sentence'])

    train_inputs = tokenizer.texts_to_sequences(df_train['Sentence'])
    test_inputs = tokenizer.texts_to_sequences(df_test['Sentence'])

    word2idx = tokenizer.word_index
    V = len(word2idx)  # Vocab size
    print("Found %s unique tokens " % V)

    train_tags = set([val for sublist in train_targets for val in sublist])
    test_tags = set([val for sublist in test_targets for val in sublist])

    print("Unique NER tags in train set: ", train_tags)
    print("Unique NER tags in test set: ", test_tags)

    tag_tokenizer = Tokenizer()
    tag_tokenizer.fit_on_texts(train_targets)
    train_tgt_int = tag_tokenizer.texts_to_sequences(train_targets)
    test_tgt_int = tag_tokenizer.texts_to_sequences(test_targets)

    # Max length
    max_length_train = max(len(sent) for sent in train_inputs)
    max_length_test = max(len(sent) for sent in test_inputs)
    max_length = max(max_length_train, max_length_test)

    # Pad input sequences
    train_inputs_final = pad_sequences(train_inputs, maxlen=max_length, padding="post")
    print("Shape of train inputs: ", train_inputs_final.shape)

    test_inputs_final = pad_sequences(test_inputs, maxlen=max_length, padding="post")
    print("Shape of test inputs: ", test_inputs_final.shape)

    train_targets_final = pad_sequences(train_tgt_int, maxlen=max_length, padding="post")
    print("Shape of train targets: ", train_targets_final.shape)

    test_targets_final = pad_sequences(test_tgt_int, maxlen=max_length, padding="post")
    print("Shape of test targets: ", test_targets_final.shape)

    # Number of classes
    K = len(tag_tokenizer.word_index) + 1
    vector_size = 16

    i = Input(shape=(max_length,))
    x = Embedding(input_dim=V + 1, output_dim=vector_size, mask_zero=True)(i)
    x = Bidirectional(LSTM(32, return_sequences=True))(x)
    x = Dense(K)(x)

    model = Model(i, x)
    print(model.summary())

    # Compile and fit
    model.compile(optimizer="adam", loss=SparseCategoricalCrossentropy(from_logits=True), metrics=["accuracy"])
    model.fit(train_inputs_final,
              train_targets_final, epochs=train_epochs, validation_data=(test_inputs_final, test_targets_final))

    return model