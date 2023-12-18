from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Data structure to store user information and selections
user_data = []

def calculate_most_picked_number(user_data):
    # Dictionary to store the count of each picked number
    number_counts = {}

    # Iterate through user data and count occurrences of each picked number
    for user in user_data:
        picked_number = user['number']
        if picked_number in number_counts:
            number_counts[picked_number] += 1
        else:
            number_counts[picked_number] = 1

    # Find the number with the maximum count (most picked number)
    most_picked_number = max(number_counts, key=number_counts.get)

    return most_picked_number

@app.route('/')
def main_page():
    return render_template('main_page.html', numbers=[1, 2, 3, 5, 8, 13])

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Retrieve user name and selected number from the form
        name = request.form['name']
        selected_number = int(request.form['number'])
        
        # Save user data to the data structure
        user_data.append({'name': name, 'number': selected_number})
        
        # Save user data to a JSON file
        with open('user_data.json', 'w') as file:
            json.dump(user_data, file)
        
        return redirect(url_for('main_page'))

@app.route('/results')
def results():
    # Load user data from the JSON file
    with open('user_data.json', 'r') as file:
        user_data = json.load(file)
    
    # Call the function to get the most picked number
    most_picked_number = calculate_most_picked_number(user_data)
    
    return render_template('results.html', user_data=user_data, most_picked_number=most_picked_number)

if __name__ == '__main__':
    app.run(debug=True)
