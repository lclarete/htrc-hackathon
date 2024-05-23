### Welcome to the Extracted Features Café (EFC)! 

The EFC is a standalone web app (implemented in Flask) designed to make the HathiTrust Extracted Features API (https://htrc.stoplight.io/docs/ef-api/8xpvh96ani2e0-ef-api) accessible to nonprogrammers, and to expand accessibility by allowing users to search for the Extracted Features using common unique identifiers such as OCLC, ISSN, ISBN, LCCN, and HathiTrust record number. 

By providing user-friendly tools and data visualizations, the EFC aims to bridge the gap between humanities students and computational resources. This will empower them to leverage digital libraries without needing extensive programming knowledge.

#### What are Extracted Features?
The Extracted Features (https://htrc.github.io/torchlite-handbook/ef.html) are data elements derived from a chosen text in the HathiTrust Digital Library. The EFC presents these page- and volume-level features in a word frequency chart, word cloud, and frequency evolution chart, along with four word clusters based on topic modeling within the text. Word frequency charts exclude “stop words,” or common words such as articles, being verbs, prepositions, and pronouns from their results. 

#### Local Installation: How-To

1. Clone this repository.
2. [Recommended] Create a virtual Python environment in the top-level folder, using `python -m venv ENV` or similar.
3. If using a virtual environment, activate it (e.g., `source ENV/bin/activate`), then install the Python dependencies: `pip install -r flask_app_issue/requirements.txt`.
4. Launch the Flask app:
   ```
   cd flask_app_issue
   flask --app app run --debug
   ```
5. Point your browser to `http://127.0.0.1:5000` in order to use the app locally.

The EFC was created by Lívia Clarete, Danielle Nasenbeny, Eryclis Silva, and Dolsy Smith during the Tools for Open Research and Computation with HathiTrust: Leveraging Intelligent Text Extraction (TORCHLITE) Hackathon hosted by the HathiTrust Research Center at University of Illinois at Urbana-Champaign.

Last Updated May 23, 2024. 
