import argparse
import csv
from datetime import date
import os.path
import re

from googleapiclient.discovery import build
import googleapiclient.discovery
import google_auth_oauthlib.flow
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def main():
    # Set up parser.
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="provide the input file")
    parser.add_argument("--output", help="provide the output file")

    args = parser.parse_args()

    # Read in CSV.
    artists_csv = load_csv(args.input)
    header = artists_csv[0]
    assert header == ['Region',
                      'Artist',
                      'Song',
                      'Link',
                      'Views',
                      'Difference',
                      'Last Updated'], "Headers are wrong!"
    artists_data = artists_csv[1:]

    # Query API and generate final result.
    client = create_client()
    views_map = make_view_map(artists_data, client, extract_ids(artists_data))
    new_artist_csv = [header] + [perform_row_update(*row, views_map) for row in artists_data]

    # Write out to CSV.
    write_csv(args.output, new_artist_csv)

# Transforms the supplied row into a row with updated view date.
def perform_row_update(region, artist, song, link, views, difference, last_update, views_map): 
    new_views = views_map.get(url_to_id(link))
    now = date.today().strftime("%m/%d/%y")
    if views: 
        new_difference = new_views - int(views.replace(',', ''))
        return [region, artist, song, link, 
                format(new_views, ','),
                format(new_difference, ','), now]
    else:
        return [region, artist, song, link, format(new_views, ','), 0, now]

# Creates the map from YouTube video IDs to their view counts.
def make_view_map(data, client, ids):
    request = client.videos().list(
            part="statistics",
            id=ids
    )
    stats = request.execute()
    return dict([(stat['id'], int(stat["statistics"]["viewCount"])) for stat in stats["items"]])

# Extracts a list of YouTube IDs from rows of video data (includes a URL).
def extract_ids(data):
    urls = [row[3] for row in data]
    return [url_to_id(url) for url in urls]

# Returns a YouTube ID from a YouTube URL.
def url_to_id(url):
    regular_expression = "^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*"
    match = re.match(regular_expression, url).groups()
    if (len(match) >= 2 and len(match[1]) == 11):
        return match[1]
    else:
        raise ValueError(f'Unable to extract ID from the url: {url}')

# Loads the CSV at the given path into a 2D array.
def load_csv(file_path):
    with open(file_path, newline='') as csvfile:
        result = []
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            result.append(row)
        return result

# Writes the data to a CSV at the given path.
def write_csv(file_path, data): 
    with open(file_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

# Returns an authenticated API client.
def create_client():
    creds = authenticate()
    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

# Returns credentials for our API client.
def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

if __name__ == '__main__':
    main()
    print('SUCCESS!')
