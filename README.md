# Named Entity Recognition research

## Dataset description
Every row in the [dataset](https://www.kaggle.com/datasets/naseralqaydeh/named-entity-recognition-ner-corpus/data) contains a complete sentence and list of NER tags for each
word in the sentence.
#### Each NER tag belongs to the one of the following 16 types:

| Key     | Description                                             |
| ------- | ------------------------------------------------------- |
| B-PER   | Name of a person                                        |
| I-PER   | Part of named entity that is the name of a person       |
| B-GEO   | Geographical entity                                     |
| I-GEO   | Part of named entity that is a geographical entity      |
| B-ART   | Title of a creative work                                |
| I-ART   | Part of named entity that is the title of a creative work |
| B-GPE   | Geopolitical entity (country, region, etc.)             |
| I-GPE   | Part of named entity that is a geopolitical entity      |
| B-EVE   | Named event or occurrence                               |
| I-EVE   | Part of named entity that is a named event or occurrence |
| B-NAT   | Nationality, religious affiliation, or political group  |
| I-NAT   | Part of named entity that is nationality, religious affiliation, or political group |
| B-ORG   | Name of an organization or group                        |
| I-ORG   | Part of named entity that is the name of an organization or group |
| B-TIM   | Time expression                                         |
| I-TIM   | Part of named entity that is a time expression          |

Data sample:

![image](https://github.com/MaratMedvedev/Named-Entity-Recognition-research/assets/90756690/3184e7a3-a7fd-440f-884d-df4cacc17ad5)

You can see this dataset in `data/ner.csv`.
## How to run the visualizer?

Firstly, you should install all requarements. For that purpose, you should run the following command:

`pip install -r requirements.txt`

After that, you simply run the `visualizer/app.py` and program run our application on your localhost. 

Next, you will see like this in your python console:
~~~
* Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
...
~~~
Now, you just should follow the link in console. 
Finally, you can use the our app.


