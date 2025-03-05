from openai import OpenAI
import os

#making an api call to openai to see if it works
client = OpenAI(
  api_key=os.getenv("API_KEY_HERE")
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message)