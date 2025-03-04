import tkinter as tk
from tkinter import filedialog
from pythonosc import udp_client

# load the media file into QLab
def load_media():
    media_path = filedialog.askopenfilename(title="Select Media File")
    
    if not media_path:
        return
    
    qlab_ip = "127.0.0.1"  # Change to the actual IP
    qlab_port = 53000

    # OSC client to send messages to QLab
    client = udp_client.SimpleUDPClient(qlab_ip, qlab_port)

    client.send_message("/new", "video")

    cue_number = 1  # can be changed
    client.send_message(f"/cue/{cue_number}/fileTarget", media_path)

    print(f"Loaded media {media_path} into QLab cue {cue_number}.")

# GUI creation parameters
root = tk.Tk()
root.title("Drag & Drop Media Loader")
root.geometry("300x150")

#GUI interface
load_button = tk.Button(root, text="Drag and Drop Media File", command=load_media)
load_button.pack(pady=20)

# Run the Tkinter
root.mainloop()