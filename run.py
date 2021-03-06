import os
import json
from datetime import datetime
from flask import Flask, redirect, render_template, request

app = Flask(__name__)
app.secret_key = 'some_secret'
data = []
q_index = 0
guessno = 0

def write_to_file(filename, data):
    """ Writing data to a file """
    with open(filename, "a") as file:
        file.writelines(data)


def write_to_file_leaderboard(filename, data):
    """ Write JSON leaderboard """
    with open(filename, "a") as file:
        file.writelines(data)
        file.write("\n") # Add newline cause Py JSON does not


def write_leaderboard(filename, data):
    """ Write Txt leaderboard """
    with open(filename, "a") as f:
        json.dump(data, f)


def get_wrong_guess_list():
    """ Get wrong guess list """
    wrong = []
    with open("data/wrong.txt", "r") as wrong_answer:
        wrong = [row for row in wrong_answer if len(row.strip()) > 0]
    return wrong


def get_leaderboard():
    """ Get leaderboard form txt file """
    leaderboard =[]
    with open("data/leaderboard.txt", "r") as the_leaderboard:
        leaderboard = [row for row in the_leaderboard if len(row.strip()) > 0]
    return leaderboard



### -----------------------------Login page------------------------------
@app.route('/', methods=["GET", "POST"])
def index():
    """Main page add user name ---------------------------------------------"""
    if request.method == "POST":
        write_to_file("data/users.txt", request.form["username"] + "\n")
        return redirect(request.form["username"])
    return render_template("index.html")





### ------------------------create game page--------------------------------
@app.route('/<username>', methods=["GET", "POST"])
def user(username):
    """Display welcome MGS messages on thegame page -----------------------"""
    data = []
    with open("data/questions.json", "r") as json_data:
            data = json.load(json_data)
            ##open("data/wrong.txt", 'w').close()

    ###--Add question

    if request.method == "POST":
        global q_index
        global guessno
        user_response = request.form["guess"].lower()
        
        if data[q_index]["answer"] == user_response:
            ### right answer
            guessno += 1
            q_index += 1
            open("data/wrong.txt", 'w').close()
            #### wrong answer
        else:
            guessno += 1
            write_to_file("data/wrong.txt", request.form["guess"] + "\n")


    if request.method == "POST":
###------remove to play fullgame ------------>         if user_response == "envelope" and q_index > 9:
        if user_response == "bottle" and q_index > 2:
            leaderboard = get_leaderboard()
            output = [ str(guessno), username]
            open("data/wrong.txt", 'w').close()

            write_to_file_leaderboard("data/leaderboard.txt", output )
###            write_to_file("data/leaderboard.json", output)
            write_leaderboard("data/leaderboard.json", output)
            


            return render_template("endgame.html", q_index=q_index, guessno=guessno, username=username, the_leaderboard = leaderboard )
            
            
    wrong = get_wrong_guess_list()


    return render_template("thegame.html",
                            username=username, question_data=data, q_index=q_index, wrong_answer=wrong)
###-------endgame page--------------------


app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)

