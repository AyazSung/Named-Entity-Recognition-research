from approaches.DistilBERT_uncased import Train_BERT_uncased
from data import data_parser

data_path = r"../../data/ner.csv"
print("Data parsing...")
df = data_parser.data_preparing(data_path)
print("Train DistilBERT model...")
modelBERT = Train_BERT_uncased.train_BERT(df)