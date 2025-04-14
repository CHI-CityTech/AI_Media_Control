import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance
import base64
import numpy as np
from io import BytesIO
from openai import OpenAI
import json

# Initialize OpenAI client
client = OpenAI(api_key="api_key_here")
assistant_id = "assistant_id_here"

class ImageSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Media Control Demo")
        self.image_paths = []
        self.thumbnails = []
        self.selected_image_path = None
        self.modified_image = None

        self.setup_ui()

    def setup_ui(self):
        tk.Button(self.root, text="Select Your Image(s)", command=self.select_images).pack(pady=16)

        # Thumbnail viewer
        self.canvas = tk.Canvas(self.root, height=150)
        self.scrollbar = tk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.pack(fill="x")
        self.scrollbar.pack(fill="x")
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Instruction input
        self.instruction_entry = tk.Entry(self.root, width=200)
        self.instruction_entry.pack(pady=16)
        tk.Button(self.root, text="Apply Instruction", command=self.apply_instruction).pack()

        # Modified image preview
        self.preview_label = tk.Label(self.root)
        self.preview_label.pack(pady=10)

    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(title="Select Your Image(s)", filetypes=[("Image Files: ", "*.png;*.jpg;*.jpeg;*.gif")])
        self.display_thumbnails()

    def display_thumbnails(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.thumbnails.clear()
        
        #
        for idx, path in enumerate(self.image_paths):
            img = Image.open(path)
            img.thumbnail((100, 100))
            tk_img = ImageTk.PhotoImage(img)
            self.thumbnails.append(tk_img)

            label = tk.Label(self.frame, image=tk_img, bd=2, relief="groove")
            label.grid(row=0, column=idx, padx=5, pady=5)
            label.bind("<Button-1>", lambda e, p=path: self.select_image(p))
    
    def select_image(self, path):
        self.selected_image_path = path
        print(f"Selected image: {path}")

    def apply_instruction(self):
        if not self.selected_image_path:
            messagebox.showwarning("No Image Selected", "Please select an image first.")
            return

        instruction = self.instruction_entry.get()
        if not instruction.strip():
            messagebox.showwarning("Empty Prompt", "Please enter an instruction.")
            return

        # Convert image to base64
        original_image = Image.open(self.selected_image_path)
        buffered = BytesIO()
        original_image.save(buffered, format="PNG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # Ask OpenAI to interpret the instruction for this application use
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an assistant that helps convert natural language into image manipulation commands. Reply ONLY with a JSON object like: {\"action\": \"grayscale\"} or {\"action\": \"brightness\", \"factor\": 1.5}"},
                    {"role": "user", "content": instruction}
                ]
            )
            parsed = json.loads(response.choices[0].message.content)
            action = parsed.get("action")
            print(f"Action from AI: {parsed}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get instruction: {e}")
            return

        # Apply manipulation to image
        try:
            result = self.manipulate_image(original_image, action, parsed)
            self.show_image(result)
        except Exception as e:
            messagebox.showerror("Error", f"Image manipulation failed: {e}")

    def manipulate_image(self, image, action, params):
        if action == "grayscale":
            image = image.convert("L").convert("RGB")
        elif action == "brightness":
            factor = params.get("factor", 1.0)
            image = ImageEnhance.Brightness(image).enhance(factor)
        elif action == "contrast":
            factor = params.get("factor", 1.0)
            image = ImageEnhance.Contrast(image).enhance(factor)
        return image

    def show_image(self, image):
        image.thumbnail((300, 300))
        self.tk_preview = ImageTk.PhotoImage(image)
        self.preview_label.configure(image=self.tk_preview)
        self.modified_image = image

# Run the application from main
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSelectorApp(root)
    root.mainloop()
