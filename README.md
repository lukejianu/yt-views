### Usage Steps
1. Click the green "Code" button in the top, then click ``Download ZIP``.
2. Extract the zip.
3. Follow Step 1 from [Python Quickstart](https://developers.google.com/youtube/v3/quickstart/python).
    - Save the JSON file from 2b into a file called credentials.json in the new ``yt-views`` folder.
4. Export the Google Sheets to a CSV called artists.csv and move it into the ``yt-views`` folder.
    - Note that the current implementation expects the following schema:
    - ``City, Artist, Song, Link, Views, Difference, Last Updated``
        - Last Updated should be in the ``mm/dd/yy`` format (IE: 04/22/23).
5. Double click on the ``main`` file in the ``yt-views`` folder.
6. Import the ``new_artists.csv`` file back into Google Sheets.
