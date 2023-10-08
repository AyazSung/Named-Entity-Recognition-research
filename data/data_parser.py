import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import ast


def data_reading_and_splitting(data_path, test_size=0.2, random_state=42):
    def load_data(data_path):
        df = pd.read_csv(data_path)
        # Remove null values if any
        df.dropna(inplace=True)
        return df

    def preprocess_data(df):
        for i in range(len(df)):
            pos = ast.literal_eval(df['POS'][i])
            tags = ast.literal_eval(df['Tag'][i])
            df['POS'][i] = [str(word) for word in pos]
            df['Tag'][i] = [str(word.upper()) for word in tags]
        return df

    df = preprocess_data(load_data(data_path))
    df_final = df[['Sentence', 'Tag']]

    df_train, df_test = train_test_split(df_final, test_size=test_size, random_state=random_state)
    return [df_train, df_test]
