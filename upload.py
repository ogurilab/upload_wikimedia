import requests
import re
from datetime import datetime
from dotenv import load_dotenv
import os

# .envファイルを読み込む
load_dotenv()

# Wikimedia Commonsのユーザー名とパスワード
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# セッションの開始
session = requests.Session()

# ログイントークンの取得
login_token_response = session.get('https://commons.wikimedia.org/w/api.php?action=query&meta=tokens&type=login&format=json')
login_token = login_token_response.json()['query']['tokens']['logintoken']

# ログイン処理
login_response = session.post('https://commons.wikimedia.org/w/api.php', data={
    'action': 'login',
    'lgname': USERNAME,
    'lgpassword': PASSWORD,
    'lgtoken': login_token,
    'format': 'json'
})

# CSRFトークンの取得
csrf_token_response = session.get('https://commons.wikimedia.org/w/api.php?action=query&meta=tokens&format=json')
csrf_token = csrf_token_response.json()['query']['tokens']['csrftoken']

# 日付をファイル名から抽出し、変換する関数
def extract_and_format_date_from_filename(filename):
    match = re.search(r'(\d{4})(\d{2})(\d{2})', filename)
    if match:
        return datetime.strptime(match.group(0), "%Y%m%d").strftime("%Y年%-m月%-d日")
    return None

# 画像のアップロード
def upload_file(file_path, file_name):
    formatted_date = extract_and_format_date_from_filename(file_name)
    if not formatted_date:
        return {"error": "Invalid file name format. Date could not be extracted."}

    upload_comment = "Uploaded a work by 愛知県半田市 from https://www.city.handa.lg.jp/kyushoku/kosodate/kyoiku/kyushoku/kyonokondate.html with UploadWizard"
    formatted_file_name = f'愛知県半田市 {formatted_date}の給食.jpeg'
    file_description = f"""=={{{{int:filedesc}}}}==
{{{{Information
|description={{{{ja|1=愛知県半田市の{formatted_date}に提供された学校給食です。}}}}
|date={formatted_date}
|source=https://www.city.handa.lg.jp/kyushoku/kosodate/kyoiku/kyushoku/kyonokondate.html
|author=愛知県半田市
|permission=
|other versions=
}}}}

=={{{{int:license-header}}}}==
{{{{cc-by-4.0}}}}

{{{{Uncategorized|year={datetime.now().year}|month={datetime.now().strftime('%B')}|day={datetime.now().day}}}}}"""

    with open(file_path, 'rb') as file:
        response = session.post('https://commons.wikimedia.org/w/api.php', files={
            'file': (formatted_file_name, file, 'multipart/form-data')
        }, data={
            'action': 'upload',
            'filename': formatted_file_name,
            'text': file_description,
            'comment': upload_comment,
            'token': csrf_token,
            'format': 'json'
        })
        return response.json()

# 画像のアップロードを行う

# upload_response = upload_file("ファイルパス", "ファイル名")
print("upload_fileを呼び出すとファイルがアップロードされます。アップロードの内容はあくまで例なので、変更は自由に行ってください。")
