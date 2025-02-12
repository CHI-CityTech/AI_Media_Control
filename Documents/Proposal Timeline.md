# **Structured Timeline and Expanded AI Interaction Research**

## **Phase-Based Timeline for AI-QLab Media Control**
Each phase builds toward a fully **adaptive, AI-controlled media system** that intelligently selects and cues images, video, sound, and lighting in live performances.

| **Stage**   | **Key Focus Areas**                                                        | **Timeframe** |
|------------|----------------------------------------------------------------------------|--------------|
| **1. Research**  | Foundational AI studies, API comparisons, dataset preparation         | **Weeks 1-5** |
| **2. Design**    | AI-based media descriptors, deeper image analysis, user feedback expansion | **Weeks 6-10** |
| **3. Produce**   | AI-driven cueing, real-time data processing, prototype testing        | **Weeks 11-15** |
| **4. Publish**   | Simulated and live tests, evaluation, and documentation               | **Weeks 16-18** |
| **5. Assess**    | Performance review, refinement, integration into future research      | **Weeks 19-20** |

---

## **Expanded AI Media Selection: How AI Can "Know" Images & Cues**
To enable **intelligent media selection**, AI must have **a deeper semantic understanding** of images and cues beyond filenames. This requires AI **describing and classifying media files**, then selecting the most appropriate content based on **natural language prompts** or performance conditions.

### **Key Strategies for AI-Driven Media Understanding**
1. **AI-Generated Descriptions for Each Media Asset**
   - AI **analyzes images/videos** and **auto-generates descriptions** using **Computer Vision (Google Cloud Vision, OpenAI CLIP, RunwayML)**.
   - Example:  
     - AI scans an image of a dark forest and labels it:  
       `"Dark, eerie forest with mist. Low visibility, high contrast lighting."`
   - These descriptors allow AI to match **text-based prompts** to visual content.

2. **Text-to-Image Mapping for AI Selection**
   - AI **receives a word or phrase prompt** (e.g., `"mystical"`, `"chaotic energy"`), then **selects the closest matching image or cue**.
   - AI maps **text-based descriptors** to images based on **semantic similarity** using OpenAI CLIP or a fine-tuned NLP model.
   - Enables **dynamic, improvisational media selection** in response to a live performance.

3. **Multi-Modal Input for AI Decision-Making**
   - AI incorporates **multiple input layers** beyond direct prompts:
     - **Music Features** → Visual Associations  
     - **Performer Gestures** → Lighting & Video Triggers  
     - **Real-Time Audience Reactions** → Scene Adjustments  
   - Example:  
     - A **louder music section** triggers AI to select **more visually intense images or video clips**.

4. **Cue Optimization & Feedback Loop**
   - AI **learns from past performances**, refining media selection over time.
   - AI **records cue effectiveness** based on performer feedback or audience response and **adapts future selections** accordingly.

---

## **Stage 1: Research (Weeks 1-5)**
**Objective:** Establish AI-driven media selection methods and train models for **cue-based selection** beyond file names.

### **Tasks:**
- **Identify the best AI tools for media analysis**  
  - Compare **Google Cloud Vision, OpenAI CLIP, and RunwayML** for **image recognition & description**.
  - Test **text-based AI models (ChatGPT, GPT-4 Vision, LLaVA) for prompt-to-image matching**.
- **Define AI media selection methodology:**  
  - Should AI **pre-label media assets** or **analyze in real-time?**  
  - What **cue categories** will AI recognize? (e.g., energy level, emotion, color scheme)
- **Prepare Media Dataset:**  
  - Collect images, videos, and sound assets to **train AI on selection accuracy**.

### **Deliverables:**
✅ API comparison report  
✅ AI-generated media descriptions for a test dataset  
✅ Initial **text-to-image matching** prototype  

---

## **Stage 2: Design (Weeks 6-10)**
**Objective:** Implement **text-based AI cueing** and real-time AI-driven media matching.

### **Tasks:**
- **Train AI to match text prompts with media selections**  
  - Use **NLP models (ChatGPT, CLIP) to convert natural language into media cues**.
  - Example:  
    - Performer input: `"Create a dreamlike atmosphere."`  
    - AI selects: `"Soft blue lighting + abstract floating visuals."`
- **Improve AI's media understanding**  
  - Incorporate **color analysis, object detection, and sentiment scoring**.
  - AI should **associate visual features with emotional or thematic concepts**.
- **User Feedback System Enhancement:**  
  - Expand feedback options beyond "good/bad" to **ratings & pattern recognition**.
  - AI tracks **which cues are most effective in performances**.

### **Deliverables:**
✅ AI-powered **text-to-media cueing system**  
✅ AI-driven **image and video tagging system**  
✅ Prototype feedback interface for **training AI on cue effectiveness**  

---

## **Stage 3: Produce (Weeks 11-15)**
**Objective:** Deploy the AI-controlled cueing system into **QLab for real-time performance control**.

### **Tasks:**
- **Integrate AI-generated descriptions directly into QLab**  
  - AI **assigns meaning to each QLab cue** based on its analysis.
- **Test AI media cueing with live prompts**  
  - Performers input **keywords, emotions, or gestures**, and AI selects cues.
- **Refine OSC messaging and QLab commands**  
  - Solve **GO1 trigger issues** for improved real-time cueing.

### **Deliverables:**
✅ Fully integrated **AI-driven QLab cue control**  
✅ Initial performance tests with **real-time AI cue selection**  

---

## **Stage 4: Publish (Weeks 16-18)**
**Objective:** Conduct **simulated and live performances** to evaluate AI's performance.

### **Tasks:**
- **Simulated Testing:**  
  - Run **AI-driven media selection tests** without human performers.
- **Live Performance Integration:**  
  - Incorporate AI cueing into a **small-scale live show**.
- **Evaluation:**  
  - Compare **AI cueing vs. manual human cueing**.
  - Measure AI’s **accuracy, responsiveness, and creative contribution**.

### **Deliverables:**
✅ Performance test data  
✅ Video documentation of AI-driven media control  

---

## **Stage 5: Assess (Weeks 19-20)**
**Objective:** Review AI’s **effectiveness, usability, and future potential**.

### **Tasks:**
- **Analyze AI’s cue selection accuracy**  
  - Did AI select **relevant** and **effective** cues in live performances?
- **Improve AI’s long-term learning**  
  - Can AI **remember past performances** and optimize future cueing?
- **Develop Scalability Plan**  
  - Outline **future applications** in **Blended Shadow Puppet Theatre, large-scale productions, and AI-driven immersive media**.

### **Deliverables:**
✅ Final **performance review report**  
✅ Documentation for **future AI-QLab integrations**  
✅ Roadmap for **next research iterations**  

---

## **Final Thoughts & Future Directions**
This research extends **beyond media automation** into **AI-assisted creativity**. By teaching AI to **understand** and **contextualize** media, the system can become a **collaborative creative partner** in live performances.

### **Potential Future Enhancements**
- 🔹 AI **real-time improvisation** (generating **new** visuals/music during performances).
- 🔹 AI **collaborating with performers** to adjust cues dynamically.
- 🔹 Integration into the **Blended Shadow Puppet Theatre for narrative control**.

---


