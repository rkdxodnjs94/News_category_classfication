from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

category = ['Politics', 'Economic', 'Social',
            'Culture', 'World', 'IT']
# 정치섹션 주소 따오기

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'}
df_titles = pd.DataFrame()

for i in range(6):
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    resp = requests.get(url, headers=headers)
    # print(list(resp))

    soup = BeautifulSoup(resp.text, 'html.parser')
    # print(soup)

    title_tags = soup.select('.cluster_text_headline')
    # print(title_tags)

    titles = []
    for title_tag in title_tags:
        # 가~Z 외의 것들을 ' '로 대체 하겠다(sub)
        titles.append(re.compile('[^가-힁a-zA-Z ]').sub(' ', title_tag.text))
# print(titles)
    df_section_titles = pd.DataFrame(titles, columns=['title'])
    df_section_titles['category'] = category[i]
    # 중복된 컬럼 나올때 마다 새로 덮어 씌우기(ignore_index)
    df_titles = pd.concat([df_titles, df_section_titles],
                          axis='rows', ignore_index=True)
print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news.csv', index=False)

