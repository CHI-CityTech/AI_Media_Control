from IPython.display import Image as IPyImage, display
from openai import OpenAI
import base64
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image as PILImage, ImageEnhance
import numpy as np
from io import BytesIO

# OpenAI client setup
client = OpenAI(
    api_key="api_key_here"  # Replace with your actual key
)

# Assistant ID (if needed)
assistant_id = "assistant_id_here"

# GUI for system instruction
root = tk.Tk()
root.withdraw()
system_instruction = simpledialog.askstring("System Instruction", "Enter system instructions for the AI:")

if not system_instruction:
    print("No instructions provided. Exiting.")
    exit()

# File picker
IMAGE_PATHS = filedialog.askopenfilenames(
    title="Select Images",
    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff;*")]
)

if not IMAGE_PATHS:
    print("No files selected. Exiting.")
    exit()

# Ask user for manipulation type
action = simpledialog.askstring(
    "Action",
    "Enter manipulation type (resize, rotate, crop, brightness, contrast, grayscale, sepia):"
)

if not action:
    print("No action selected. Exiting.")
    exit()

action = action.lower()
params = None

# Ask for manipulation parameters
if action == "resize":
    width = simpledialog.askinteger("Width", "Enter width:")
    height = simpledialog.askinteger("Height", "Enter height:")
    params = (width, height)
elif action == "rotate":
    angle = simpledialog.askinteger("Angle", "Enter angle to rotate:")
    params = {"angle": angle}
elif action == "crop":
    left = simpledialog.askinteger("Left", "Enter left coordinate:")
    upper = simpledialog.askinteger("Upper", "Enter upper coordinate:")
    right = simpledialog.askinteger("Right", "Enter right coordinate:")
    lower = simpledialog.askinteger("Lower", "Enter lower coordinate:")
    params = (left, upper, right, lower)
elif action in ["brightness", "contrast"]:
    factor = simpledialog.askfloat("Factor", f"Enter {action} factor (e.g., 1.0 for original):")
    params = {"factor": factor}

# Function to manipulate and encode image
def manipulate_image(image_path, action, params=None):
    image = PILImage.open(image_path)

    if action == "resize":
        width, height = params
        image = image.resize((width, height))
    elif action == "rotate":
        angle = params.get("angle", 90)
        image = image.rotate(angle)
    elif action == "crop":
        left, upper, right, lower = params
        image = image.crop((left, upper, right, lower))
    elif action == "brightness":
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(params["factor"])
    elif action == "contrast":
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(params["factor"])
    elif action == "grayscale":
        image = image.convert("L")
    elif action == "sepia":
        image = np.array(image)
        tr = np.array([0.393, 0.769, 0.189])
        tg = np.array([0.349, 0.686, 0.168])
        tb = np.array([0.272, 0.534, 0.131])
        image = np.dot(image[...,:3], [tr, tg, tb])
        image = np.clip(image, 0, 255).astype(np.uint8)
        image = PILImage.fromarray(image)

    # Encode to base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    buffered.seek(0)
    encoded = base64.b64encode(buffered.read()).decode("utf-8")
    return encoded, image

# Apply manipulation and show images
manipulated_images = [
    manipulate_image(path, action, params)
    for path in IMAGE_PATHS
]

for encoded_img, img in manipulated_images:
    img.show()
    display(IPyImage(data=img.tobytes()))

# Prepare messages for OpenAI
image_messages = [
    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded}"}}
    for encoded, _ in manipulated_images
]

# Send to OpenAI
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": image_messages}
    ],
)

print(response.choices[0].message.content)
