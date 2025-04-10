from IPython.display import Image, display
from openai import OpenAI
import base64
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image as PILImage, ImageEnhance #image to be manipulated
import numpy as np
import pickle  # use to serialize python objects
import json  # save file as json
from io import BytesIO
import os # for image path to be save

# OpenAI key here
client = OpenAI(api_key="api_key_here")

# assistant's ID here
assistant_id = "assistant_id_here"

# creating a GUI window to enter system instructions to OPENAI assistant
root = tk.Tk()
root.withdraw()  # hides the main window
system_instruction = simpledialog.askstring("System Instruction", "Enter system instructions for the AI:")

if not system_instruction:
    print("No instructions provided. Exiting.")
    exit()

# here are the file extensions to select images from
IMAGE_PATHS = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff;*")])

if not IMAGE_PATHS:
    print("No files selected. Exiting.")
    exit()

# Function to manipulate images (resize, rotate, crop, change colors)
def manipulate_image(image_path, action, params=None):
    # Open the image using PIL
    image = PILImage.open(image_path)
    
    # Image manipulation actions
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
        image = enhancer.enhance(params["factor"])  # greater than 1.0 is brightness. while less than 1.0 is darkness
    elif action == "contrast":
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(params["factor"])  # greater than 1.0 is more contrast. while less than 1.0 is less contrast
    elif action == "grayscale":
        image = image.convert("L")
    elif action == "sepia":
        # Apply sepia filter
        image = np.array(image)
        tr = np.array([0.393, 0.769, 0.189])  # Red filter
        tg = np.array([0.349, 0.686, 0.168])  # Green filter
        tb = np.array([0.272, 0.534, 0.131])  # Blue filter
        
        # Apply sepia filter
        image = np.dot(image[...,:3], [tr, tg, tb])
        image = np.clip(image, 0, 255).astype(np.uint8)
        image = PILImage.fromarray(image)
    
    # Save the modified image in a BytesIO object to return as base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    buffered.seek(0)
    return base64.b64encode(buffered.read()).decode("utf-8"), image

# Ask the user for the image manipulation action
action = simpledialog.askstring("Action", "Please enter the image manipulation option that you would like to apply: (resize, rotate, crop, brightness, contrast, grayscale, sepia):").lower()

params = None
if action in ["resize", "rotate", "crop"]:
    if action == "resize":
        # Ask for new dimensions
        width = simpledialog.askinteger("Width", "Enter width:")
        height = simpledialog.askinteger("Height", "Enter height:")
        params = (width, height)
    elif action == "rotate":
        # Ask for the rotation angle
        angle = simpledialog.askinteger("Angle", "Enter angle to rotate:")
        params = {"angle": angle}
    elif action == "crop":
        # Ask for crop coordinates (left, upper, right, lower)
        left = simpledialog.askinteger("Left", "Enter left coordinate:")
        upper = simpledialog.askinteger("Upper", "Enter upper coordinate:")
        right = simpledialog.askinteger("Right", "Enter right coordinate:")
        lower = simpledialog.askinteger("Lower", "Enter lower coordinate:")
        params = (left, upper, right, lower)
elif action == "brightness":
    # Ask for brightness factor
    factor = simpledialog.askfloat("Brightness", "Enter brightness factor (e.g., 1.0 for original, >1 for brighter):")
    params = {"factor": factor}
elif action == "contrast":
    # Ask for contrast factor
    factor = simpledialog.askfloat("Contrast", "Enter contrast factor (e.g., 1.0 for original, >1 for more contrast):")
    params = {"factor": factor}
elif action == "grayscale":
    params = None  # No parameter needed
elif action == "sepia":
    params = None  # No parameter needed

# Process and manipulate the selected images
manipulated_images = [
    manipulate_image(image_path, action, params)
    for image_path in IMAGE_PATHS
]

# Display the manipulated images
for encoded_image, image in manipulated_images:
    image.show()

# Save the manipulated image and preserve the data
def save_image_as_data(image, original_image_path):
    # Extract the file extension (ex: .png, .jpg)
    file_extension = os.path.splitext(original_image_path)[1].lower() 

    # output path will be shown
    os.makedirs("output_images", exist_ok=True)

    # Set the file path to save the image with user submitted extension file
    filename = f"manipulated_image{file_extension}"
    output_path = os.path.join("output_images", filename)

    # Save the image in the original format
    image.save(output_path, format=file_extension[1:].upper()) 

    # Return the file path of the saved image
    return output_path

# Save the manipulated images to file paths
file_paths = []
for i, (encoded_image, image_path) in enumerate(zip(manipulated_images, IMAGE_PATHS)):
    saved_path = save_image_as_data(image, image_path)  # using the image directory path
    file_paths.append(saved_path)

# Send the manipulated images to OpenAI API (using base64)
image_messages = [
    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded_image}"}}
    for encoded_image, _ in manipulated_images
]

# sends the text messages to the OpenAI API. Analyze user and system input data
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": image_messages}
    ],
)

print(response.choices[0].message.content)

save_option = simpledialog.askstring("Save", "Do you want to save your preferences in a file? (YES/NO)").lower()

if save_option == "yes":
    # Save user preferences and image manipulation settings
    preferences = {
        "system_instruction": system_instruction,
        "image_manipulation": {
            "action": action,
            "params": params,
            "image_file_paths": file_paths  # Save the file path here
        }
    }

    # Save preferences/data as config file
    with open("config.json", "w") as config_file:
        json.dump(preferences, config_file, indent=4)
    
    # Save image(s) as a serialized file
    with open("manipulated_images.pkl", "wb") as pkl_file:
        pickle.dump(manipulated_images, pkl_file)
    
    print("Your Preferences and image(s) have been saved.")

else:
    print("Your data will not be saved.")
