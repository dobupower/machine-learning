from flask import Flask, render_template, request
import xgboost as xgb
import pandas as pd

app = Flask(__name__)

# 저장된 모델 불러오기
xgb_model = xgb.Booster()  
xgb_model.load_model('xgb_model.model')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['POST'])  # 변경된 엔드포인트
def predict():
    # HTML 폼에서 전송된 데이터 받기
    age = float(request.form['age'])
    sex = int(request.form['sex'] == 'Female')  # Female은 1로, Male은 0으로 변환
    alb = float(request.form['alb'])
    alp = float(request.form['alp'])
    alt = float(request.form['alt'])
    ast = float(request.form['ast'])
    bil = float(request.form['bil'])
    che = float(request.form['che'])
    chol = float(request.form['chol'])
    crea = float(request.form['crea'])
    ggt = float(request.form['ggt'])
    prot = float(request.form['prot'])

    # 입력 받은 데이터로 새로운 데이터 프레임 생성
    new_data = pd.DataFrame({
        'Age(나이)': [age],
        'Sex(성별)': [sex],
        'ALB(알부민수치)': [alb],
        'ALP(알칼리인산화효소)': [alp],
        'ALT(알라닌아미노전이효소)': [alt],
        'AST(아스파르테이트아미노전이효소)': [ast],
        'BIL(빌리루빈)': [bil],
        'CHE(콜린에스터아제)': [che],
        'CHOL(롤레스테롤)': [chol],
        'CREA(크레아티닌)': [crea],
        'GGT(감마-글루타밀전달효소)': [ggt],
        'PROT(단백질수치)': [prot]
    })

    # XGBoost 데이터 형식으로 변환
    dnew = xgb.DMatrix(new_data)

    # 새로운 데이터에 대한 예측 결과 출력
    new_predict = xgb_model.predict(dnew)
    if new_predict < 0.5:
        prediction = "Normal로 예측됩니다."
    else:
        prediction = "Disease로 예측됩니다."

    return render_template('result.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
