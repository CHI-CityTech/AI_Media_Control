import os
from pythonosc import udp_client
from pythonosc import osc_message_builder

# Folder path for images/video here
folder_path = r'c:\Users\geddi\OneDrive\Desktop\images'

# List all image/video files in the directory
files_check = os.listdir(folder_path)
image_files = [f for f in files_check if f.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp'))]
image_files.sort()

# OSC client. Change if needed.
osc_ip = "127.0.0.1"  
osc_port = 53000     
client = udp_client.SimpleUDPClient(osc_ip, osc_port)

# Feedback database to store each image that is selected. Show status.
feedback_db = {image: {'correct': 0, 'incorrect': 0} for image in image_files}

# Function for feedback and store in database
def give_feedback(user_input, correct_image):
    if user_input == correct_image:
        feedback_db[user_input]['correct'] += 1  # Increment based on the selected image
        return 1  # Positive feedback for correct 
    else:
        feedback_db[user_input]['incorrect'] += 1  # Decrement based on the selected image
        return -1  # Negative feedback for incorrect

# Function for the AI loop system. Training the AI model
def ai_training_loop():
    ai_score = 0  # Track AI's score based on feedback loop

    while True:
        # Ask the user for the "correct" image.
        print("\nSelect the correct image for the cue.")
        for idx, image_file in enumerate(image_files, 1):
            print(f"{idx}.) {image_file}")

        try:
            # User selects an image
            selection = int(input(f"Enter a number between 1 and {len(image_files)}: "))
            
            if 1 <= selection <= len(image_files):
                chosen_image = image_files[selection - 1]
                print(f"You chose this image: {chosen_image}")

                # Ask if the selection is correct or not
                correct_answer = input(f"Is '{chosen_image}' the correct image? (Enter 1 for Yes or 0 for No): ")
                correct_image = chosen_image if correct_answer == '1' else None  # If '1', it's correct

                # Feedback point system 
                if correct_image:
                    feedback = give_feedback(chosen_image, correct_image)
                    ai_score += feedback
                    print("Correct! AI is receiving positive feedback.")
                else:
                    feedback = give_feedback(chosen_image, correct_image)
                    ai_score += feedback
                    print("Incorrect! AI is receiving negative feedback.")
                
                # Update AI loop (updating the score)
                print(f"AI's current score: {ai_score}")

                # OSC message to trigger the cue
                cue_number = selection  # set cue number to match user selection
                message = osc_message_builder.OscMessageBuilder(address=f"/cue/{cue_number}")
                message.add_arg("GO")  # trigger the cue
                client.send(message.build())  
                print(f"Sent OSC message to trigger cue: {cue_number} , for image: {chosen_image}")

                # Print current feedback database (tp track AI's learning process)
                print("\nCurrent Feedback Database:")
                for image, feedback in feedback_db.items():
                    print(f"{image}: Correct: {feedback['correct']}, Incorrect: {feedback['incorrect']}")

            else:
                print("This input is invalid. Try again, please.")

            # Prompt for user to select another image
            continue_selection = input("Would you like to select another image? (y/n): ").lower()
            if continue_selection != 'y':
                print("Thank you for testing!")
                break

        except Exception as e:
            print(f"Error: Please enter a valid number from 1 to {len(image_files)}. {e}")

# Start AI loop
ai_training_loop()