# CS50x Final Project
# Michael Samp

from flask import Flask, render_template, request, redirect
import json
import helpers

app = Flask(__name__)

# Homepage
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        # Create a text file containing a counter in the static/ folder so that
        # the current puzzle number can be accessed globally
        with open('static/counter.txt', 'w') as counter:
            counter.write('-1')
        counter.close()

        # Get form data for pieces to include
        pieces = ""
        pieces += request.form.get('my_pawn', '')
        pieces += request.form.get('my_bishop', '')
        pieces += request.form.get('my_knight', '')
        pieces += request.form.get('my_rook', '')
        pieces += request.form.get('my_queen', '')
        pieces += request.form.get('op_pawn', '')
        pieces += request.form.get('op_bishop', '')
        pieces += request.form.get('op_knight', '')
        pieces += request.form.get('op_rook', '')
        pieces += request.form.get('op_queen', '')

        # Get form value for rating or use default value
        lower_rating = request.form.get('lower_rating')
        if lower_rating == '':
            lower_rating = 0
        upper_rating = request.form.get('upper_rating')
        if upper_rating == '':
            upper_rating == 5000

        # Create the pieces list that will be searched against the database
        pieces = ''.join(sorted(pieces))

        # Search for specified piece combination and return the match list at
        # static/puzzles.json
        helpers.find_puzzle(pieces, lower_rating, upper_rating)

        # Make sure puzzles are found
        with open('static/puzzles.json', 'r') as puzzle_list:
            puzzles = json.load(puzzle_list)
            if not puzzles['Rating']:
                error = 'No puzzles found. Try a different piece combination.'
                print('An error has occurred')
                puzzle_list.close()
                return render_template('index.html', error=error)

        # Move to puzzles page for actual puzzle solving
        return redirect("/puzzles")
    
    if request.method == "GET":

        # Initial load
        with open('static/counter.txt', 'w') as counter:
            counter.write('')
        counter.close()
        return render_template('index.html', puzzle_url='')
        

# Page where puzzles are solved
@app.route("/puzzles")
def puzzles():
    
    # Get puzzle number
    with open('static/counter.txt', 'r') as counter:
        i = int(counter.read())
    counter.close()

    # Iterate counter
    i += 1
 

    # Write new counter
    with open('static/counter.txt', 'w') as counter:
        counter.write(str(i))

    # Open puzzle data and output the ith puzzle in the list
    file = open('static/puzzles.json')
    puzzles = json.load(file)
    num_puzzles = len(puzzles['Rating'])

    return render_template('puzzles.html', rating=puzzles['Rating'][i], 
                                           moves=puzzles['Moves'][i], 
                                           PuzzleId=puzzles['PuzzleId'][i], 
                                           URL=puzzles['EncodedURL'][i],
                                           i=i, num_puzzles=num_puzzles)
