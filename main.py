import pandas as pd
from bs4 import BeautifulSoup
from urllib import request

# 記事からHTMLを取得してパース
url = 'https://qiita.com/e869120/items/eb50fdaece12be418faa'
res = request.urlopen(url)
soup = BeautifulSoup(res, 'html.parser')
res.close()

data = []

# 分野別初中級者が解くべき過去問精選100問を取得
first_c = '全探索：全列挙'
domains = ['atcoder.jp', 'judge.u-aizu.ac.jp']
idx = 1
flag = False
category = None
for e in soup.find('div', id='personal-public-article-body').find_all(['h4', 'a']):
    if e.name == 'a':
        text = e.get_text()
        href = e['href']
    else:
        category = e.get_text().replace('"', '').strip()
        continue

    if category == first_c:
        flag = True

    if not flag or not any([href.find(d) >= 0 for d in domains]):
        continue
    else:
        data.append([idx, category, text, href])
        idx += 1
        if idx > 100:
            break

df = pd.DataFrame(data, columns=['番号', '分野', '問題', 'URL'])
df.to_csv('output.tsv', sep='\t', index=False)