import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template
import re

data_dict = []

def crawling():
    for i in range(1,73):
        url = f'https://www.jeju.go.kr/culture/dialect/dictionary.htm?pageSize=100&page={i}'
        res = requests.get(url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.content, 'html.parser')

        keys = soup.find_all('a', class_ = 'view-history', string=True)
        values = soup.find_all('td', class_ = 'dotdotdot title', string=True)
        
        data = list(zip((j.text.strip() for j in keys), (k.text.strip() for k in values)))
        data_dict.append(data)
            
crawling()

keys = []
values = []

for i in range(len(data_dict)):
    for j in range(len(data_dict[i])):
        keys.append(data_dict[i][j][0])
        values.append(data_dict[i][j][1])

ziped = zip(keys, values)
data_dict = dict(ziped)


def translate(text):
    # 입력 텍스트를 공백을 기준으로 분할
    words = text.split()
    # 변환된 텍스트를 저장할 리스트
    translated_words = []
    
    for word in words:
        # 사전에서 단어를 찾아서 변환
        if word in data_dict:
            translated_words.append(data_dict[word])
        else:
            # 사전에 없는 단어는 그대로 사용
            translated_words.append(word)
    
    # 변환된 단어들을 공백으로 연결하여 최종 문장 생성
    return ' '.join(translated_words)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', data = '번역 결과가 여기에 표시됩니다.')

@app.route('/result', methods=['POST'])
def submit():
    textarea_value = request.form['textarea']
    return render_template('index.html', data = translate(textarea_value))

if __name__ == '__main__':
    app.run(debug=True)