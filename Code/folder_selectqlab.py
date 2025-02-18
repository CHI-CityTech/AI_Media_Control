import os
from pythonosc import udp_client
from pythonosc import osc_message_builder

# i try to rewrite the python script to control it through an osc to be communicated with a 
# put folder path for images here
folder_path = r'c:\Users\geddi\OneDrive\Desktop\images'

# List all image files in the directory
files_check = os.listdir(folder_path)
image_files = [f for f in files_check if f.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp'))]
image_files.sort()

# OSC client
osc_ip = "127.0.0.1"  
osc_port = 53000     
client = udp_client.SimpleUDPClient(osc_ip, osc_port)

# repeated selections
while True:
    print("\nSelect an image by typing in a number from the following:")
    for idx, image_file in enumerate(image_files, 1):
        print(f"{idx}.) {image_file}")

    try:
        selection = int(input(f"Enter a number between 1 and {len(image_files)}: "))

        if 1 <= selection <= len(image_files):
            chosen_image = image_files[selection - 1]
            print(f"You chose this image: {chosen_image}")

            # OSC message to trigger the cue
            cue_number = 1  # change to actual cue number
            message = osc_message_builder.OscMessageBuilder(address=f"/cue/{cue_number}")
            message.add_arg("GO")  # trigger the cue
            client.send(message.build())

            print(f"Sent OSC message to trigger cue {cue_number} for image: {chosen_image}")

        else:
            print("This is an invalid input.")

        # user to select another image
        continue_selection = input("Would you like to select another image? (y/n): ").lower()
        if continue_selection != 'y':
            print("Thank you!")
            break

    except Exception as e:
        print(f"Error: Please enter a valid number from 1 to {len(image_files)}. {e}")