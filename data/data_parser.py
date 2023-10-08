import pandas as pd
import ast


def data_preparing(data_path):
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

    return df_final
