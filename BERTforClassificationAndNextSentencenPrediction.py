from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load pre-trained BERT tokenizer and model (for sentiment analysis)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)  # 2 labels: positive/negative

# Example sentence
sentence = "The cat sat on the mat liking the milk."

# Step 1: Tokenize the sentence
inputs = tokenizer(sentence, return_tensors="pt")  # returns PyTorch tensors

print("Token IDs:", inputs['input_ids'])
print("Tokens:", tokenizer.convert_ids_to_tokens(inputs['input_ids'][0]))

# Step 2: Pass tokens through BERT model
outputs = model(**inputs)

# Step 3: Get logits (raw predictions before softmax)
logits = outputs.logits

# Step 4: Convert logits to probabilities
probabilities = torch.softmax(logits, dim=1)

print("Probabilities:", probabilities.detach().numpy())

# Step 5: Predicted class
predicted_class = torch.argmax(probabilities, dim=1).item()
print("Predicted class:", predicted_class)

from transformers import BertTokenizer, BertForNextSentencePrediction
import torch

# Load pre-trained BERT NSP model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForNextSentencePrediction.from_pretrained('bert-base-uncased')

# Sentences for NSP
sentence_a = "The cat sat on the mat."
sentence_b = "It purred softly."

# Tokenize and encode as required for NSP
encoding = tokenizer(sentence_a, sentence_b, return_tensors='pt')

print("Token IDs:", encoding['input_ids'])
print("Tokens:", tokenizer.convert_ids_to_tokens(encoding['input_ids'][0]))

# Pass through BERT NSP model
outputs = model(**encoding)
logits = outputs.logits

# Apply softmax to get probabilities
probs = torch.softmax(logits, dim=1)
print("Probabilities (IsNext, NotNext):", probs.detach().numpy())

# Get prediction: 0 = IsNext, 1 = NotNext
prediction = torch.argmax(probs, dim=1).item()
if prediction == 0:
    print("Prediction: Sentence B is the next sentence after Sentence A (IsNext).")
else:
    print("Prediction: Sentence B is NOT the next sentence after Sentence A (NotNext).")
