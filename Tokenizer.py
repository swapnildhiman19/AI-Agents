import tiktoken

# Load the encoding used by GPT-3.5 or GPT-4
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

# Sample paragraph
paragraph = "Artificial intelligence is powerful."

# Encode the paragraph into tokens (IDs)
tokens = encoding.encode(paragraph)

# Get string version of each token
token_strings = [encoding.decode([t]) for t in tokens]

# Print results
print("Original Text:", paragraph)
print("\nTokenized Output:")
for token_id, token_str in zip(tokens, token_strings):
    print(f"{token_id}: '{token_str}'")

# Decode back to check correctness
decoded = encoding.decode(tokens)
print("\nDecoded Text:", decoded)