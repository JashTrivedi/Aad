from flask import Flask, render_template, request
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def compare_chefs():
    start_time = time.time()  # Start the timer to measure execution time
    
    points1 = None
    points2 = None
    winner = None
    error_message = None
    chef_result = None
    
    if request.method == 'POST':
        try:
            # Get the input ratings from the form
            chef1_ratings = request.form['chef1'].split()
            chef2_ratings = request.form['chef2'].split()
            
            # Ensure there are exactly 3 ratings for each chef
            if len(chef1_ratings) != 3 or len(chef2_ratings) != 3:
                raise ValueError("Each chef must have exactly 3 ratings (Presentation, Taste, Hygiene).")
            
            # Convert ratings to integers
            chef1_ratings = list(map(int, chef1_ratings))
            chef2_ratings = list(map(int, chef2_ratings))
            
            # Calculate total points for each chef
            points1 = sum(chef1_ratings)
            points2 = sum(chef2_ratings)
            
            # Determine the winner based on the total points
            if points1 > points2:
                winner = "Chef 1 wins!"
            elif points2 > points1:
                winner = "Chef 2 wins!"
            else:
                winner = "It's a tie!"
            
            chef_result = f"Chef 1 total points: {points1}<br>Chef 2 total points: {points2}"
        
        except ValueError as e:
            error_message = str(e)
        
    execution_time = round(time.time() - start_time, 6)  # Measure and round execution time
    
    return render_template('index.html', points1=points1, points2=points2, winner=winner, 
                           error_message=error_message, chef_result=chef_result, execution_time=execution_time)

if __name__ == '__main__':
    app.run(debug=True)
