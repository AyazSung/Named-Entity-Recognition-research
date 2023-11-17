from approaches.Using_BERT_Transformer import Train_BERT
from data import data_parser

data_path = r"../../data/ner.csv"
print("Data parsing...")
df = data_parser.data_preparing(data_path)
print("Train BERT model...")
modelBERT = Train_BERT.train_BERT(df)