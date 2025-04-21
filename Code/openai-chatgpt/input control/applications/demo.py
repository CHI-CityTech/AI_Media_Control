# programmed by Edward Gonzalez (github: egonzalez99)
#below are the python 
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image as PILImage, ImageEnhance, ImageTk
import base64
import numpy as np
from io import BytesIO
from openai import OpenAI

# OpenAI client setup
client = OpenAI(api_key="api_key_here")  # Replace with your key
# assistant's ID here
assistant_id = "assistant_id_here"

# Global variables
selected_images = []
manipulated_images = []

# 1. Function to analyze an image with AI (e.g., using CLIP for image analysis)
def analyze_image_with_ai(image_path):
    try:
        # Open image and prepare for analysis
        with open(image_path, 'rb') as img_file:
            response = client.image.analysis.create(image=img_file)
        return response
    except Exception as e:
        messagebox.showerror("An AI Error", f"Computation Error with image: {str(e)}")
        return None

# 2. Function to suggest manipulations based on AI analysis (brightness, color, etc.)
def ai_edits(image_path):
    analysis_response = analyze_image_with_ai(image_path)  # Use AI model to analyze image
    if analysis_response:
        # Hypothetical response structure from AI (e.g., if analysis contains "dark")
        if 'dark' in analysis_response:
            return "Increase brightness by 20%"
        elif 'sunset' in analysis_response:
            return "Applied filter"
        else:
            return "No edits"
    return "Error with the image"

# 3. Apply Style Transfer (e.g., artistic transformation)
def ai_style(image_path):
    try:
        with open(image_path, 'rb') as img_file:
            response = client.image.style_transfer.create(image=img_file, model="artistic-style")
        return response["resulting_image"]
    except Exception as e:
        messagebox.showerror("An AI Error", f"Error applying style: {str(e)}")
        return None

# 4. Enhance image quality (e.g., noise reduction, sharpness, etc.)
def enhancement(image_path):
    try:
        with open(image_path, 'rb') as img_file:
            response = client.image.enhance.create(image=img_file)
        return response["enhanced_image"]
    except Exception as e:
        messagebox.showerror("An AI Error", f"Error with enhancement: {str(e)}")
        return None
    
# Function to manipulate image
def manipulate_image(image_path, action, params=None):
    image = PILImage.open(image_path)

    if action == "Resize":
        width, height = params
        image = image.resize((width, height))
    elif action == "Rotate":
        angle = params.get("angle", 90)
        image = image.rotate(angle)
    elif action == "Crop":
        left, upper, right, lower = params
        image = image.crop((left, upper, right, lower))
    elif action == "Brightness":
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(params["factor"])
    elif action == "Contrast":
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(params["factor"])
    elif action == "Grayscale":
        image = image.convert("L")
    elif action == "color filter":
        image = np.array(image)
        tr = np.array([0.393, 0.769, 0.189])
        tg = np.array([0.349, 0.686, 0.168])
        tb = np.array([0.272, 0.534, 0.131])
        image = np.dot(image[...,:3], [tr, tg, tb])
        image = np.clip(image, 0, 255).astype(np.uint8)
        image = PILImage.fromarray(image)

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded, image

# UI logic
def choose_images():
    global selected_images
    file_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    if file_paths:
        selected_images = file_paths
        listbox.delete(0, tk.END)
        for path in selected_images:
            listbox.insert(tk.END, path.split("/")[-1])

def update_param_fields(event=None):
    action = action_var.get()
    for widget in params_frame.winfo_children():
        widget.destroy()

    if action == "Resize":
        tk.Label(params_frame, text="Width:").grid(row=0, column=0)
        tk.Entry(params_frame, textvariable=param1_var).grid(row=0, column=1)
        tk.Label(params_frame, text="Height:").grid(row=1, column=0)
        tk.Entry(params_frame, textvariable=param2_var).grid(row=1, column=1)
    elif action == "Rotate":
        tk.Label(params_frame, text="Angle:").grid(row=0, column=0)
        tk.Entry(params_frame, textvariable=param1_var).grid(row=0, column=1)
    elif action == "Crop":
        for i, label in enumerate(["Left", "Top", "Right", "Bottom"]):
            tk.Label(params_frame, text=label + ":").grid(row=i, column=0)
            tk.Entry(params_frame, textvariable=crop_vars[i]).grid(row=i, column=1)
    elif action in ["Brightness", "Contrast"]:
        tk.Label(params_frame, text="Factor (e.g., 1.0):").grid(row=0, column=0)
        tk.Entry(params_frame, textvariable=param1_var).grid(row=0, column=1)

def apply_manipulation():
    global manipulated_images
    manipulated_images = []
    action = action_var.get()

    for path in selected_images:
        if action == "Resize":
            params = (int(param1_var.get()), int(param2_var.get()))
        elif action == "Rotate":
            params = {"angle": int(param1_var.get())}
        elif action == "Crop":
            params = tuple(int(var.get()) for var in crop_vars)
        elif action in ["Brightness", "Contrast"]:
            params = {"factor": float(param1_var.get())}
        else:
            params = None
        encoded, img = manipulate_image(path, action, params)
        manipulated_images.append((encoded, img))
        preview_image(img)

def preview_image(pil_img):
    preview = PILImage.new("RGB", pil_img.size)
    preview.paste(pil_img)
    preview.thumbnail((200, 200))
    img_tk = ImageTk.PhotoImage(preview)
    img_label = tk.Label(image_frame, image=img_tk)
    img_label.image = img_tk
    img_label.pack(padx=5, pady=5)

# system instructions for errors
def send_to_openai():
    if not manipulated_images:
        messagebox.showwarning("Warning", "No images to send.")
        return

    system_instruction = system_input.get()
    if not system_instruction:
        messagebox.showwarning("Warning", "System instruction is required.")
        return

    image_messages = [
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded}"}}
        for encoded, _ in manipulated_images
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": image_messages}
            ],
        )
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, response.choices[0].message.content)
    except Exception as e:
        messagebox.showerror("API Error", str(e))

# UI
app = tk.Tk()
app.title("Image Manipulation + AI")
app.geometry("800x600")

# Instruction input
tk.Label(app, text="System Instruction for AI:").pack()
system_input = tk.Entry(app, width=80)
system_input.pack(pady=5)

# Image selection
tk.Button(app, text="Choose Image(s)", command=choose_images).pack(pady=5)
listbox = tk.Listbox(app, width=60, height=5)
listbox.pack()

# Manipulation selection
tk.Label(app, text="Manipulation:").pack()
action_var = tk.StringVar()
action_menu = ttk.Combobox(app, textvariable=action_var, state="readonly")
action_menu["values"] = ["Resize", "Rotate", "Crop", "Brightness", "Contrast", "Grayscale", "Sepia"]
action_menu.current(0)
action_menu.pack()
action_menu.bind("<<ComboboxSelected>>", update_param_fields)

params_frame = tk.Frame(app)
params_frame.pack(pady=5)

param1_var = tk.StringVar()
param2_var = tk.StringVar()
crop_vars = [tk.StringVar() for _ in range(4)]

# Apply button
tk.Button(app, text="Apply Manipulation Change", command=apply_manipulation).pack(pady=10)

# Preview area
image_frame = tk.Frame(app)
image_frame.pack(pady=10)

# Send to OpenAI
tk.Button(app, text="Send to OpenAI AI", command=send_to_openai).pack(pady=5)

# Output from OpenAI
tk.Label(app, text="Here is OpenAI's Response:").pack()
output_box = tk.Text(app, height=8, width=90)
output_box.pack(pady=5)

update_param_fields()
app.mainloop()
