# programmed by Edward Gonzalez (github: egonzalez99)
#below are the python 
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from openai import OpenAI
import requests, base64
from PIL import Image, ImageTk, ImageOps
from io import BytesIO
from math import ceil, sqrt
import os

# Initialize OpenAI client
client = OpenAI(api_key="api_key_here")  # Replace with your actual API key

assistant_id = "assistant_id_here"
# hold multiple images
edit_base_image_path = ""
edit_second_image_path = ""
edit_image_paths = []

# Display Image from bytes(easier to store and move image information as nums)
def display_image(image_bytes, label):
    img = Image.open(BytesIO(image_bytes)).resize((512, 512))
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk
    
# Image Generation tab and functions here
def generate_image():
    global generated_image_bytes
    prompt = gen_prompt_entry.get()
    if not prompt:
        messagebox.showerror("Error", "Please enter a prompt with what you want done with the image.")
        return
    try:
        response = client.images.generate(
            model="dall-e-2", # openai image model used, careful of api calls
            prompt=prompt,
            n=1,
            size="512x512", 
            response_format="url" 
        )
        image_url = response.data[0].url 
        generated_image_bytes = requests.get(image_url).content  # storing/saving the image       
        display_image(generated_image_bytes, gen_image_label)
        generator_result.config(text="Generator was successful!")
    except Exception as e:
        messagebox.showerror("Error with the generator", str(e))

# saving generated image
def save_generated_image():
    if generated_image_bytes:
        img = Image.open(BytesIO(generated_image_bytes)) # saving image from the generator as this variable
        img.save("image_saved.png") # image saved file, can be changed
        messagebox.showinfo("Saved", "Image saved as 'image_saved.png'")
    else:
        messagebox.showerror("Error", "No image to save.")
# ------------------------------------------------------------------------------------------------------------ 

# Image Editing tab and functions here
def edit_first_image():
    global edit_base_image_path
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff")])
    if path:
        edit_base_image_path = path
        img = Image.open(path).resize((150, 150))  
        img_tk = ImageTk.PhotoImage(img)
        edit_base_label.config(image=img_tk, text="")
        edit_base_label.image = img_tk

def edit_second_image():
    global edit_second_image_path
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff")])
    if path:
        edit_second_image_path = path
        img = Image.open(path).resize((150, 150))  
        img_tk = ImageTk.PhotoImage(img)
        edit_second_label.config(image=img_tk, text="")
        edit_second_label.image = img_tk

from math import ceil, sqrt

def merge_image(image_paths, size=(150, 150), background_color=(255, 255, 255, 0)):
    num_images = len(image_paths)
    if num_images == 0:
        raise ValueError("No images provided to merge.")
    
    # Smart grid size
    if num_images == 1:
        cols, rows = 1, 1
    elif num_images == 2:
        cols, rows = 2, 1
    else:
        cols = 2
        rows = ceil(num_images / 2)  # 2 images per row
    
    # Create a blank canvas
    collage = Image.new("RGBA", (cols * size[0], rows * size[1]), background_color)
    
    # Open and paste each image
    for i, path in enumerate(image_paths):
        img = Image.open(path).resize(size)
        x = (i % cols) * size[0]
        y = (i // cols) * size[1]
        collage.paste(img, (x, y))
    
    output_path = "combined_image.png"
    collage.save(output_path)
    return output_path

def image_editor():
    global image_bytes
    if not edit_base_image_path or not edit_second_image_path:
        messagebox.showerror("Error", "Please select both base and second images to manipulate.")
        return

    prompt = edit_prompt_entry.get()
    if not prompt:
        messagebox.showerror("Error", "Enter your prompt here.")
        return

    try:
        # Merge the selected images (this will auto handle grid size and number of images)
        combined_path = merge_image([edit_base_image_path, edit_second_image_path])

        # Open the combined image
        with open(combined_path, "rb") as image_file:
            result = client.images.edit(
                model="dall-e-2",  # OpenAI image model used
                image=image_file,
                prompt=prompt,  # User input prompt
                response_format="b64_json"
            )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        # Save the edited image locally
        with open("image-edited.png", "wb") as f:
            f.write(image_bytes)

        # Open and show the image using the show() method
        edited_image = Image.open("image-edited.png")
        edited_image.show()  # This will open the image in the default image viewer

        # Display the image in your Tkinter GUI
        display_image(image_bytes, edit_image_label)
        edit_result_label.config(text="Edited image saved as 'image-edited.png'")

    except Exception as e:
        messagebox.showerror("Error with image selected", str(e))
        
def resize_image():
    global edit_base_image_path
    if not edit_base_image_path:
        messagebox.showerror("Error", "Please select an image to resize.")
        return
    
    try:
        width = int(resize_width_entry.get())
        height = int(resize_height_entry.get())
        
        img = Image.open(edit_base_image_path)
        resized_img = img.resize((width, height))
        
        img_tk = ImageTk.PhotoImage(resized_img)
        edit_base_label.config(image=img_tk, text="")
        edit_base_label.image = img_tk
        
        messagebox.showinfo("Success", f"Image resized to {width}x{height}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid width and height.")

def rotate_image():
    global edit_base_image_path
    if not edit_base_image_path:
        messagebox.showerror("Error", "Please select an image to rotate.")
        return

    try:
        angle = int(rotate_angle_entry.get())
        
        img = Image.open(edit_base_image_path)
        rotated_img = img.rotate(angle)
        
        img_tk = ImageTk.PhotoImage(rotated_img)
        edit_base_label.config(image=img_tk, text="")
        edit_base_label.image = img_tk
        
        messagebox.showinfo("Success", f"Image rotated by {angle} degrees")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid rotation angle.")

def apply_grayscale():
    global edit_base_image_path
    if not edit_base_image_path:
        messagebox.showerror("Error", "Please select an image for grayscale.")
        return
    
    img = Image.open(edit_base_image_path)
    grayscale_img = img.convert("L")  # Convert image to grayscale
    
    img_tk = ImageTk.PhotoImage(grayscale_img)
    edit_base_label.config(image=img_tk, text="")
    edit_base_label.image = img_tk

    messagebox.showinfo("Success", "Image converted to grayscale.")

def apply_sepia():
    global edit_base_image_path
    if not edit_base_image_path:
        messagebox.showerror("Error", "Please select an image for sepia filter.")
        return
    
    img = Image.open(edit_base_image_path)
    sepia_img = img.convert("RGB")
    pixels = sepia_img.load()

    for i in range(sepia_img.width):
        for j in range(sepia_img.height):
            r, g, b = sepia_img.getpixel((i, j))
            
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            
            # Apply the sepia filter
            sepia_img.putpixel((i, j), (min(tr, 255), min(tg, 255), min(tb, 255)))

    img_tk = ImageTk.PhotoImage(sepia_img)
    edit_base_label.config(image=img_tk, text="")
    edit_base_label.image = img_tk
    
    messagebox.showinfo("Success", "Sepia filter applied.")
        
        
# saving edited image
def save_edited_image():
    if image_bytes:
        img = Image.open(BytesIO(image_bytes)) # saving image from the edited image as this variable
        img.save("image_saved.png") # image saved file, can be changed
        messagebox.showinfo("Saved", "Image saved as 'image_saved.png'")
    else:
        messagebox.showerror("Error", "No image to save.")
# ------------------------------------------------------------------------------------------------------------   
# Image Mask tab and functions here
def first_image():
    global base_image_path
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff")])
    if path:
        base_image_path = path
        img = Image.open(path).resize((150, 150))  
        img_tk = ImageTk.PhotoImage(img)
        mask_base_label.config(image=img_tk, text="")
        mask_base_label.image = img_tk

def second_image():
    global mask_image_path
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff")])
    if path:
        mask_image_path = path
        img = Image.open(path).resize((150, 150))  
        img_tk = ImageTk.PhotoImage(img)
        mask_second_label.config(image=img_tk, text="")
        mask_second_label.image = img_tk

def apply_mask_edit():
    
    try:
        # Open base and mask images
        base_img = Image.open(base_image_path).convert("RGBA")
        mask_img = Image.open(mask_image_path).convert("L")  # Convert mask to grayscale

        # Resize mask to match base image
        mask_img = mask_img.resize(base_img.size)

        # image 
        overlay_image = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
        binary_mask = mask_img.point(lambda p: 255 if p > 128 else 0)
        overlay_image.putalpha(binary_mask)
        preview_img = Image.alpha_composite(base_img, overlay_image)
        preview_img.save("mask_overlay.png")
        preview_img.show()

        # store images for API call
        base_path = "temp_base.png"
        mask_path = "temp_mask.png"
        base_img.save(base_path, format="PNG")
        mask_img.save(mask_path, format="PNG")

        # Call OpenAI image edit API
        with open(base_path, "rb") as image_file, open(mask_path, "rb") as mask_file:
            result = client.images.edit(
                model="dall-e-2",
                image=image_file,
                mask=mask_file,
                response_format="b64_json"
            )

        image_base64_ = result.data[0].b64_json
        image_bytes_ = base64.b64decode(image_base64_)

        with open("masked_image.png", "wb") as f:
            f.write(image_bytes_)

        display_image(image_bytes_, mask_result_image)
        mask_result_label.config(text="Saved as 'masked_image.png'")

    except Exception as e:
        messagebox.showerror("Error", str(e))

        
# Create the main application window
root = tk.Tk()
root.title("AI Image Generator & Editor")
root.geometry("640x800")

# Create a frame to hold the tab content
tab_frame = tk.Frame(root)
tab_frame.pack(fill="both", expand=True)

# Create a canvas inside the tab frame
canvas = tk.Canvas(tab_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a vertical scrollbar linked to the canvas
scrollbar = tk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas
content_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# Create the notebook (tab container)
tab_control = ttk.Notebook(content_frame)
tab_control.pack(expand=1, fill="both")

# Generator Tab
generate_tab = ttk.Frame(tab_control)
tab_control.add(generate_tab, text='⚙️ 🛠️ Image Generator')

tk.Label(generate_tab, text="This uses two images to generate a new Image with something you want in a background or other instruction").pack(pady=10)

tk.Label(generate_tab, text="Write in the prompt below an image you want generated:").pack(pady=15)
gen_prompt_entry = tk.Entry(generate_tab, width=75)
gen_prompt_entry.pack(pady=15)

tk.Button(generate_tab, text="Generate The Image", command=generate_image).pack(pady=10)

gen_image_label = tk.Label(generate_tab)
gen_image_label.pack(pady=10)

generator_result = tk.Label(generate_tab, text="")
generator_result.pack()

tk.Button(generate_tab, text="Save Your Image", command=save_generated_image).pack(pady=10)

# Edit Tab
edit_tab = ttk.Frame(tab_control)
tab_control.add(edit_tab, text='-ˋˏ✄┈┈┈┈ 🎨 Image Editor')

tk.Label(edit_tab, text="This uses two images to be edited with a prompt. For example: combine the two images with a sunset background").pack(pady=10)

edit_image_path = tk.StringVar()

tk.Button(edit_tab, text="Select First Image", command=edit_first_image).pack(pady=10)
edit_base_label = tk.Label(edit_tab, text="No base image selected yet")
edit_base_label.pack(pady=5)

tk.Button(edit_tab, text="Select Second Image", command=edit_second_image).pack(pady=10)
edit_second_label = tk.Label(edit_tab, text="No second image selected yet")
edit_second_label.pack(pady=10)

tk.Label(edit_tab, text="Write in the prompt an instruction for the images to be edited:").pack(pady=10)
edit_prompt_entry = tk.Entry(edit_tab, width=60)
edit_prompt_entry.pack(pady=10)
tk.Button(edit_tab, text="Edit Both Images", command=image_editor).pack(pady=15)

tk.Label(edit_tab, text="Resize the image:").pack(pady=10)
resize_width_entry = tk.Entry(edit_tab, width=20)
resize_width_entry.pack(pady=5)
resize_height_entry = tk.Entry(edit_tab, width=20)
resize_height_entry.pack(pady=5)
tk.Button(edit_tab, text="Resize Image", command=resize_image).pack(pady=10)

tk.Label(edit_tab, text="Rotate the image (in degrees):").pack(pady=10)
rotate_angle_entry = tk.Entry(edit_tab, width=20)
rotate_angle_entry.pack(pady=5)
tk.Button(edit_tab, text="Rotate Image", command=rotate_image).pack(pady=10)

tk.Button(edit_tab, text="Apply Grayscale Filter", command=apply_grayscale).pack(pady=10)
tk.Button(edit_tab, text="Apply Sepia Filter", command=apply_sepia).pack(pady=10)

edit_image_label = tk.Label(edit_tab)
edit_image_label.pack(pady=15)

edit_result_label = tk.Label(edit_tab, text="")
edit_result_label.pack()

tk.Button(edit_tab, text="Save Edited Image", command=save_edited_image).pack(pady=15)

# Mask Tab
mask_tab = ttk.Frame(tab_control)
tab_control.add(mask_tab, text='🖌️ 🎭 Image Layering')

tk.Label(mask_tab, text="This uses two images to layer one image on top of another to generate a new image.").pack(pady=10)

tk.Button(mask_tab, text="Select Your First Image", command=first_image).pack(pady=20)
mask_base_label = tk.Label(mask_tab, text="No base image selected")
mask_base_label.pack(pady=15)

tk.Button(mask_tab, text="Select Your Second Image", command=second_image).pack(pady=20)
mask_second_label = tk.Label(mask_tab, text="No mask image selected")
mask_second_label.pack(pady=20)

tk.Button(mask_tab, text="Apply Your Layering for Both IMages", command=apply_mask_edit).pack(pady=20)

mask_result_image = tk.Label(mask_tab)
mask_result_image.pack(pady=10)

mask_result_label = tk.Label(mask_tab, text="")
mask_result_label.pack()

# Function to update the scrollregion whenever necessary
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

content_frame.bind("<Configure>", on_frame_configure)

# Function for mouse wheel scrolling
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Bind mouse wheel to canvas
canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Start the Tkinter event loop
root.mainloop()

