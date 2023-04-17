import requests

access_token = 'ya29.a0Ael9sCOoAgzSnItOQFq6S3dFMB-MTpJkpHlCMYqwTQH9NDm60_vA1wwwP7PNV9Y6IuUnoOSFOO5c_XNV30JNW3lqAlMh4vsPqnVwaSOGrH-9dxqoWUo8DKy2AS7EMJ-judLepSXeW0Q7TxEHTRQxqSY0p0buaCgYKAekSARISFQF4udJh1t-iCjBxUExRuaYZ2lop-A0163'
file_id = '1iiY6-P166rZUQR_9t_YtdEr4oVphEIKQJV0j5CvfQtI'

headers = {
    'Authorization': f'Bearer {access_token}'
}

url = f'https://www.googleapis.com/drive/v3/files/{file_id}'

params = {
    'fields': 'mimeType'
}

response = requests.get(url, headers=headers, params=params).json()

if response['mimeType'] == 'application/vnd.google-apps.document':
    print('The Google Docs ID refers to a document.')
elif response['mimeType'] == 'application/vnd.google-apps.spreadsheet':
    print('The Google Docs ID refers to a spreadsheet.')
elif response['mimeType'] == 'application/vnd.google-apps.presentation':
    print('The Google Docs ID refers to a presentation (slides).')
else:
    print('The Google Docs ID does not refer to a Google document, spreadsheet, or presentation.')