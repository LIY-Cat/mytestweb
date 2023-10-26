import csv
from flask import Flask, render_template, send_from_directory
import os
import matplotlib.pyplot as plt

app = Flask(__name__)

#작업 디렉터리 변경
os.chdir(r'C:\Users\218\Desktop\webcc')  # 백슬래시를 이스케이프 문자로 처리하기 위해 'r' 접두어 사용

# 데이터 파일을 읽어서 리스트로 반환하는 함수
def read_data(filename):
    data = []
    with open(filename, 'r', encoding='euc-kr') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

# 데이터를 분석하고 그래프를 생성하는 함수
def analyze_and_plot_data(data):
    dates = []
    avg_temperatures = []

    for row in data:
        date = row['날짜']
        avg_temp = row['평균기온(℃)']
        
        # 빈 값이 있는 행을 건너뛰기
        if avg_temp:
            dates.append(date)
            avg_temperatures.append(float(avg_temp))

    plt.figure(figsize=(12, 6))
    plt.plot(dates, avg_temperatures, marker='o', linestyle='-')
    plt.title('서울 일일 평균 기온')
    plt.xlabel('날짜')
    plt.ylabel('평균기온(℃)')
    plt.xticks(rotation=45)  # x축 라벨을 45도 회전
    plt.tight_layout()

    # 그래프를 이미지로 저장
    image_path = os.path.join('static', 'temperature_plot.png').replace('\\', '/')
    # 디버깅: 이미지 경로를 출력합니다.
    print("이미지 경로:", image_path)
    plt.savefig(image_path, bbox_inches='tight')

    return image_path

# 데이터 파일 경로
data_file = 'data.csv'

# 데이터 분석 및 웹페이지 렌더링
@app.route('/')
def analyze_data():
    data = read_data(data_file)
    plot = analyze_and_plot_data(data)
    img_path = os.path.join(app.root_path, 'static', 'temperature_plot.png')
    return render_template('main.html', data=data, img_path=img_path)

if __name__ == '__main__':
    app.run(debug=True)
