from IPython.display import Image, display, Audio, Markdown 
from openai import OpenAI
import base64
import tkinter as tk
from tkinter import filedialog

# OpenAI key here
client = OpenAI(
  api_key="api_key_here" 
)

# Open file dialog to select image
root = tk.Tk()
root.withdraw()  # Hide the main window
IMAGE_PATH = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])

if not IMAGE_PATH:
    print("No file selected. Exiting.")
    exit()

# Preview image for context
display(Image(IMAGE_PATH))

# Open the image file and encode it as a base64 string
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image(IMAGE_PATH)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Please describe the image with as much detail as possible."},
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{base64_image}"}
            }
        ]}
    ],
)

print(response.choices[0].message.content)
