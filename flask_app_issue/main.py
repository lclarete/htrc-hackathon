import requests
import re
import pandas as pd
from nltk.corpus import stopwords, words
import nltk
from util import export_charts_to_html, get_ef_data_by_volume_id, get_ht_bib_metadata, extract_ef_ids, extract_data_from_pages, extract_book_data, export_charts_to_pdf

nltk.download('stopwords')
nltk.download('words')

BASE_URL_HTRC = "https://data.htrc.illinois.edu/ef-api"
BASE_URL_HT = "https://catalog.hathitrust.org/api/volumes/full/"

stop_words = set(stopwords.words('english'))
english_vocab = set(words.words())

def main(oclc):
    metadata = get_ht_bib_metadata("oclc", oclc, BASE_URL_HT)
    extract_book_data(metadata, 'book_data.csv')
    mich = get_ef_data_by_volume_id(extract_ef_ids(metadata), BASE_URL_HTRC)
    ef_mich = extract_data_from_pages(mich, stop_words, english_vocab)
    df = pd.DataFrame.from_records(ef_mich).sort_values(by='counts', ascending=False)
    df['cumulative_sum'] = df.groupby('token')['counts'].cumsum()
    df['length'] = df['token'].str.len()
    return df

oclc_lawrence = "3580950"
df = main(oclc_lawrence)

export_charts_to_html(df, 'results.html')
export_charts_to_pdf(df, 'book_data.csv', 'charts_output.pdf')
