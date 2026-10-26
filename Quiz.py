
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Capital City Quiz</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .quiz-container {
            background: white;
            width: 100%;
            max-width: 500px;
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
        }

        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
        }

        .subtitle {
            text-align: center;
            color: #777;
            margin-bottom: 30px;
        }

        .question {
            margin-bottom: 25px;
        }

        label {
            display: block;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }

        input {
            width: 100%;
            padding: 13px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
            outline: none;
        }

        input:focus {
            border-color: #667eea;
            box-shadow: 0 0 5px #667eea;
        }

        button {
            width: 100%;
            padding: 14px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 17px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }

        button:hover {
            background: #4c5fd5;
        }

        .result {
            margin-top: 25px;
            padding: 20px;
            text-align: center;
            border-radius: 10px;
            background: #f0f4ff;
        }

        .result h2 {
            color: #333;
            margin-bottom: 10px;
        }

        .result p {
            margin: 8px 0;
            font-size: 16px;
        }

        .correct {
            color: green;
        }

        .wrong {
            color: red;
        }

        .footer {
            text-align: center;
            margin-top: 25px;
            color: #999;
            font-size: 13px;
        }
    </style>
</head>

<body>

    <div class="quiz-container">

        <h1>Capital City Quiz</h1>
        <p class="subtitle">Test your knowledge of Indian capitals!</p>

        <form method="POST">

            <div class="question">
                <label for="india">
                    1. What is the capital of India?
                </label>

                <input
                    type="text"
                    id="india"
                    name="india"
                    placeholder="Enter your answer"
                    required
                >
            </div>

            <div class="question">
                <label for="telangana">
                    2. What is the capital of Telangana?
                </label>

                <input
                    type="text"
                    id="telangana"
                    name="telangana"
                    placeholder="Enter your answer"
                    required
                >
            </div>

            <button type="submit">Submit Answers</button>

        </form>

        {% if score is not none %}
        <div class="result">

            <h2>Your Result</h2>

            <p>
                Your Score: <strong>{{ score }} / 2</strong>
            </p>

            <p class="{{ 'correct' if india_correct else 'wrong' }}">
                India: {{ 'Correct!' if india_correct else 'Wrong! Answer: New Delhi' }}
            </p>

            <p class="{{ 'correct' if telangana_correct else 'wrong' }}">
                Telangana: {{ 'Correct!' if telangana_correct else 'Wrong! Answer: Hyderabad' }}
            </p>

        </div>
        {% endif %}

        <div class="footer">
            Made with Python Flask
        </div>

    </div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    score = None
    india_correct = False
    telangana_correct = False

    if request.method == "POST":

        india = request.form.get("india", "").strip().lower()
        telangana = request.form.get("telangana", "").strip().lower()

        india_correct = india in ("delhi", "new delhi")
        telangana_correct = telangana == "hyderabad"

        score = int(india_correct) + int(telangana_correct)

    return render_template_string(
        HTML,
        score=score,
        india_correct=india_correct,
        telangana_correct=telangana_correct
    )


if __name__ == "__main__":
    app.run(debug=True)
