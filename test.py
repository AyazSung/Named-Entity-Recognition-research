from approaches import NER_using_RNN
from data import data_parser

data_path = r"data/ner.csv"
print("Data parsing...")
df_train, df_test = data_parser.data_reading_and_splitting(data_path, test_size=0.2, random_state=42)
print("Train rnn model...")
model = NER_using_RNN.NER_RNN(df_train, df_test, train_epochs=5)
