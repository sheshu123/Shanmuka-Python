# user_name=input("Enter your name: ")
# user_password=input("Enter your password: ") 
# inbuit_user_name="admin"
# inbuit_user_password="admin123"
# if user_name==inbuit_user_name and user_password==inbuit_user_password:
#     print("Login successful!")
# else:
#     print("Invalid username or password.")


from flask import Flask, request, render_template_string

app = Flask(__name__)

inbuilt_user_name = "admin"
inbuilt_user_password = "admin123"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Glass Login</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', Arial, sans-serif;
}

body {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    background: linear-gradient(135deg, #090e29, #251653, #086b83);
    padding: 20px;
}

/* Background glow effects */
.glow {
    position: fixed;
    border-radius: 50%;
    filter: blur(3px);
    opacity: 0.8;
    pointer-events: none;
}

.glow-one {
    width: 280px;
    height: 280px;
    background: linear-gradient(135deg, #ff42d0, #754bff);
    top: 8%;
    left: 12%;
}

.glow-two {
    width: 320px;
    height: 320px;
    background: linear-gradient(135deg, #00e5ff, #2875ff);
    bottom: 5%;
    right: 10%;
}

.glow-three {
    width: 150px;
    height: 150px;
    background: #a855f7;
    bottom: 15%;
    left: 20%;
}

/* Glass login card */
.login-card {
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 390px;
    padding: 42px 35px;
    color: white;
    text-align: center;

    background: rgba(255, 255, 255, 0.10);
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);

    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 24px;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.35);
}

.logo {
    width: 64px;
    height: 64px;
    margin: 0 auto 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 20px;
    font-size: 30px;
    font-weight: bold;
    background: linear-gradient(135deg, #8b5cf6, #06b6d4);
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
}

h1 {
    font-size: 29px;
    margin-bottom: 10px;
    letter-spacing: -0.5px;
}

.subtitle {
    color: #d4d8f5;
    font-size: 14px;
    margin-bottom: 32px;
}

.form-group {
    text-align: left;
    margin-bottom: 20px;
}

label {
    display: block;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 9px;
    color: #f1f3ff;
}

input {
    width: 100%;
    padding: 14px 15px;
    color: white;
    font-size: 14px;
    background: rgba(10, 15, 45, 0.35);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 11px;
    outline: none;
    transition: 0.3s;
}

input::placeholder {
    color: #c2c9e4;
}

input:focus {
    border-color: #67e8f9;
    box-shadow: 0 0 0 3px rgba(103, 232, 249, 0.15);
}

button {
    width: 100%;
    padding: 14px;
    margin-top: 7px;
    border: none;
    border-radius: 11px;
    background: linear-gradient(100deg, #8b5cf6, #06b6d4);
    color: white;
    font-size: 15px;
    font-weight: bold;
    cursor: pointer;
    transition: 0.3s;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(6, 182, 212, 0.3);
}

.message {
    margin-top: 20px;
    padding: 12px;
    border-radius: 10px;
    font-size: 14px;
    overflow-wrap: anywhere;
}

.success {
    color: #bbf7d0;
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(74, 222, 128, 0.4);
}

.error {
    color: #fecaca;
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(248, 113, 113, 0.4);
}

.footer {
    margin-top: 26px;
    font-size: 12px;
    color: #c4cbe8;
}

@media (max-width: 480px) {
    .login-card {
        padding: 35px 24px;
    }

    .glow-one {
        left: -100px;
    }

    .glow-two {
        right: -130px;
    }
}
</style>
</head>

<body>

<div class="glow glow-one"></div>
<div class="glow glow-two"></div>
<div class="glow glow-three"></div>

<div class="login-card">

    <div class="logo">✦</div>

    <h1>Welcome Back</h1>
    <p class="subtitle">Sign in to continue to your account</p>

    <form method="POST">

        <div class="form-group">
            <label for="username">Username</label>
            <input
                type="text"
                id="username"
                name="username"
                placeholder="Enter your username"
                autocomplete="username"
                required
            >
        </div>

        <div class="form-group">
            <label for="password">Password</label>
            <input
                type="password"
                id="password"
                name="password"
                placeholder="Enter your password"
                autocomplete="current-password"
                required
            >
        </div>

        <button type="submit">Sign In →</button>

    </form>

    {% if message %}
        <div class="message {{ status }}" role="status">
            {{ message }}
        </div>
    {% endif %}

    <p class="footer">SECURE LOGIN · WELCOME TO YOUR SPACE</p>

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    status = ""

    if request.method == "POST":
        user_name = request.form.get("username", "")
        user_password = request.form.get("password", "")

        if (
            user_name == inbuilt_user_name
            and user_password == inbuilt_user_password
        ):
            message = "Login successful!"
            status = "success"
        else:
            message = "Invalid username or password."
            status = "error"

    return render_template_string(
        HTML,
        message=message,
        status=status
    )

if __name__ == "__main__":
    app.run(debug=True)



