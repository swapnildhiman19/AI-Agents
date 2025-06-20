from transformers import pipeline
#transformers are from Hugging Face, a library for natural language processing (NLP) tasks

#Since Bert is pre-trained model, bert-base-uncased is a pre-trained BERT model. It’s trained on a huge amount of text to understand English, but not for any specific task (like sentiment analysis).
#When you use pipeline("sentiment-analysis", model="bert-base-uncased"), Hugging Face tries to use the model for sentiment analysis, but since the model’s classification head is not trained for this, it gives random or default results.
#The labels LABEL_0 and LABEL_1 are just generic placeholders, not “positive” or “negative”.
#classifier = pipeline("sentiment-analysis", model="bert-base-uncased", tokenizer="bert-base-uncased")

classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


sentences = ["I love using BERT for Natural Language Processing tasks.","I am not a fan of waiting in the long lines."]
results = classifier(sentences)

for i, sentence in enumerate(sentences):
    print(f"Sentence: {sentence}")
    print(f"Prediction: {results[i]['label']}, Score: {results[i]['score']:.4f}")