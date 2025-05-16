import openai
import osc  # replace with the actual OSC library (e.g., python-osc)

openai.api_key = "API KEY"

client = osc.Client("127.0.0.1", 53000)  # IP address and port for QLab

# process and handle the generated text for QLab
def getTextGenerator(address, args):
    textGenerator = args[0] 
    print("Here's your text message: ", textGenerator)
    
    # Check for 'start cue' in the generated text
    if "start cue" in textGenerator:
        handleCue = textGenerator.split()  
        # Extract cue number and send the OSC command to QLab
        if "cue" in handleCue:
            cue_number = handleCue[handleCue.index("cue") + 1]
            client.send_message(f"/cue/{cue_number}/start", [])

# This function generates text using OpenAI and sends it via OSC
def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=prompt,
        max_tokens=1000,  
        n=1,
        stop=None,
        temperature=0.0  # Low temperature for less randomness
    )
    
    # Extract the generated text
    generated_text = response.choices[0].text
    # Send generated text as an OSC message
    client.send_message("/text_generated", generated_text)

# OSC handlers for incoming messages
client.add_msg_handler("/generate_text", generate_text)  # Trigger text generation
client.add_msg_handler("/text_generated", getTextGenerator)  # Handle generated text

client.serve_forever()