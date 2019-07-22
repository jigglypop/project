import requests
# import pprint
import csv

movie_infos = [] # 영화 상세정보 딕셔너리가 들어갈 리스트
key = ''
api_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={key}&movieCd='
# print(api_url)

# csv 열기
with open('boxoffice.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        temp = {}
        # url로 요청하고 값 받아오기
        response = requests.get(api_url + row.get('movieCd')).json()
        response = response.get('movieInfoResult').get('movieInfo')
        watchGradeNm = response.get('audits')[0].get('watchGradeNm') if response.get('audits') else None
        genreNm = response.get('genres')[0].get('genreNm') if response.get('genres') else None
        peopleNm = response.get('directors')[0].get('peopleNm') if response.get('directors') else None
        # 한 영화의 상세 정보 딕셔너리
        temp = {
            'movieCd': response.get('movieCd'),
            'movieNm': response.get('movieNm'),
            'movieNmEn': response.get('movieNmEn'),
            'movieNmOg': response.get('movieNmOg'),
            'watchGradeNm': watchGradeNm,
            'openDt': response.get('openDt'),
            'showTm': response.get('showTm'),
            'genreNm': genreNm,
            'peopleNm': peopleNm
        }
        movie_infos.append(temp)

with open('movie.csv', 'w', encoding='utf-8') as f:
    # 헤더와 딕셔너리 키 값을 맞춰줘야함.
    fieldnames = ['movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genreNm', 'peopleNm'] 
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()
    for movie in movie_infos:
        csv_writer.writerow(movie)