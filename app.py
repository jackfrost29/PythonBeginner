from flask import Flask, request, render_template
app = Flask(__name__)


@app.route("/")
@app.route("/<User>")
def home(User=None):
    return render_template("user.html", user=User)

@app.route("/login")
def loginPage():
    return render_template('login.html')

@app.route("/shopping")
def showShoppingList():
    food = ["Cheese", "Burger", "Shwarma"]
    return render_template("shoppingList.html", food = food)

'''
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
'''

if __name__ == "__main__":
    app.run(debug=True)

