import ollama

# Specify the model name
model_name = "gemma3:1b"

# Define the prompt
prompt = "What is the capital of France?"

# Send the prompt to the model and get the response
answer = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])
answer_text = answer["message"]["content"]

# Print the response
print(answer_text)