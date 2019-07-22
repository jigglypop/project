import csv
import requests

key = ''
movies = []
with open('boxoffice.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        movies.append(row['영화코드'])
        
result = {}
for movieCd in movies:
    response = requests.get(f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?movieCd={movieCd}&key={key}').json()
    movie_info = response['movieInfoResult']['movieInfo']
    result[movieCd] = {
            '영화 대표코드': movie_info.get('movieCd'),
            '영화명(국문)': movie_info.get('movieNm'),
            '영화명(영문)': movie_info.get('movieNmEn'),
            '영화명(원문)': movie_info.get('movieNmOg'),
            '관람등급': movie_info.get('audits')[0]['watchGradeNm'] if movie_info.get('audits') else None,
            '장르': movie_info.get('genres')[0]['genreNm'] if movie_info.get('genres') else None,
        }
with open('movie.csv', 'w', encoding='utf-8') as f:
    fieldnames = ['영화 대표코드' , '영화명(국문)' , '영화명(영문)' , '영화명(원문)' , '관람등급' ,  '장르'] # 맞춰서 작성..
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()
    for item in result.values():
        csv_writer.writerow(item)