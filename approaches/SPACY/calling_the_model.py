from model_class import *

st = SpacyTrained('output_models')

doc = st.predict_entities("Microsoft company was founded in 1945 year by Bill Gates and Paul Allen.")

for ent in doc.ents:
    print(ent.text, ent.label_)