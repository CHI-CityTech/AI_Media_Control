from IPython.display import Image, display
from openai import OpenAI
import base64
import tkinter as tk
from tkinter import filedialog, simpledialog

# OpenAI key here
client = OpenAI(
    api_key="api_key_here"
)

# assistant's ID here
assistant_id = "assistant_id_here"

# Create a GUI window to enter system instructions here
root = tk.Tk()
root.withdraw()  # Hides the main window
system_instruction = simpledialog.askstring("System Instruction", "Enter system instructions for the AI:")

if not system_instruction:
    print("No instructions provided. Exiting.")
    exit()

# Open file extensions to select image
IMAGE_PATH = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])

if not IMAGE_PATH:
    print("No file selected. Exiting.")
    exit()

#Image to show AI for context/content
display(Image(IMAGE_PATH))

# Open the image file and encode it as a base64 string
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image(IMAGE_PATH)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_instruction}, #AI role and instructions are here to be call from OpenAI api
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{base64_image}"}  #the users info and image bath is here to be analyze
            }
        ]}
    ],
)

print(response.choices[0].message.content)