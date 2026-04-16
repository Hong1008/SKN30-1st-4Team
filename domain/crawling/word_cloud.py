from wordcloud import WordCloud
import numpy as np
from PIL import Image

wordlist = []
year = '2018'

with open(f'ev_or_kr_csv/ev_or_kr_{year}.csv', 'r', encoding='UTF-8') as f:
    result = f.readline()

    while result:
        title = result.split(',')[1]

        for j in title.split():
            if '.' in j or len(j) == 1:
                pass
            else:
                wordlist.append(j.replace('"', ""))

        result = f.readline()
    
word_clean = set(wordlist)
wordCount = {}

for w in word_clean:
    wordCount[w] = wordlist.count(w)

# 불용어 제거(조사 제거)
stop_words = ['그리고', '있는', '이런', '그는', '아니', '같은', '내가', '나는', '하고', '나를']

# 제외하기
for w in stop_words:
    if w in wordCount:
        del wordCount[w]

# 이미지 불러오기
masking_image = np.array(Image.open(f'word_cloud_bg/{year}.png'))

# 워드 클라우드 만들기
wordcloud = WordCloud(font_path='font/NanumSquareRoundEB.ttf',
                      mask = masking_image,
                      max_font_size=150,
                      colormap='tab10',
                      min_font_size=8,
                      max_words=300,
                      prefer_horizontal=0.8,
                      relative_scaling=0.4,
                      background_color='white').generate_from_frequencies(wordCount)

wordcloud.to_file(f'word_cloud/{year}.jpg')
