from IPython.display import Image, display
from openai import OpenAI
import base64
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image as PILImage, ImageEnhance

#create an application that will allow users to play with the images from the folder/ ex: find blue - searches through images to find blue
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

# Open file extensions to select images
IMAGE_PATHS = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff;*")])

if not IMAGE_PATHS:
    print("No files selected. Exiting.")
    exit()

# Display selected images for context/content
for image_path in IMAGE_PATHS:
    display(Image(image_path))

# Function to encode images to base64
def encode_image(image_path):
    Image = PILImage.open(image_path)
    Image.show()
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    

# Encode all selected images that the user picks
encoded_images = [encode_image(image_path) for image_path in IMAGE_PATHS]

# Prepare messages to send to the AI, including the encoded images
image_messages = [
    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded_image}"}}
    for encoded_image in encoded_images
]

# Sending to the OpenAI API
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": image_messages}
    ],
)

print(response.choices[0].message.content)
