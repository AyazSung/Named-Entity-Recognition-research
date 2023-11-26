from datasets import Dataset, load_dataset
from transformers import AutoTokenizer
from transformers import DataCollatorForTokenClassification
import evaluate
import numpy as np
from transformers import AutoModelForTokenClassification, TrainingArguments, Trainer

def train_BERT(df_final):
    # Unique labels
    labels = [set([val for sublist in df_final['Tag'].values for val in sublist])]

    # Label2index
    label2index = {"O": 0, "B-PER": 1, "I-PER": 2, "B-GEO": 3, "I-GEO": 4, "B-ART": 5, "I-ART": 6,
                   "B-GPE": 7, "I-GPE": 8, "B-EVE": 9, "I-EVE": 10, "B-NAT": 11, "I-NAT": 12, "B-ORG": 13,
                   "I-ORG": 14, "B-TIM": 15, "I-TIM": 16}

    index2label = {v: k for k, v in label2index.items()}

    def create_tokens(text):
        data = [word for word in text.split()]
        return data

    def create_num_labels(label):
        num_label = [label2index[text] for text in label]
        return num_label

    df_trf = df_final.copy()
    df_trf.loc[:, 'Tokens'] = df_trf['Sentence'].apply(lambda x: create_tokens(x))
    df_trf.loc[:, 'NER_Tags'] = df_trf['Tag'].apply(lambda label: create_num_labels(label))

    # Remove rows with unequal # tokens and # tags
    index_labels = []
    for i in range(len(df_trf)):
        if len(df_trf['Tokens'][i]) != len(df_trf['NER_Tags'][i]):
            print(f"Tokens and tags at index {i} don't match")
            index_labels.append(i)

    # Drop rows at index positions in index_labels
    for idx in index_labels:
        df_trf.drop(index=idx, inplace=True)

    # Reset index
    df_trf.reset_index(drop=True, inplace=True)

    # Select relevant columns only
    df_trf = df_trf[['Tokens', 'NER_Tags']]

    df_dict = df_trf.to_dict('list')

    raw_dataset = Dataset.from_dict(df_dict)

    split = raw_dataset.train_test_split(test_size=0.15, shuffle=True, seed=42)

    checkpoint = 'jonastokoliu/token_classification_finetune'
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)

    label_names = [key for key in label2index.keys()]

    def tokenize_and_align_labels(examples):
        tokenized_inputs = tokenizer(examples["Tokens"], truncation=True, is_split_into_words=True)

        labels = []
        for i, label in enumerate(examples[f"NER_Tags"]):
            word_ids = tokenized_inputs.word_ids(batch_index=i)  # Map tokens to their respective word.
            previous_word_idx = None
            label_ids = []
            for word_idx in word_ids:  # Set the special tokens to -100.
                if word_idx is None:
                    label_ids.append(-100)
                elif word_idx != previous_word_idx:  # Only label the first token of a given word.
                    label_ids.append(label[word_idx])
                else:
                    label_ids.append(-100)
                previous_word_idx = word_idx
            labels.append(label_ids)

        tokenized_inputs["labels"] = labels
        return tokenized_inputs

    tokenized_dataset = split.map(tokenize_and_align_labels, batched=True)

    data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

    seqeval = evaluate.load("seqeval")

    def compute_metrics(p):
        predictions, labels = p
        predictions = np.argmax(predictions, axis=2)

        true_predictions = [
            [label_names[p] for (p, l) in zip(prediction, label) if l != -100]
            for prediction, label in zip(predictions, labels)
        ]
        true_labels = [
            [label_names[l] for (p, l) in zip(prediction, label) if l != -100]
            for prediction, label in zip(predictions, labels)
        ]

        results = seqeval.compute(predictions=true_predictions, references=true_labels)
        return {
            "precision": results["overall_precision"],
            "recall": results["overall_recall"],
            "f1": results["overall_f1"],
            "accuracy": results["overall_accuracy"],
        }

    print("Loading model from pre-trained...")
    model = AutoModelForTokenClassification.from_pretrained(
        checkpoint, num_labels=17, id2label=index2label, label2id=label2index, ignore_mismatched_sizes=True
    )

    training_args = TrainingArguments(
        output_dir="model",
        learning_rate=2e-5,
        per_device_train_batch_size=9,
        per_device_eval_batch_size=6,
        num_train_epochs=3,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        report_to="tensorboard",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["test"],
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,

    )

    print("Starting training...")
    trainer.train()