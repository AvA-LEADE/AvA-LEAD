from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "secret123"

# Lưu user tạm thời
users = {}

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["username"] = username
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for("home"))
        else:
            flash("Sai tài khoản hoặc mật khẩu!", "error")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if username in users:
            flash("Tài khoản đã tồn tại!", "error")
        elif password != confirm:
            flash("Mật khẩu nhập lại không khớp!", "error")
        else:
            users[username] = password
            flash("Đăng ký thành công! Hãy đăng nhập.", "success")
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/home")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("home.html", username=session["username"])


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Đã đăng xuất!", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
