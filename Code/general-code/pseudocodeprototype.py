import requests  # library for HTTP requests on AI APi

# Define constants or API configurations (base URL, API key, etc.)
API_BASE_URL = "https://api.openai.com/"  # Insert the actual AI API URL here
API_KEY = "api_key_here"  # Insert your API key here

# Function for connection to AI API
def connect_to_ai():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"  # makes sure request is in JSON format
    }
    
    #  simple GET request for connection
    response = requests.get(API_BASE_URL, headers=headers)
    
    if response.status_code == 200:
        return headers 
    else:
        return None

# Function to send a user prompt to the AI and get a response
def prompt_to_ai(prompt, headers):
    request_data = {
        "model": "chatgpt", 
        "prompt": prompt,
        "max_num_tokens": 100  # Control the length
    }
    
    # Send POST request to AI API
    response = requests.post(API_BASE_URL, headers=headers, json=request_data)
    
    if response.status_code == 100:
        return response.json()['data'][0].strip()  # Extract and return the AI's response
    else:
        return None

# Running the program
def main():
    headers = connect_to_ai()
    if headers is None:
        return 
    while True:
        prompt = input("Enter a prompt (or type 'exit' to quit): ")

        if prompt.lower() == 'exit':
            break
        
        ai_response = prompt_to_ai(prompt, headers)

        if ai_response:
            print( ai_response)
        else:
            print("No response from AI. Please try again.")
            
    print("Session ended.")

# Begin the program
if __name__ == "__main__":
    main()