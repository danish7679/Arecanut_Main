import streamlit as st
import os
import subprocess
import streamlit.web.cli as stcli




def save_uploaded_file(file):
    os.makedirs("temp", exist_ok=True)

    # Save the uploaded file to the temporary directory
    file_path = os.path.join("temp", file.name)
    with open(file_path, "wb") as f:
        f.write(file.getvalue())

    return file_path



def run_detection(file_path,detect_script_path):

    command = [
        "python",
        detect_script_path,
        "--weights", "best.pt",
        "--img", str(256),
        "--conf", str(0.1),
        "--source", file_path
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    st.text(result.stdout)
    st.text(result.stderr)

    result1=str(result)

    if "good" in result1:
        st.text("Arecanut Grade = 1")
    elif "karigot" in result1:
        st.text("Arecanut Grade = 2")
    elif "phatora" in result1:
        st.text("Arecanut Grade = 3")
    else :
        st.text("Arecanut not detected")




st.header('Arecanut Classification')

file = st.file_uploader("Upload a file...", type=["jpg", "jpeg", "png", "mp4"])

if file is not None:
    st.write("Uploaded File:")
    if file.type.startswith('image'):
        st.image(file, caption='Uploaded Image')
        folder = 'temp_images'
    elif file.type.startswith('video'):
        st.video(file.read())
        folder = 'temp_videos'
    else:
        st.error("Unsupported file format.")
        st.stop()

    if st.button("Detect Arecanut"):
        file_path = save_uploaded_file(file)
        detect_script_path = "yolov5\\detect.py"
        run_detection(file_path, detect_script_path)