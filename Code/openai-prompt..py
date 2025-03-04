from openai import OpenAI
#making an api call to openai to see if it works. Requires payment of tokens
client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message)