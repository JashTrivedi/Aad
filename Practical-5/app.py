from flask import Flask, render_template, request

app = Flask(__name__)

# Function to calculate the minimum coins using dynamic programming
def min_coins(amount, coins):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1

# Home page route - Minimum Coin Calculator
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            amount = int(request.form['amount'])
            coins = [1, 4, 6]
            result = min_coins(amount, coins)
        except ValueError:
            result = "Invalid input"
    return render_template('index.html', result=result)

# Comparative Analysis Route
@app.route('/analysis')
def analysis():
    coins = [1, 4, 6]
    test_cases = [1, 2, 5, 9, 10, 12, 15, 20]
    results = {case: min_coins(case, coins) for case in test_cases}
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
