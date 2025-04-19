from flask import Flask, render_template, request
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(path)
        return f"Đã upload: {file.filename}"
    return render_template("upload.html")

app.run(host='0.0.0.0', port=3000)
