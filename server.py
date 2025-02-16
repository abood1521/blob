from flask import Flask, request, render_template
import os
from transcribe import transcribe_audio
from flask_cors import CORS
from saving import save_text_to_file

app = Flask(__name__)
CORS(app)

integer_list = []

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def new_int_name():
    for name in os.listdir("uploads"):
        try:
            print(name[:-4])
            # int(name[:-4])
            integer_list.append(int(name[:-4]))
        except:
            pass
    return max(integer_list)
            

@app.route("/listen_audio", methods=["POST"])
def listen_audio():
    if "audio" not in request.files:
        return "No audio file found", 400
    
    audio_file = request.files["audio"]
    # print(audio_file.filename)
    filename = audio_file.filename.strip() if audio_file.filename.strip() and audio_file.filename != ".wav" else str(new_int_name()+1)+".wav"
    audio_path = os.path.join(UPLOAD_FOLDER, filename)
    audio_file.save(audio_path)
    print(f"Filename: {filename}")

    transcription = transcribe_audio(f"uploads/{filename}")
    save_text_to_file(f"transcriptions/{filename[:-4]}.txt", transcription)
    print(transcription)
    return f"Audio received and transcribed as {transcription}"

@app.route("/home")
def load_home_page():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=9999, host="0.0.0.0")
