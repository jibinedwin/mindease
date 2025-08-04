from flask import Flask, render_template, request, redirect, url_for
from nlp_utils import detect_emotion, generate_response, is_crisis
from database import init_db, log_conversation, get_stats

app = Flask(__name__)
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    user_input = bot_response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        emotion, score = detect_emotion(user_input)
        bot_response = generate_response(emotion)

        # Append crisis helpline if needed
        if is_crisis(user_input):
            bot_response += (
                " It sounds like you might be in distress. "
                "If you're thinking about harming yourself, please reach out to "
                "local helplines or mental health professionals immediately."
            )

        log_conversation(user_input, bot_response, emotion, score)

    return render_template(
        "index.html",
        user_input=user_input,
        bot_response=bot_response
    )

@app.route("/stats")
def stats():
    data = get_stats()
    # data: list of (emotion, count)
    return render_template("stats.html", stats=data)

if __name__ == "__main__":
    app.run(debug=True)
