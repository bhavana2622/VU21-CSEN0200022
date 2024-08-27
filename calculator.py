from flask import Flask, jsonify, request
import requests
import time

app = Flask(__name__)

# Configuration
WINDOW_SIZE = 10
numbers_storage = []
window_prev_state = []
window_curr_state = []

def fetch_numbers(number_id):
    # Simulate fetching numbers from a third-party API
    # Here, replace with your actual API URL
    response = requests.get(f'https://api.example.com/numbers/{number_id}')
    
    if response.status_code == 200:
        return response.json()  # Assuming the response is a JSON list
    return []

def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

@app.route('/numbers/<number_id>', methods=['GET'])
def average_calculator(number_id):
    global window_prev_state, window_curr_state, numbers_storage
    
    start_time = time.time()
    
    # Fetch numbers from the third-party server
    new_numbers = fetch_numbers(number_id)
    
    # Filter unique numbers and disregard duplicates
    unique_numbers = list(set(new_numbers))

    # Update the window state
    window_prev_state = window_curr_state.copy()
    
    # Add new numbers to storage
    numbers_storage.extend(unique_numbers)
    
    # Maintain only the most recent 'WINDOW_SIZE' numbers
    if len(numbers_storage) > WINDOW_SIZE:
        numbers_storage = numbers_storage[-WINDOW_SIZE:]

    window_curr_state = numbers_storage.copy()
    
    # Calculate average
    avg = calculate_average(window_curr_state)

    # Prepare the response
    response = {
        "windowPrevState": window_prev_state,
        "windowCurrState": window_curr_state,
        "numbers": new_numbers,
        "avg": avg
    }

    # Check for response time
    elapsed_time = time.time() - start_time
    if elapsed_time > 0.5:
        return jsonify({"error": "Response time exceeded 500 ms"}), 504

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
