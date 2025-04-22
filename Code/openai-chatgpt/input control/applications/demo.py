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
app.geometry("850x850")

# scroll setup
main_canvas = tk.Canvas(app)
main_scrollbar = tk.Scrollbar(app, orient="vertical", command=main_canvas.yview)
main_scrollable_frame = tk.Frame(main_canvas)

main_scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )
)

main_canvas.create_window((0, 0), window=main_scrollable_frame, anchor="nw")
main_canvas.configure(yscrollcommand=main_scrollbar.set)

main_canvas.pack(side="left", fill="both", expand=True)
main_scrollbar.pack(side="right", fill="y")

# mousewheel scroll 
def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    main_canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows/Mac
    main_canvas.bind_all("<Button-4>", lambda e: main_canvas.yview_scroll(-1, "units"))  # Linux scroll up
    main_canvas.bind_all("<Button-5>", lambda e: main_canvas.yview_scroll(1, "units"))   # Linux scroll down

# to scroll entire ui
tk.Label(main_scrollable_frame, text="System Instruction for AI:").pack()
system_input = tk.Entry(main_scrollable_frame, width=80)
system_input.pack(pady=5)

tk.Button(main_scrollable_frame, text="Choose Image(s)", command=choose_images).pack(pady=5)
listbox = tk.Listbox(main_scrollable_frame, width=60, height=5)
listbox.pack()

tk.Label(main_scrollable_frame, text="Manipulation:").pack()
action_var = tk.StringVar()
action_menu = ttk.Combobox(main_scrollable_frame, textvariable=action_var, state="readonly")
action_menu["values"] = ["Resize", "Rotate", "Crop", "Brightness", "Contrast", "Grayscale", "Sepia"]
action_menu.current(0)
action_menu.pack()
action_menu.bind("<<ComboboxSelected>>", update_param_fields)

params_frame = tk.Frame(main_scrollable_frame)
params_frame.pack(pady=5)

param1_var = tk.StringVar()
param2_var = tk.StringVar()
crop_vars = [tk.StringVar() for _ in range(4)]

tk.Button(main_scrollable_frame, text="Choose & Manipulation Change", command=apply_manipulation).pack(pady=10)

# Scrollable Image Preview Area
preview_container = tk.Frame(main_scrollable_frame)
preview_container.pack(fill="both", expand=True, pady=10)

canvas = tk.Canvas(preview_container, height=200)
scrollbar = tk.Scrollbar(preview_container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

image_frame = scrollable_frame  # Use this for preview_image

tk.Button(main_scrollable_frame, text="Send to OpenAI AI", command=send_to_openai).pack(pady=5)

tk.Label(main_scrollable_frame, text="Here is OpenAI's Response:").pack()
output_box = tk.Text(main_scrollable_frame, height=8, width=90)
output_box.pack(pady=5)

update_param_fields()
app.mainloop()
