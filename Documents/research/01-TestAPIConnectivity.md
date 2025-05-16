
# 📌 Research Activity: Testing Initial ChatGPT-Python Connectivity

## 📝 Objective  
To establish a **basic API connection** between a Python script and **ChatGPT (OpenAI API)**.  
The script should:  
1. Accept **user input (a prompt)** from the terminal.  
2. Send the input as a **request** to OpenAI's API.  
3. Receive **ChatGPT's response** and display it in the terminal.  

---

## ⚙️ Setup Instructions  

### 1️⃣ Install Required Dependencies  
Ensure Python (≥ 3.7) is installed. Then, install `openai` via pip:  

```sh
pip install openai
```

### 2️⃣ Set Up API Key  
Obtain an **OpenAI API Key** from [OpenAI's API portal](https://platform.openai.com/signup/).  

Export it as an environment variable (recommended):  

```sh
export OPENAI_API_KEY="your-api-key-here"
```

Alternatively, store it **inside the script** (not recommended for security reasons).  

---

## 💻 Python Script: Simple Terminal-Based Chat with ChatGPT  

```python
import openai
import os

# Load API Key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Set it as an environment variable.")

def chat_with_gpt(prompt):
    """ Sends a prompt to OpenAI API and returns the response """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" if needed
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# Interactive Terminal Loop
print("🔹 ChatGPT Terminal Interface - Type 'exit' to quit 🔹")
while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        print("Exiting Chat. Goodbye! 👋")
        break
    response = chat_with_gpt(user_input)
    print(f"ChatGPT: {response}")
```

---

## 📊 Expected Output  
### When running the script:  
```sh
$ python chat_test.py
🔹 ChatGPT Terminal Interface - Type 'exit' to quit 🔹

You: What is the capital of France?
ChatGPT: The capital of France is Paris.

You: Who developed the theory of relativity?
ChatGPT: The theory of relativity was developed by Albert Einstein.

You: exit
Exiting Chat. Goodbye! 👋
```

---

## 🛠️ Research Evaluation Criteria  
✅ **Does the script connect successfully to OpenAI’s API?**  
✅ **Does it correctly send a user prompt and retrieve a response?**  
✅ **Does it handle basic errors (e.g., no API key, bad response)?**  
✅ **Does the terminal display responses clearly?**  

### 🔍 Next Steps (After Success)  
- **Expand functionality** to send AI responses via **OSC to QLab**.  
- **Improve formatting** (e.g., add timestamps, structured output).  
- **Test latency & optimize** for real-time interaction.  

---

This **research activity provides a functional baseline** for OpenAI API integration.  
Let me know if you'd like to **modify anything before testing!** 🚀


---

### **✅ Key Markdown Considerations:**
- **Code blocks** (`sh`, `python`) remain properly formatted.  
- **Lists and headings** are structured to avoid **Markdown rendering issues**.  
- **Inline emphasis (`**bold**`, `_italic_`)** enhances clarity.  
- **Internal links** (e.g., OpenAI portal) are properly formatted.  

This version **ensures compatibility** for **GitHub, Notion, and other markdown platforms**. 🚀  
Let me know if you'd like any refinements!
