import tiktoken

# Load the encoding used by GPT-3.5 or GPT-4
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

# Sample paragraph
paragraph = "Artificial intelligence is powerful."

# Encode the paragraph into tokens (IDs)
tokens = encoding.encode(paragraph)

# Get string version of each token
token_strings = [encoding.decode([t]) for t in tokens]

# tokens is a list of token IDs (integers) produced by the tokenizer.
# encoding.decode([t]) takes a single token ID (as a list with one element) and decodes it back to its string representation.
# The list comprehension [encoding.decode([t]) for t in tokens] loops through each token ID in tokens and decodes it, creating a new list (token_strings) where each element is the string version of the corresponding token.


# Print results
print("Original Text:", paragraph)
print("\nTokenized Output:")
for token_id, token_str in zip(tokens, token_strings):
    print(f"{token_id}: '{token_str}'")

# Decode back to check correctness
decoded = encoding.decode(tokens)
print("\nDecoded Text:", decoded)


# Original Text: Artificial intelligence is powerful.

# Tokenized Output:
# 9470: 'Art'
# 16895: 'ificial'
# 11478: ' intelligence'
# 374: ' is'
# 8147: ' powerful'
# 13: '.'