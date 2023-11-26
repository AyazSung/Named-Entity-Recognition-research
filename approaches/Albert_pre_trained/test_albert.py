from approaches.Albert_pre_trained import Train_Albert
from data import data_parser

data_path = r"../../data/ner.csv"
print("Data parsing...")
df = data_parser.data_preparing(data_path)
print("Train AlBERT model...")
modelBERT = Train_Albert.train_BERT(df)