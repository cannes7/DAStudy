# -*- coding: utf-8 -*-
"""2-1) 인기도서리스트 Requests패키지.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16-L0DUse27b2cznV5O7h82TJ_eYOQkTZ

# 도서관 정보나루 공개 API에서 JSON 데이터 자동 다운로드하는 프로그램 만들기
"""

import requests #requests 패키지 호출

#url변수에 도서관 정보나루 API 인증키 넣은 호출 URL 저장
url="http://data4library.kr/api/loanItemSrch?format=json&startDt=2021-04-01&endDt=2021-04-30&age=20&authKey=d925598243957fd1868ddb9ed43dd91eedbec8650c69dec2cdbbe79fc2fdbb47"

"""#url이 HTTP GET방법으로 파라미터 값을 전달하기 때문에 url을 **requests.get()**함수에 전달해야함(뭔솔)
get()함수는 API호출의 결과를 담고 있는 requests패키지의 Response클래스 객체를 반환함(뭔솔)
"""

r=requests.get(url)

"""# **JSON문자열을 파이썬 객체로 변환하는 json()매서드** #"""

#Response클래스 객체가 제공하는 메서드 중 json()메서드는 웹 서버로부터 받은 JSON 문자열을 파이썬 객체로 변환하여 반환해줌
#그러면 저 url타고 들어가면 볼 수 있었던 데이터를 출력함
data = r.json()
print(data)

#변수명만 쓰면 보기 쉽게 들여쓰기까지 해서 보여주는게 코랩 기능
data

"""## {response{docs{doc:책정보}}}딕셔너리 구조를 판다스 데이터프레임으로 전환하기 위해##
##지저분한 정보 치우기 위해 doc키에 매핑된 딕셔너리를 추출하여 빈 리스트에 추가 ##


"""

#for문 사용
#data딕셔너리를 빈 books리스트에 추가하겠음
books = []
for d in data['response']['docs']:
  books.append(d['doc'])

books

"""#**판다스 데이터프레임에 books리스트 넘기기**#"""

import pandas as pd
books_df = pd.DataFrame(books)
books_df

"""#**20대가 좋아하는 도서 200권 목록을 JSON파일에 저장하기** #
to_json메소드는 기본적으로 유니코드를 16진수로 저장하기 때문에, 텍스트 편집기에서 20s_best_book.json 파일 열면 한글 다 깨짐.
따라서 to_json()메소드가 한글 제대로 저장하게 하려면 force_ascii매개변수를 False로 지정해야함
"""

#to_json() : 판다스 데이터프레임을 JSON파일로 저장하는 메서드
books_df.to_json('20s_best_book.json')

"""# **검색 결과 페이지 가져오기** #
.gdown패키지를 사용해 20대가 가장 좋아하는 도서 목록을 코랩으로 다운로드 <br>
구글 드라이브 링크 https://bit.ly/3q9SZix 에서 해당 파일 다운하는 패키지
"""

import gdown
gdown.download('https://bit.ly/3q9SZix', '20s_best_book.json', quiet=False)

"""# **판다스 데이터프레임으로 불러온 뒤, head() 메서드로 처음 다섯 개 행 출력** #"""

import pandas as pd
books_df=pd.read_json('20s_best_book.json')
books_df.head()

"""# **특정 열만 불러오기** #
## 데이터프레임에 'no' ~ 'isbn13'까지만 추출하는 방법 ##
['no', 'ranking', 'bookname']처럼 원하는 열 이름을 리스트로 만들어 데이터프레임의 인덱스처럼 사용
"""

books = books_df[['no', 'ranking', 'bookname', 'authors', 'publisher', 'publication_year', 'isbn13']]
books.head()

"""# **loc메서드로 원하는 행'열 편하게 선택하기** #
앞에서처럼 열 저렇게 하나하나 쓰는건 귀찮음<br>
loc는 메서드이지만 대괄호로 행의 목록과 열의 목록을 받음<br>



```
books_df.loc[[0,1],['bookname','authors']]
```
첫 번째 매개변수로 **행 인덱스 0과 1을 리스트로 전달**, 두 번째 매개변수로 **열 이름을 리스트로 전달** <br>-> 첫, 두 번째 행의 도서명과 저자만 추출하여 데이터프레임 만들 수 있음



"""

#예시 실행
books_df.loc[[0,1],['bookname','authors']]

"""#**참고) iloc 메서드로는 인덱스 번호로 열도 추출할 수 있다.**


"""

#예시 실행
books_df.iloc[[0,1],[2,3,4]]

"""#**참고) 슬라이스 연산자(:) 사용도 가능!**#

"""

#예시 실행
books_df.loc[0:1, 'bookname':'authors']

#시작과 끝을 지정하지 않고 그냥 :만 쓰면 전체임
books = books_df.loc[:,'no':'isbn13']
books.head()

###**참고)파이썬 슬라이싱처럼 스텝도 지정 가능**###

books_df.loc[::2, 'no': 'isbn13'].head()

"""#**검색 결과 페이지 html 가져오기: request.get()함수**
첫 번째 도서에 대한 검색 결과 페이지 HTML 가져오기
<br>
1. 첫 번째 도서의 ISBN과 yes24 검색 결과 페이지 url을 위한 변수 정의<br>
https://www.yes24.com/Product/Search?domain=BOOK&query=9791190090018 가 첫 도서ISBN으로 검색했을 때 뜨는 링크<br>
여기서 마지막 ISBN 자리를 변수{}로 지정하는거임
2. requests.get()함수 호출할 때 파이썬 문자열의 format()메서드를 사용해 isbn 변수에 저장된 값을 url 변수에 전달

참고)
format() 메서드는 입력한 값의 형식을 지정합니다.

괄호 {}로 표시된 위치에 지정된 형식의 문자열을 대체합니다.


```
age = 10
string1 = 'I am {} years old.'.format(age)

print(string1)

>>> I am 10 years old.
```
"""

import requests
isbn = 9791190090018
url = 'http://www.yes24.com/Product/Search?domain=BOOK&query={}'
r = requests.get(url.format(isbn))

print(r.text)
#도서 검색 결과 페이지에서 html출력하기

"""# **뷰티플수프** #
원하는 데이터가 html 어디있는지 검사 도구로 찾아(f12)
"""

from bs4 import BeautifulSoup

#클래스의 객체 생성
#첫번째 매개변수=파싱할 html문서 / 두 번째 매개변수=파싱에 사용할 파서(입력 데이터를 받아 데이터 구조를 만드는 소프트웨어 라이브러리)
soup = BeautifulSoup(r.text, 'html.parser')

"""#**find()메서드: 페이지에서 원하는 부분(태그)의 위치를 찾게 하기**#
첫 번째 매개변슈= 찾을 태그 이름 <br>
두 번째 매개변수 attrs 매개변수에는 찾으려는 태그의 속성을 딕셔너리로 지정
"""

prd_link = soup.find('a', attrs={'class':'gd_name'})
#class속성이 gd_name인 <a>태그 추출
#prd_link는 링크가 포함된 뷰티플수프의 Tag 클래스 객체

#태그 안에 포함된 html 출력
print(prd_link)

#prd_link를 딕셔너리처럼 사용해 태그 안의 속성 참조 가능-> href 속성의 값(링크 주소) 구할 수 있음
print(prd_link['href'])
#그러면 상세 페이지로 가는 링크 추출한 것!!

"""#도서 상세 페이지 html 가져오기#
방금 구한 주소로 request.get()함수 활용해 쪽수가 담긴 상세페이지 html을 가져올 수 있음
"""

#우리가빛으로어쩌구 책 상세 페이지 가져오기
url = 'http://www.yes24.com'+prd_link['href']
r = requests.get(url)

#아까처럼 응답객체 r 사용해 가져온 html 추출(도서상세페이지의)
print(r.text)

"""#도서 상세페이지에서 쪽수 담긴 html 위치 찾아내기#"""

from bs4 import BeautifulSoup

soup = BeautifulSoup(r.text,'html.parser')
prd_detail = soup.find('div', attrs={'id':'infoset_specific'})
print(prd_detail)

"""# find_all()메서드 -> 특정 html태그 모두 찾아 리스트로 반환
find()메서드:지정된 이름을 가진 첫 번째 태그 반환
find_all()메서드: 지정된 이름을 가진 모든 태그 반환
"""

#아까 찾은 <div> 안에서 쪽수, 무게, 크기 란에 해당하는 <tr>태그 찾아 <td>태그 안 텍스트 가져오기
#prd_detail에 포함된 <tr>태그 모두 리스트로 만들기
prd_tr_list = prd_detail.find_all('tr')
print(prd_tr_list)

"""# for문으로 prd_tr_list를 순회하며 <th> 안의 텍스트가 '쪽수, 무게, 크기'에 해당하는지 검사
찾으면 <td>안의 텍스트를 page_td 변수에 저장
# get_text()메서드로 <td> 안에 있는 텍스트 반환
"""

for tr in prd_tr_list:
  if tr.find('th').get_text() == '쪽수, 무게, 크기':
    page_td= tr.find('td').get_text()
    break

print(page_td)

"""# 쪽수만 남기고 지우기
split()메서드->공백을 기준으로 문자열을 나누어 리스트로 반환. 여기서 첫번째 것만 출력
"""

print(page_td.split()[0])

"""지금까지 한 방법으로 모든 책의 쪽수를 추출하면 되는데, pandas는 한 행씩 처리하는 데 최적화되어있지 않음->데이터프레임에 for문은 부적합<br>
but 데이터프레임은 각 행'열에 원하는 함수 자동으로 적용하는 여러 가지 방법 제공<br>
#앞에서 한 모든 과정을 하나의 함수로 만들기

"""

#ISBN 값 받아 쪽수 반환하는 함수
def get_page_cnt(isbn):
  url = 'https://www.yes24.com/Product/Search?domain=BOOK&query={}'
  r = requests.get(url.format(isbn)) #url에 isbn 넣어서 html가져옴
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(r.text, 'html.parser')
  prd_info = soup.find('a', attrs={'class':'gd_name'})
  if prd_info == None:
    return ''
  url = 'http://www.yes24.com'+prd_info['href']
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  prd_detail = soup.find('div', attrs={'id' : 'infoset_specific'})
  prd_tr_list = prd_detail.find_all('tr')
  for tr in prd_tr_list:
    if tr.find('th').get_text() == '쪽수, 무게, 크기':
      return tr.find('td').get_text().split()[0]
  return ''

get_page_cnt(9791190090018)

"""# 데이터프레임 행 혹은 열에 함수 적용하기:apply()메서드
books_df 데이터프레임에서 최고인기 10권 가져와 데이터프레임 만들기
"""

top10_books = books.head(10)

"""# 인기 10권의 쪽수 한 번에 구하기
데이터프레임 각 행의 반복 작업에는 apply() 메서드 이용<br>
apply() 메서드의 첫 번째 매개변수: 실행할 함수<br>
-> 데이터프레임의 한 행을 받아 get_page_cnt()함수를 사용해 쪽수 구하는 함수를 만들어야함.<br><br>
cf) apply() 메서드를 사용하면 행 또는 열에 함수를 일괄적용할 수 있음<br>
axis 매개변수에 1 지정->행에, 0->열에 적용<br>
<br>
apply(실행할 함수, axis = 0 or 1)
"""

#isbn13열의 값을 get_page_cnt()함수로 전달하는 함수 만들기
# 이 함수를 apply가 사용해서 데이터프레임 속 10행에 사용할 것임
def get_page_cnt2(row):
  isbn = row['isbn13']
  return get_page_cnt(isbn)

page_count = top10_books.apply(get_page_cnt2, axis=1)
print(page_count)

"""page_count 시리즈 객체를 top10_books 데이터프레임의 열로 합쳐
도서명과 쪽수를 한 번에 보자
"""

#page_count 시리즈 객체에 이름 지정->top10_books에 추가될 때 열 이름으로 사용됨
#시리즈 객체의 name 속성을 사용하면 이름을 간단하게 지정할 수 있음
page_count.name = 'page_count'
print(page_count)

"""# 데이터프레임에 열 합치기 : merge() 함수 사용
첫, 두 번째 매개변수 = 합칠 데이터프레임이나 시리즈 객체<br>
두 객체의 인덱스를 기준으로 합칠 경우, left_index와 right_index 매개변수를 True로 지정<br>
두 데이터프레임의 행 인덱스가 일치하는 행들끼리 병합된다는 의미


"""

top10_with_page_count = pd.merge(top10_books, page_count, left_index=True, right_index=True)
top10_with_page_count

"""# robots.txt 파일을 통해 웹 스크래핑이 가능한지 확인해보자
ex.yes24.com/robots.txt
"""