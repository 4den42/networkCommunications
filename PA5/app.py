from flask import Flask, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)
with open('PA5/funFacts.txt', 'r') as file:
    funnies = [line.strip() for line in file.readlines()] 

@app.route('/fact', methods=['GET'])
def fact():
    amount = int(request.headers.get('Amount', 1))  #Always give at least 1 fact
    amount = min(max(amount, 1), 15)                #Cap it
    selected_facts = random.sample(funnies, amount)
    return jsonify(selected_facts)

@app.route('/info', methods=['GET'])
def info():
    user_agent = request.headers.get('User-Agent', 'Unknown')
    http_method = request.method
    current_time = datetime.now()
    return jsonify({
        "Time": current_time,
        "User_Agent": user_agent,
        "Method": http_method
    })

if __name__ == "__main__":
    app.run(debug=True)
