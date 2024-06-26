import requests
import re
import pandas as pd
from nltk.corpus import stopwords, words
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

# Download stopwords and English words from NLTK if not already downloaded
import nltk
nltk.download('stopwords')
nltk.download('words')

BASE_URL_HTRC = "https://data.htrc.illinois.edu/ef-api"
BASE_URL_HT = "https://catalog.hathitrust.org/api/volumes/full/"

stop_words = set(stopwords.words('english'))
english_vocab = set(words.words())

def get_ef_data_by_volume_id(volume_id):
    """Fetches the extract featureset data for a given volume"""
    url = f"{BASE_URL_HTRC}/volumes/{volume_id}"
    response = requests.get(url)
    return response.json()["data"]["features"]["pages"]

def get_ht_bib_metadata(id_type, id_value):
    """Fetches the volume metadata for a given standard identifier.
    id_type should be one of oclc, issn, isbn, issn, htid, recordnumber"""
    url = f"{BASE_URL_HT}/{id_type}/{id_value}.json"
    response = requests.get(url)
    return response.json()

def extract_ef_ids(lawrence_metadata):
    """Extracts specific fields from items in lawrence_metadata."""
    ef_ids = []
    for item in lawrence_metadata["items"]:
        ef_item = {
            "orig": item["orig"],
            "htid": item["htid"],
            "enumcron": item["enumcron"]
        }
        ef_ids.append(ef_item)
    return ef_ids[0]['htid']

def extract_data_from_pages(pages):
    """Extract token data from pages, applying preprocessing steps."""
    extracted_data = []
    for i, page in enumerate(pages):
        body = page.get('body')
        if body:
            token_pos_count = body.get('tokenPosCount')
            if token_pos_count:
                for t, pos in token_pos_count.items():
                    t = t.lower()
                    if t not in stop_words and re.match("^[a-zA-Z]+$", t) and t in english_vocab:
                        token_data = {"page": i, "token": t}
                        pos_dict = dict(zip(["pos", "counts"], list(pos.items())[0]))
                        token_data.update(pos_dict)
                        extracted_data.append(token_data)
    return extracted_data

def extract_book_data(data, csv_filename='book_data.csv'):
    """Extracts book data from the given data structure and creates a DataFrame."""
    records = data['records']
    items = data['items']
    titles = []
    oclcs = []
    publish_dates = []
    orig = []
    item_urls = []
    for record_id, record_info in records.items():
        titles.append(record_info['titles'][0] if record_info['titles'] else None)
        oclcs.append(record_info['oclcs'][0] if record_info['oclcs'] else None)
        publish_dates.append(record_info['publishDates'][0] if record_info['publishDates'] else None)
    for item in items:
        orig.append(item['orig'])
        item_urls.append(item['itemURL'])
    df = pd.DataFrame({
        'titles': titles,
        'oclcs': oclcs,
        'publishDates': publish_dates,
        'orig': orig,
        'itemURL': item_urls
    })
    df = df.T
    df.reset_index(inplace=True)
    df.to_csv(csv_filename, index=False, header=False)
    return df

def main(oclc):
    metadata = get_ht_bib_metadata("oclc", oclc)
    extract_book_data(metadata, 'book_data.csv')
    mich = get_ef_data_by_volume_id(extract_ef_ids(metadata))
    ef_mich = extract_data_from_pages(mich)
    df = pd.DataFrame.from_records(ef_mich).sort_values(by='counts', ascending=False)
    df['cumulative_sum'] = df.groupby('token')['counts'].cumsum()
    return df

# Visualization functions
def plot_top_20_frequent_words(df, token_column='token', pdf=None, fig_size=(15, 6)):
    top_20_freq = df[token_column].value_counts()


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib.backends.backend_pdf import PdfPages

def export_charts_to_pdf(main_df, book_csv_path, pdf_path, fig_size=(10, 6)):
    """
    Exports several charts into a single PDF document with book data on the first page.

    Args:
    - main_df (pd.DataFrame): The DataFrame containing the data for the charts.
    - book_csv_path (str): The file path to the CSV file containing book data.
    - pdf_path (str): The file path to save the PDF document.
    - fig_size (tuple): The figure size for all charts.

    Returns:
    - None
    """
    # Read the book data from CSV
    book_data = pd.read_csv(book_csv_path)
    
    with PdfPages(pdf_path) as pdf:
        # Create a figure for the book data
        fig, ax = plt.subplots(figsize=(18, 6))
        ax.axis('off')
        ax.set_title('Book Data')
        
        # Create a table from the book data and add it to the plot
        table = ax.table(cellText=book_data.values, colLabels=book_data.columns, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)

        pdf.savefig(fig)
        plt.close(fig)
        
        # Plot the charts
        plot_top_20_frequent_words(main_df, pdf=pdf, fig_size=(18, 6))
        generate_word_cloud(main_df, pdf=pdf, fig_size=(18, 6))
        plot_top_words_evolution(main_df, pdf=pdf, fig_size=(18, 6))

def plot_top_20_frequent_words(df, token_column='token', pdf=None, fig_size=(8, 4)):
    top_20_freq = df[token_column].value_counts()[:20]

    top20 = pd.DataFrame()
    top20['Words'] = list(top_20_freq.index)
    top20['Counts'] = list(top_20_freq.values)

    colors = sns.color_palette("viridis", len(top20))

    fig, ax = plt.subplots(figsize=fig_size)
    bars = sns.barplot(x='Words', y='Counts', data=top20, palette=colors, ax=ax)
    bars.set(title='Top 20 Most Frequent Words in the Corpus')

    plt.savefig("static/frequency.png")

    if pdf:
        pdf.savefig(fig)
    plt.close(fig)

def generate_word_cloud(df, token_column='token', pdf=None, fig_size=(10, 6)):
    token_counts = df.groupby(token_column)['counts'].sum().to_dict()

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(token_counts)

    fig, ax = plt.subplots(figsize=fig_size)
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('Word Cloud of Most Frequent Tokens')


    plt.savefig("static/word_cloud.png")

    if pdf:
        pdf.savefig(fig)
    plt.close(fig)

def plot_top_words_evolution(df, token_column='token', count_column='counts', page_column='page', top_n=10, pdf=None, fig_size=(10, 6)):
    top_words = df.groupby(token_column)[count_column].sum().sort_values(ascending=False).head(top_n).index

    fig, ax = plt.subplots(figsize=fig_size)
    for word in top_words:
        word_data = df[df[token_column] == word]
        ax.scatter(word_data[page_column], [word] * len(word_data), s=word_data[count_column] * 10, label=word, alpha=0.6)

    ax.set_xlabel('Page')
    ax.set_ylabel('Words')
    ax.set_title('Evolution of Top Words by Page')
    ax.legend(title='Words', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
    ax.grid(True)

    plt.savefig("static/top_words.png")

    if pdf:
        pdf.savefig(fig)
    plt.close(fig)
