import os
import json
from datetime import datetime
from flask import Flask, redirect, render_template, request

app = Flask(__name__)
app.secret_key = 'some_secret'
data = []
q_index = 0

def write_to_file(filename, data):
    """Handle process of writing data to a file"""
    with open(filename, "a") as file:
        file.writelines(data)
        
def get_wrong_guess_list():
    wrong = []
    with open("data/wrong.txt", "r") as wrong_answer:
        wrong = [row for row in wrong_answer if len(row.strip()) > 0]
    return wrong        
        


@app.route('/', methods=["GET", "POST"])
def index():
    """Main page add user name ---------------------------------------------"""
    if request.method == "POST":
        write_to_file("data/users.txt", request.form["username"] + "\n")
        return redirect(request.form["username"])
    return render_template("index.html")





### create game page
@app.route('/<username>', methods=["GET", "POST"])
def user(username):
    """Display welcome MGS messages on thegame page -----------------------"""
    data = []
    with open("data/questions.json", "r") as json_data:
            data = json.load(json_data)
        
 
    ###--Add question
    
    
    
    if request.method == "POST":
        global q_index
        user_response = request.form["guess"].lower()
       
        if data[q_index]["answer"] == user_response:
            # Correct answer

            q_index += 1
            print("Correct")
            write_to_file("data/right.txt", request.form["guess"] + "\n")
            
            # wrong answer
        else:
            print("Wrong")
            write_to_file("data/wrong.txt", request.form["guess"] + "\n")
    
    if request.method == "POST":
        if user_response == "envelope" and q_index > 9:
            return render_template("endgame.html", username=username, q_index=q_index)
            
    wrong = get_wrong_guess_list()
    
    

  

    return render_template("thegame.html",
                            username=username, question_data=data, q_index=q_index, wrong_answer=wrong)

















"""-----------------------------------------------------------------------------
@app.route('/<username>', methods=["GET", "POST"])
def user(username):
    ###Display welcome MGS messages on thegame page -----------------------
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
--------------------------------------------------------------------------------------------------"""




app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)

