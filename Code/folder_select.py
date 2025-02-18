import os
from PIL import Image

# put folder path here
folder_path = r'c:\Users\geddi\OneDrive\Desktop\images'

# list all files
files_check = os.listdir(folder_path)

# image files based on extensions
image_files = [f for f in files_check if f.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp'))] 

image_files.sort()

# allow repeated selections
while True:
    # Print the list of images with index numbers
    print("\nSelect an image by typing in a number. It will select an image from the folder:")
    #idx is index and enumerate returns item in position
    for idx, image_file in enumerate(image_files, 1): 
        print(f"{idx}.) {image_file}")

    try:
        selection = int(input(f"Enter a number between 1 and {len(image_files)}: "))
        
        if 1 <= selection <= len(image_files):
            choosen_image = image_files[selection - 1]
            print(f"You chose this image: {choosen_image}")
            
            # path to the selected image
            image_path = os.path.join(folder_path, choosen_image)
            
            img = Image.open(image_path)
            img.show()
        else:
            print("This is an invalid input.")
        
        # exit loop if user once yser doesnt want to select another image. lower all strings
        continue_selection = input("Would you like to select another image? (y/n): ").lower()
        if continue_selection != 'y':
            print("TThank you!")
            break  
    
    except Exception as e:
        print(f" Error: Please enter a valid number from 1 to {len(image_files)}")

