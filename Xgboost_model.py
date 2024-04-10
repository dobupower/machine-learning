import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 데이터 불러오기
excel_file = '/root/liver_disease_data.xlsx'
df = pd.read_excel(excel_file, engine='openpyxl')
# 성별을 0과 1로 변환
df['Sex(성별)'] = df['Sex(성별)'].map({'Male': 0, 'Female': 1})
# 레이블을 숫자형으로 변환
df['Category'] = df['Category'].map({'Normal': 0, 'Disease': 1})
# Feature와 Label 분리
X = df.drop('Category', axis=1)  # Category를 제외한 모든 열을 feature로 사용
y = df['Category']  # Category 열을 label로 사용
# 트레이닝셋과 테스트셋으로 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# XGBoost 모델 설정
params = {
    'max_depth': 3,
    'eta': 0.1,
    'objective': 'binary:logistic',  # 이진 분류인 경우
    'eval_metric': 'logloss',  # 오타 수정
    'early_stopping_rounds': 100
}
num_rounds = 400
# XGBoost 데이터 형식으로 변환
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)
evals = [(dtrain, 'train'), (dtest, 'eval')]
xgb_model = xgb.train(params=params, dtrain=dtrain, num_boost_round=num_rounds,
                      early_stopping_rounds=100, evals=evals)
# 학습된 모델을 파일로 저장
xgb_model.save_model('xgb_model.model')
