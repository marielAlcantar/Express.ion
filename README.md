# Express.ion 😁🙁😡🤢🥶
Python/Tkinter desktop application that runs a selection window with three options: the first corresponds to recording expressions without any stimulus presented 😁, the second section corresponds to recording with stimuli presented 🥶, and the last section corresponds to recording expressions while looking at the screen 😊.

## 🛠 Features 
1. Initial window: Displays instructions and a button to start the experiment.
2. Main menu with buttons to choose between three experiment sections and exit the program.
3. Section 1: Expression + Neutral
  - Displays the expression words (Happy, Sad, Anger, etc.) in full screen.
  - For each expression, the camera records a video segment of a fixed duration (DURATION).
3. Section 2: Images
  - Loads all images found in the PATH_IMAGES folder.
  -Displays them in full screen one by one, while the camera records each stimulus.
  -Each video is saved with the name of the corresponding image.
4. Section 3: Camera
  -Records directly with OpenCV in full screen.
  -Each expression is overlaid as text in the top left corner.
  -The video is scaled to fit the screen resolution with black borders if necessary.
  -An AVI file is recorded for each expression.
5. At the end of each section, a pop-up message is displayed confirming the recording.
6. All videos are stored in the Documents\Facial Expression Logs\Recording_YYYYMMDD_HHMMSS folder, organized into subfolders:
  -Section 1
  -Section 2
  -Section 3
## 📌 Requirements
- Python 3.8+
- Tkinter
- Pygame (for displaying images and colors)
- OpenCV (for capturing and recording images)
- Numpy (for handling images and black frames)
- PIL / Pillow (for drawing text over images and supporting accents)
## 🧭 Step-by-Step Instructions
1. Place the script (expression.py) and the images in the folder Imagenes2.
2. Install requirements.

Create and activate a virtual environment, then install dependencies.
**Windows / macOS**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS
source .venv/bin/activate

pip install -r requirements.txt
```
3. Run "expression.py".

``` bash
python expression.py

```
4. A window titled “Instrucciones” will open.
   Read the instructions carefully and click “Comenzar”.

3. The main menu appears with the following options:
  -Sección 1: Sin estímulo
  -Sección 2: Con estímulo visual
  -Sección 3: Cámara + Texto
  -Salir
5. Click a section button to start recording.
  Each section runs automatically and shows a message box when finished.
6. Recorded videos are automatically saved in:
   Documents/Facial expressions records/Grabacion_YYYYMMDD_HHMMSS/
   Inside, there are three folders:
   Seccion1/
   Seccion2/
   Seccion3/



## 📑 Usage 
  -This Python/Tkinter desktop application allows you to record facial expressions across three different experimental sections:
  -Section 1 – Without Stimuli:
    Displays only the name of each emotion on a fullscreen window.
    The user performs the expression for each emotion for 10 seconds.
  -Section 2 – With Visual Stimuli:
    Shows external images (e.g., emotional pictures) as stimuli while recording.
    Each image is displayed fullscreen for the set duration while the webcam records.
      ⚠️ You must have a folder containing the stimuli images.
      Update its path in the variable RUTA_IMAGENES near the top of the code. The folder is Images2, 
      which can be downloaded from the repository.
  -Section 3 – Mirror Mode (Self-View):
    Opens the webcam in fullscreen so the user can see themselves while performing each emotion.
    The emotion name is shown on screen (drawn with Pillow for accented characters).

## Notes
- The camera is automatically released when closing the app.
- To stop a section early, press Esc (Section 3 only).
- Ensure the arial.ttf font is available for accented text (used by Pillow).
- Fullscreen mode is used for both Pygame and OpenCV windows.

## 📕 Language 
- Spanish-only UI. All labels, buttons, and feedback messages are in Spanish.
- Button labels, instructions, and messages are shown in Spanish.
## 🧾 License
This project is licensed under the **MIT License**.  
Copyright © 2025 Amaury Santiago Horta.
See the [LICENSE](LICENSE) file for details.
