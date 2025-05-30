# AI Media Control System (AIMCoS) – Engineering Specification (v0.1)

## Overview
The AI Media Control System (AIMCoS) enables real-time audience interaction by selecting and displaying curated images in response to spoken words. The system uses AI (ChatGPT) to associate images with semantically relevant concepts and allows for responsive, dynamic visual composition. This document outlines the architecture in two distinct phases:

1. **Image Preprocessing and Curation (AIMCoS-Curator)**
2. **Real-Time Display and Interaction (AIMCoS-Display)**

> _Note: This document describes a **speculative prototype** and is open to future UX and system design revisions._

---

## Part I – AIMCoS-Curator

### Purpose
Prepares a dataset linking curated images with AI-generated semantic responses, stored for later real-time access.

### Inputs
- Folder of curated images (e.g., `.jpg`, `.png`)
- GPT API Key and connection credentials

### Outputs
- Image-Response JSON/CSV file (data map)
- Config file (preferences for runtime behavior)

### Workflow

1. **Image Folder Ingestion**
   - Recursively scan and index all images in a user-specified folder.
   - Assign unique IDs or filenames as keys.

2. **AI Description Generation**
   - For each image:
     - Use the OpenAI API (or local model) to generate a description based on the image filename or image contents.
     - Suggested prompt:  
       `"Describe this image in a way that captures the key emotional, visual, or conceptual themes."`

3. **Data Structure Creation**
   - For each image, store:
     ```json
     {
       "image_path": "images/img001.jpg",
       "description": "A lonely tree in a foggy field, evoking isolation and calm.",
       "tags": ["tree", "fog", "isolation", "calm"]
     }
     ```
   - Store all entries in a master `data.json` or `.csv`.

4. **Save Configuration**
   - Prompt user to save:
     - Data map file
     - Config file with parameters:
       ```json
       {
         "display_mode": "raster",
         "image_opacity": 0.8,
         "max_images_on_screen": 5,
         "update_interval_sec": 3
       }
       ```

5. **Output Summary**
   - Saved in `/output` directory with timestamped filenames.
   - User can review and re-run with different AI prompts or curations.

---

## Part II – AIMCoS-Display

### Purpose
Loads the curated data and responds to live spoken words by dynamically selecting and displaying related images.

### Inputs
- Pre-saved data map (`data.json`)
- Config file
- Live microphone input (via system or USB mic)

### Outputs
- Real-time visual display (e.g., fullscreen or windowed raster)
- Optional session log

### Workflow

1. **Initialize Application**
   - Prompt user to select config and data files from dropdown or file browser.

2. **System Initialization**
   - Load image-response mappings into memory.
   - Initialize microphone and audio processing module.
   - Prepare graphics renderer (OpenGL, Pygame, or web canvas, etc.).

3. **Live Audio Capture**
   - Continuously sample audio input in short windows (e.g., 3–5 sec).
   - Convert audio to text using speech-to-text engine (e.g., Google Speech API, Whisper, Vosk).

4. **Keyword Extraction**
   - Use NLP parsing to extract:
     - Nouns
     - Adjectives
     - Named Entities
   - Optional: TF-IDF or semantic vectorization for more nuanced results.

5. **AI or Algorithmic Matching**
   - Compare parsed keywords with descriptions or tags in the data map.
   - Matching can use:
     - Direct keyword overlap
     - Cosine similarity between vector embeddings (e.g., using OpenAI embeddings or spaCy)
   - Select top-matching image(s) with fallback option.

6. **Image Display**
   - Render selected image in the designated region of the display.
   - Apply transformations based on config (scale, opacity, layer order).
   - Maintain layered display without erasing previous images unless config requires.

7a. **Loop & Update** two possibilities:  select one or the other
 
   - Wait `update_interval_sec` before processing next speech input.  
   - Repeat steps 3–6 until user exits application.  
7b. **Loop & Update**
   - Continuously monitor accumulated spoken words.
   - When the **word count exceeds a configurable threshold** (e.g., every 10–15 words), process the current queue.
   - After processing:
     - Clear the word buffer.
     - Display new image(s) based on matches.
   - Repeat the cycle until the application is terminated.


9. **Termination**
   - On keypress or UI trigger, save optional session log:
     - Timestamps
     - Spoken input
     - Image responses
   - Close display and free resources.

---

## System Requirements

### Dependencies
- Python 3.8+
- OpenAI API (or local LLM)
- Speech-to-text engine (e.g., Whisper, Vosk)
- Image display library (e.g., Pygame, Tkinter, ElectronJS)
- NLP toolkit (spaCy, NLTK, or OpenAI embeddings)

### Hardware
- Microphone (standard or USB)
- Display (HD or higher recommended)

---

## Future Considerations
- **User Interaction Layer**: Let audience touch or click images for more information or branching paths.
- **Projection Support**: Map visual output to physical surfaces.
- **Emotion Detection**: Infer emotional tone of speech to bias image selection.
- **Network Sync**: Enable multiple clients or a central server for collaborative displays.

---
