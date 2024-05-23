from flask import Flask, render_template, request, redirect
import json
import os
import your_script  # Import your data processing script

app = Flask(__name__)

DATA_FILE = 'data.json'

# Ensure data.json exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({"codes": []}, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-code', methods=['POST'])
def submit_code():
    code = request.form['code']
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    data['codes'].append(code)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

    # Process the code using the functions from your_script
    df = your_script.main(code)  # Assuming main function is adapted to take `code`
    df.to_csv('output.csv', index=False)
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
