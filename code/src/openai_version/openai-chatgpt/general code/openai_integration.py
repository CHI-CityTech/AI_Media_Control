# this program will allow users to place an image and have the AI describe the image back to them. later on maniipulate the content.
from openai import OpenAI

#open ai key here
client = OpenAI(
  api_key="API-KEY-HERE" 

)

# Define your assistant's ID
assistant_id = "assistant_id_here"

print("Hello, this is an AI you can chat with. Type 'END' to quit. Enjoy!")

while True:
  user_input = input("You: ") #user input variable

  #checking if user wants to end the program. if so then exit it
  if user_input.strip().upper() == "END":
    print("Thank you for trying out this AI program")
    break
  
  #chat complation code is here
  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
      {"role": "system", "content": "You are a helpful assistant."}, # <-- This is the system message that provides context to the model
      {"role": "user", "content": user_input}
    ]
  )

  # Print AI's response
  print("AI: ", completion['choices'][0]['message']['content'])
