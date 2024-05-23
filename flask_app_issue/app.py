from flask import Flask, render_template, request, redirect, send_from_directory
import json
import os
import your_script  # Import your data processing script

app = Flask(__name__)

DATA_FILE = 'data.json'
PDF_DIRECTORY = 'pdfs'
PDF_FILENAME = 'charts_output.pdf'

# Ensure data.json exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({"codes": []}, f)

# Ensure PDF directory exists
if not os.path.exists(PDF_DIRECTORY):
    os.makedirs(PDF_DIRECTORY)

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

    # Generate the PDF
    pdf_path = os.path.join(PDF_DIRECTORY, PDF_FILENAME)
    your_script.export_charts_to_pdf(df, 'book_data.csv', pdf_path)

    # Serve the PDF file
    return redirect(f'/download/{PDF_FILENAME}')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(PDF_DIRECTORY, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
