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
    """Main page add user name ---------------------------------------------"""
    if request.method == "POST":
        write_to_file("data/users.txt", request.form["username"] + "\n")
        return redirect(request.form["username"])
    return render_template("index.html")


@app.route('/<username>', methods=["GET", "POST"])
def user(username):
    """Display welcome MGS messages on thegame page -----------------------"""
    data = []
    with open("data/questions.json", "r") as json_data:
            data = json.load(json_data)
        
 
    ###--Add question
    question_index = 0
    if request.method == "POST":
       
       write_to_file("data/guess.txt", request.form["guess"] + "\n")
       
       user_response = request.form["guess"].lower()
       
       if data[question_index]["answer"] == user_response:
            # Correct answer
            # Go to next riddle
            question_index += 1
  

    return render_template("thegame.html",
                            username=username, question_data=data, question_index=question_index)



app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)

