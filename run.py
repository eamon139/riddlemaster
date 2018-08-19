import os
import json
from datetime import datetime
from flask import Flask, redirect, render_template, request

app = Flask(__name__)
app.secret_key = 'some_secret'
data = []


def write_to_file(filename, data):
    """Handle process of writing data to a file"""
    with open(filename, "a") as file:
        file.writelines(data)




@app.route('/', methods=["GET", "POST"])
def index():
    """Main page ad user name ---------------------------------------"""
    
    # Handel the post request
    if request.method == "POST":
        write_to_file("data/users.txt", request.form["username"] + "\n")
        return redirect(request.form["username"])
    return render_template("index.html")


@app.route('/<username>')
def user(username):
    """Display welcome MGS messages on thegame page -----------------------"""
    data = []
    with open("data/questions.json", "r") as json_data:
            data = json.load(json_data)
            return render_template("thegame.html", username=username, question_data=data)
                            
                            
                            



app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)

