import numpy as np
import pandas as pd
import xgboost as xgb
from xgboost import plot_importance, plot_tree
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

# 데이터 불러오기
excel_file = 'liver_disease_data.xlsx'
df = pd.read_excel(excel_file)

# 성별을 0과 1로 변환
df['Sex(성별)'] = df['Sex(성별)'].map({'Male': 0, 'Female': 1})

# 레이블을 숫자형으로 변환
df['Category'] = df['Category'].map({'Normal': 0, 'Disease': 1})

# Feature와 Label 분리
X = df.drop('Category', axis=1)  # Category를 제외한 모든 열을 feature로 사용
y = df['Category']  # Category 열을 label로 사용

# 트레이닝셋과 테스트셋으로 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)

# XGBoost 모델 설정
params = {
    'max_depth': 3,
    'eta': 0.1,
    'objective': 'binary:logistic',  # 이진 분류인 경우
    'eval_metric': 'logloss',
    'early_stopping_rounds': 100
}
num_rounds = 400
# XGBoost 데이터 형식으로 변환
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

evals = [(dtrain, 'train'), (dtest, 'eval')]
xgb_model = xgb.train(params=params, dtrain=dtrain, num_boost_round=num_rounds,
                      early_stopping_rounds=100, evals=evals)

predicts = xgb_model.predict(dtest)
print(np.round(predicts[:10], 3))

# 테스트 데이터 예측
preds = [1 if x > 0.5 else 0 for x in predicts]

# 정확도, 정밀도, 재현율 평가
print("정확도: {}".format(accuracy_score(y_test, preds)))
print("정밀도: {}".format(precision_score(y_test, preds)))
print("재현율: {}".format(recall_score(y_test, preds)))

xgb_model.save_model('xgb_model.model')
