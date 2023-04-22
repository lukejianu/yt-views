### Prerequisites
- Install the prerequisites and follow step 1 from [Python Quickstart](https://developers.google.com/youtube/v3/quickstart/python).

### Usage
- Export the Google Sheets to a CSV. 
    - Note that the current implementation expects the following schema: 
    - ``City, Artist, Song, Link, Views, Difference, Last_Updated`` 
        - Last_Updated should be in the ``mm/dd/yy`` format (IE: 04/22/23).
- ``python3 main.py --input YOUR_CSV_PATH --output SOME_OUTPUT_PATH``
- Import the new CSV back into Google Sheets.
