# here we will be using the local llamafile downloaded from llama.cpp to mimic the openAI server
# Downloaded the model from Hugging Face Meta-Llama-3.1-8B-Instruct.Q8_0.llamafile 
# Did chmod +x Meta-Llama-3.1-8B-Instruct.Q8_0.llamafile
# Then ran the following command:
# ./Meta-Llama-3.1-8B-Instruct.Q8_0.llamafile : This model is up and running on localhost:8080

from openai import OpenAI

client = OpenAI(base_url="http://localhost:8080/v1", api_key="dummy")

response = client.chat.completions.create(
    model="Meta-Llama-3.1-8B-Instruct.Q8_0.llamafile",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
        ]
)

print(response.choices[0].message.content)