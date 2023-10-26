import csv
from flask import Flask, render_template, request
import os
import matplotlib.pyplot as plt

app = Flask(__name__)

# 작업 디렉터리 변경
os.chdir(r'C:\Users\218\Desktop\webcc')

# 업로드된 파일을 저장할 디렉터리 설정
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        
        if avg_temp:
            dates.append(date)
            avg_temperatures.append(float(avg_temp))

    plt.figure(figsize=(12, 6))
    plt.plot(dates, avg_temperatures, marker='o', linestyle='-')
    plt.title('서울 일일 평균 기온')
    plt.xlabel('날짜')
    plt.ylabel('평균기온(℃)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    image_path = os.path.join('static', 'temperature_plot.png').replace('\\', '/')
    plt.savefig(image_path, bbox_inches='tight')

    return image_path

# HTML 폼을 표시하는 뷰 함수
@app.route('/')
def upload_form():
    return render_template('upload.html')

# 업로드된 파일을 처리하는 뷰 함수
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_data.csv')
        file.save(filename)
        data = read_data(filename)
        plot = analyze_and_plot_data(data)
        img_path = os.path.join(app.root_path, 'static', 'temperature_plot.png')
        return render_template('result.html', data=data, img_path=img_path)

if __name__ == '__main__':
    app.run(debug=True)
