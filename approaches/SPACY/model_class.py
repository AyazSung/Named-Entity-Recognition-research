import time
import numpy as np
import pandas as pd
import os

import spacy
import en_core_web_sm

from sklearn.model_selection import train_test_split
import ast

import spacy
from spacy.tokens import DocBin
from spacy.util import filter_spans

from spacy.training import Example
import random
from tqdm import tqdm


class SpacyTrained:
    def __init__(self):
        spacy.prefer_gpu()
        self.nlp = spacy.load("en_core_web_sm")
        self.output_dir = 'output_models'
        print("Loading from", self.output_dir)
        self.nlp_updated = spacy.load(self.output_dir)

    def predict_entities(self, text):
        model = self.nlp
        doc = model(text)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        return doc
