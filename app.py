from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return "Method used %s" %request.method


@app.route("/profile/<username>")
def profile(username):
    return render_template("profile.html", username=username)








@app.route("/beef", methods = ['GET', 'POST'])
def beef():
    if request.method == 'POST':
        return 'You are using POST mehtod'
    else:
        return 'You are using GET method'


@app.route("/tuna")
def page():
    return "<h2>Tuna is GOOD</h2>"



@app.route("/post/<int:postID>")
def post(postID):
    return "<h2>The post number is %s</h2>" %postID


if __name__ == "__main__":
    app.run(debug=True)

