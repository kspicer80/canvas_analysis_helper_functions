from api_key import API_KEY
from api_key import header_argument
import requests
import re
from pprint import pprint

def download_files_from_canvasapi(url):
    response = requests.get(url, headers=header_argument, timeout=15)

    if response.status_code == 200:
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            match = re.search('filename="(.+)"', content_disposition)
            if match:
                filename = match.group(1)
            else:
                filename = 'downloaded_file'
        else:
            filename = 'downloaded_file'

        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f'File downloaded successfully as {filename}')
    else:
        print('Failed to download the file from {url}')

API_KEY = API_KEY

course_id = # This will store the Canvas Course ID number for your course
assignment_id = # Here's the unique ID number for the assignment you want to download
user_id = # This is the unique ID number for the student whose assignment you want to download

URL = # Your Canvas API URL goes here, with the course ID, assignment ID, and user ID numbers inserted into the URL (f strings are perfect)

response = requests.get(URL, headers=header_argument, timeout=15)
data = response.json()

#pprint(data['attachments'][0]['url'])

download_url = data['attachments'][0]['url']

response = requests.get(download_url, headers=header_argument, timeout=15)

if response.status_code == 200:
    # Try to get the filename from the content-disposition header
    content_disposition = response.headers.get('content-disposition')
    if content_disposition:
        match = re.search('filename="(.+)"', content_disposition)
        if match:
            filename = match.group(1)
        else:
            filename = 'downloaded_file'
    else:
        filename = 'downloaded_file'

    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f'File downloaded successfully as {filename}')
else:
    print('Failed to download the file')




