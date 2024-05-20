import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QMessageBox, QWidget, QFormLayout
from PyQt5.QtGui import QPixmap
import xgboost as xgb
import pandas as pd

class PredictionDialog(QDialog):
    def __init__(self, parent=None, prediction_result=None):
        super().__init__(parent)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        if prediction_result <= 0.5:
            label = QLabel(f"정상입니다. 정상일 확률: {100*(1 - prediction_result):.3f}%")
            layout.addWidget(label)
            image_label = QLabel()
            pixmap = QPixmap('liver_good.png')
            image_label.setPixmap(pixmap)
            layout.addWidget(image_label)
        else:
            label = QLabel(f"간질환이 의심됩니다. 간질환 확률: {100*prediction_result:.3f}%")
            layout.addWidget(label)
            image_label = QLabel()
            pixmap = QPixmap('liver_sick.png')
            image_label.setPixmap(pixmap)
            layout.addWidget(image_label)


class InputWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Input Form")
        self.setGeometry(100, 100, 600, 550)

        self.init_ui()
        self.load_model()

    def init_ui(self):
        layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        form_layout = QFormLayout()

        self.input_widgets = {}

        # Define input fields
        fields = [
            ("Age (나이):", "age", "정상 범위: 0 ~ 100"),
            ("Sex (남성0/여성1):", "sex", "정상 범위: 0 or 1"),
            ("ALB (알부민수치):", "alb", "정상 범위: 3.5 ~ 5.2"),
            ("ALP (알칼리인산화효소):", "alp", "정상 범위: 30 ~ 115"),
            ("ALT (알라닌아미노전이효소):", "alt", "정상 범위: 0 ~ 40"),
            ("AST (아스파르테이트아미노전이효소):", "ast", "정상 범위: 0 ~ 40"),
            ("BIL (빌리루빈):", "bil", "정상 범위: 0.1 ~ 1.2"),
            ("CHE (콜린에스터아제):", "che", "정상 범위: 210 ~ 450"),
            ("CHOL (콜레스테롤):", "chol", "정상 범위: 40 이상"),
            ("CREA (크레아티닌):", "crea", "정상 범위: 0.5 ~ 1.4"),
            ("GGT (감마-글루타밀전달효소):", "ggt", "정상 범위: 11 ~ 63"),
            ("PROT (단백질수치):", "prot", "정상 범위: 6.0 ~ 8.0")
        ]

        for label_text, key, normal_range_text in fields:
            label = QLabel(label_text)
            line_edit = QLineEdit()
            normal_range_label = QLabel(normal_range_text)
            form_layout.addRow(label, line_edit)
            form_layout.addRow(QLabel(), normal_range_label)  # Add empty label for alignment
            self.input_widgets[key] = line_edit

        layout.addLayout(form_layout)

        # Submit Button
        self.submit_button = QPushButton("Submit")
        layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.get_input_values)
    
        # Image Label
        self.pixmap = QPixmap('liver.jpg')
        self.image_label = QLabel()
        self.image_label.setPixmap(self.pixmap)
        layout.addWidget(self.image_label)

    def load_model(self):
        try:
            self.model = xgb.Booster()
            self.model.load_model('xgb_model.model')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"모델을 로드하는 도중 오류가 발생했습니다: {e}")
            sys.exit(1)

    def get_input_values(self):
        try:
        # Retrieve input values
            data = {}
            for key, widget in self.input_widgets.items():
                input_text = widget.text().strip()
                if not input_text:
                    QMessageBox.critical(self, "Input Error", "모든 입력값은 필수입니다.")
                    return
                if not input_text.replace('.', '', 1).isdigit():  # 숫자 또는 소수점으로만 구성된 문자열인지 확인
                    QMessageBox.critical(self, "Input Error", f"{key} 입력값은 숫자여야 합니다.")
                    return
                data[key.upper()] = [float(input_text)]

            # Make prediction
            prediction = self.model.predict(xgb.DMatrix(pd.DataFrame(data)))[0]

            # Show prediction result dialog
            dialog = PredictionDialog(prediction_result=prediction)
            dialog.exec()
        except ValueError:
            QMessageBox.critical(self, "Input Error", "입력값은 숫자여야 합니다.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"예상치 못한 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InputWindow()
    window.show()
    sys.exit(app.exec_())
