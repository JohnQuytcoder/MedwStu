from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "supersecret"  # key để giữ session

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Fake database lưu user
users = {}

# ---------- LOGIN GATE ----------
@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("index"))
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("index"))
        else:
            return "Sai tài khoản hoặc mật khẩu!"
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users:
            return "Tài khoản đã tồn tại!"
        users[username] = password
        session["user"] = username
        return redirect(url_for("index"))
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

# ---------- MAIN WEB ----------
@app.route("/index")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        file = request.files["file"]
        path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(path)
        return f"Đã upload: {file.filename}"
    return render_template("upload.html")

@app.route("/quiz")
def quiz():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("quiz.html")

@app.route("/quiz_timer")
def quiz_timer():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("quiz_timer.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Secret key để dùng session

# Giả lập cơ sở dữ liệu người dùng
users_db = {}

# Trang index (Đăng nhập hoặc Đăng ký)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Đăng nhập
        username = request.form["username"]
        password = request.form["password"]

        if username in users_db and users_db[username] == password:
            session["username"] = username
            return redirect(url_for('dashboard'))  # Redirect đến trang dashboard nếu đăng nhập thành công
        else:
            return "Tên đăng nhập hoặc mật khẩu không đúng", 401
    return render_template("index.html")

# Trang đăng ký
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Xử lý đăng ký người dùng
        username = request.form["username"]
        password = request.form["password"]

        if username in users_db:
            return "Tên đăng nhập đã tồn tại", 400
        users_db[username] = password
        return redirect(url_for('index'))  # Redirect về trang đăng nhập sau khi đăng ký

    return render_template("signup.html")

# Trang Dashboard (chỉ cho người đã đăng nhập)
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("index"))  # Nếu chưa đăng nhập, redirect về trang index
    return f"Chào mừng {session['username']} đến trang chính của MedwStu!"

if __name__ == "__main__":
    app.run(debug=True)
