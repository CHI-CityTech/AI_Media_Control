# this program will allow users to place an image and have the AI describe the image back to them. later on maniipulate the content.
from IPython.display import Image, display, Audio, Markdown
from PIL import Image as PILImage, ImageEnhance
from openai import OpenAI
import base64

#open ai key here
client = OpenAI(
  api_key="api_key_here" 

)

#input the image path here (file)
IMAGE_PATH = "IMAGE_PATH_HERE"

# Preview image for context
display(Image(IMAGE_PATH))

# Open the image file and encode it as a base64 string
def encode_image(image_path):
    Image = PILImage.open(image_path)
    Image.show()
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image(IMAGE_PATH)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Please decribe the image with as much detail as possible."},
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{base64_image}"}
            }
        ]}
    ],
)

print(response.choices[0].message.content)
