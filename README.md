# Project Overview

This project blends technical research, artistic expression, and software development to explore the intersection of artificial intelligence and live entertainment systems. It demonstrates how AI-driven automation can be harmoniously integrated with performance technologies to redefine the boundaries of modern theater, interactive media, and immersive storytelling. By merging creativity with computation, the project highlights innovative pathways for transforming contemporary stagecraft and digital production environments.

This Python application provides a graphical user interface (GUI) for generating, editing, and manipulating images using OpenAI's DALL·E/ChatGPT model:

1. Image Generation – Users can input a text prompt to generate an AI-created image.

2. Image Editing – Users can combine and modify two selected images using text prompts, apply filters (grayscale, sepia), resize, and rotate images.
   
3. Image Masking – Users can layer one image over another using a mask, enabling creative overlays and targeted edits.

# 🖼️📦 AI-with-QLab-using-an-OSC Template
Combining Generative AI with QLab Using Open Sound Control 

#Application UI Concept

---
| Instruction: [ "Make it sepia and brighter" ]|
|                 [Apply]                      |

---
|   [Image Selected 1]    [Image Selected 2]   |
|               (Click to select)              |
|             [ Select Images Button ]         |

---
|       [Modified Image Previews Here]         |

---

Here is a complete **installation and setup guide** for the Python script you provided, titled:

# 🖼️ AI Image Generator & Editor — Installation Guide [Under Demo > Main Demo]

---

# 👥 Contributors / Contact
* **Edward Gonzalez** – Developer, Designer & AI | [GitHub Page: @egonzalez99](https://github.com/egonzalez99)

* 📧 Email: [bryangonzalez040@gmail.com](mailto:bryangonzalez040@gmail.com)

---

## ✅ Requirements

This Python application uses the **OpenAI API**, `tkinter` for GUI, and several image processing libraries. It provides image generation, editing, and layering functionalities using `DALL·E 2`.

---

## 📦 Step 1: Install Python

Ensure that **Python 3.8 or newer** is installed in your system.

To check:

  ```Terminal
  python --version
  ```

If it's not installed, download it from: [https://www.python.org/downloads](https://www.python.org/downloads)

## Step 1 (For Visual Studio Code Users): 

You can use Visual Studio Code as your IDE: [https://code.visualstudio.com/download](https://code.visualstudio.com/download)

Here is a tutorial in Visual Studio Code's wensite on setting up Python once downloaded (Can Be Followed Along With Steps 1-3): [https://code.visualstudio.com/docs/languages/python](https://code.visualstudio.com/docs/languages/python)

* Install the Python extension in VS Code (it helps with environment management, syntax, etc.)

---

## 📁 Step 2: Set Up a Project Folder 

* Create and navigate to a new folder OR Use explorer from your IDE:

  ```Terminal
  mkdir ai-image-editor
  cd ai-image-editor
  ```

1. 📄 Save the AI Media Control script as a file called [For Example]:  `app.py`.
   
2. Paste the AI Media Control script/code into it your file: [https://github.com/CHI-CityTech/AI_Media_Control/blob/main/applications/main_demo/demo.py](https://github.com/CHI-CityTech/AI_Media_Control/blob/main/applications/main_demo/demo.py) 

## Step 2 (For Visual Studio Code Users): 

1. Open VS Code

2. Press Ctrl + Shift + P (or Cmd + Shift + P on macOS) → search for "New Folder" or just:

  * Open a terminal: Ctrl + ~
  * Run:

    ```Terminal
    Copy
    Edit
    mkdir ai-image-editor
    cd ai-image-editor
    ```

3. Go to File > Open Folder... Select and open the new folder you just created for this project.

4. 📄 Add the Script by the follwoing: 
  * In the Explorer panel, right-click the folder → click "New File"
  
  * Name it (optional, but can be named however you want. Must add .py at the end though): app.py
  
  * Paste the AI Media Control script/code into it your file: [https://github.com/CHI-CityTech/AI_Media_Control/blob/main/applications/main_demo/demo.py](https://github.com/CHI-CityTech/AI_Media_Control/blob/main/applications/main_demo/demo.py) 

---

## 📥 Step 3: Create and Activate a Virtual Environment (Optional but Recommended)

  ```Terminal
  python -m venv venv
  # Windows
  venv\Scripts\activate
  # macOS/Linux
  source venv/bin/activate
  ```

## Step 3 (For Visual Studio Code Users): 
1. Open the integrated terminal (Ctrl + ~)

2. Run:

  ```Terminal
  Copy
  Edit
  python -m venv venv
  ```
3. Activate it:

  Windows Users:
  
  ```bash
  Copy
  Edit
  venv\Scripts\activate
  ```
  macOS/Linux Users:

  ```bash/Terminal
  Copy
  Edit
  source venv/bin/activate
  ```
* You’ll see (venv) as folders in your folders on the left side and venv in your bottom right corner.
  
---

## 🧩 Step 4: Install Required Packages

Run the following to install the dependencies:

```Terminal
pip install openai pillow requests
```

> ⚠️ `tkinter` comes pre-installed with standard Python on most systems. If it’s missing:

* Ubuntu/Debian (For Linux User): `sudo apt-get install python3-tk`
* macOS w/ Homebrew (For MacOS Users): `brew install python-tk`

---

## 🔑 Step 5: Set Your OpenAI API Key

* 🔒 **warning** Note

* Please Do **not** share your OpenAI API key publicly. Never share the key openly and save the key somewhere. Consider using environment variables - `.env`/`python -m venv venv` file in running the app.

Inside your filename `app.py` replace this line:

```python
client = OpenAI(api_key="api_key_here")
```

with your own OpenAI API key. You can obtain one from here: [https://platform.openai.com/account/api-keys](https://platform.openai.com/api-keys)

```python
client = OpenAI(api_key="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
```

You can also set your assistant ID if applicable: You can obtain one from here (Optional): [https://platform.openai.com/assistants](https://platform.openai.com/assistants) 
> If you’re only using image generation/editing, the assistant ID may not be needed. But it can enhance your images with descriptions and instructions of what you want.
```python
assistant_id = "your_assistant_id_here"
```

* 🔒 **warning** Track your API Key usage to see how much you're using and have to pay. Here's OpenAI usage link: [https://platform.openai.com/usage](https://platform.openai.com/usage)
  
---

## ▶️ Step 6: Run the Application

From your terminal OR Play the run button [▶️] from your IDE (Visual Studio Code):

```Terminal
python app.py
```

You’ll see a GUI window titled **“AI Image Generator & Editor”** with three tabs:

* **Image Generator**
* **Image Editor**
* **Image Layering**

---

## 📚 Features

### 1. 🛠️ Image Generator

* Enter a prompt to generate an image with DALL·E 2.
* Save the generated image.

### 2. 🎨 Image Editor

* Upload two images.
* Enter a prompt to combine/edit them via DALL·E.
* Additional tools: resize, rotate, grayscale, sepia.

### 3. 🎭 Image Layering (Mask)

* Use a base image and a mask image.
* Combines them using DALL·E’s mask API.
* Save or preview the result.

---

## 📝 Tips

* Use descriptive prompts for better results (e.g., *"Combine both images with a beach background at sunset."*).
* Ensure both images are valid formats: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff`.
* Different resolution sizes could cause problems when running the application.

---

## ❓ Troubleshooting

| Problem                  | Solution                                                                                       |
| ------------------------ | ---------------------------------------------------------------------------------------------- |
| `ModuleNotFoundError`    | Ensure all packages are installed: `pip install openai pillow requests`                        |
| App crashes with Tkinter | Install GUI dependencies: `sudo apt install python3-tk`                                        |
| API limit errors         | Check your OpenAI usage quota at [OpenAI Dashboard](https://platform.openai.com/account/usage) |

---

*Thank You For Our App! ☺️✨*
