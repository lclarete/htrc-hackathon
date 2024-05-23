from flask import Flask, render_template, request, redirect, send_from_directory
import json
import os
import your_script  # Import your data processing script

app = Flask(__name__)
app.config['SECRET_KEY'] = '8b3798d5ae564b839f7d279b474f6452'  # Hardcoded secret key
app.config['DEBUG'] = True

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
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        data['codes'].append(code)
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)

        # Debugging the code processing
        print(f"Processing code: {code}")
        
        # Process the code using the functions from your_script
        df = your_script.main(code)  # Assuming main function is adapted to take `code`
        print(f"DataFrame created: {df.head()}")
        df.to_csv('output.csv', index=False)
        print("DataFrame saved to CSV successfully")

        # Generate the PDF
        pdf_path = os.path.join(PDF_DIRECTORY, PDF_FILENAME)
        your_script.export_charts_to_pdf(df, 'book_data.csv', pdf_path)
        print("PDF generated successfully")

        # Serve the PDF file
        return redirect(f'/download/{PDF_FILENAME}')
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}", 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(PDF_DIRECTORY, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Ensure the app listens on all network interfaces
