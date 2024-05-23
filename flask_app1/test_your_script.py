import your_script
import os
import json

def test_function():
    code = 'test_code'  # Replace with an appropriate test code
    try:
        print("Testing main function with code:", code)
        # Test main function
        df = your_script.main(code)
        print("DataFrame returned by main function:", df.head())

        # Save the dataframe to a CSV file
        df.to_csv('output_test.csv', index=False)
        print("DataFrame saved to CSV successfully")

        # Test export_charts_to_pdf function
        pdf_directory = 'pdfs'
        pdf_filename = 'charts_output_test.pdf'
        if not os.path.exists(pdf_directory):
            os.makedirs(pdf_directory)
        pdf_path = os.path.join(pdf_directory, pdf_filename)
        your_script.export_charts_to_pdf(df, 'book_data.csv', pdf_path)
        print("PDF generated successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    test_function()
