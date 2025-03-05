# Set your OpenAI API key
from openai import OpenAI
# send a file of a picture and let it describe what it is back to me 
client = OpenAI(
  api_key="API_KEY_HERE"
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  store=True,
  messages=[
    {"role": "system", "content": "You are a helpful assistant. Help me with my math homework!"}, # <-- This is the system message that provides context to the model
    {"role": "user", "content": "Hello! Could you solve 2+2?"}
  ]
)

print(completion.choices[0].message);
