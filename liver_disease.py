import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton

class InputWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Input Form")

        self.category_label = QLabel("Category:", self)
        self.category_label.move(20, 20)
        self.category_input = QLineEdit(self)
        self.category_input.move(150, 20)

        self.age_label = QLabel("Age:", self)
        self.age_label.move(20, 50)
        self.age_input = QLineEdit(self)
        self.age_input.move(150, 50)

        self.sex_label = QLabel("Sex:", self)
        self.sex_label.move(20, 80)
        self.sex_input = QLineEdit(self)
        self.sex_input.move(150, 80)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.move(150, 120)
        self.submit_button.clicked.connect(self.get_input_values)

        self.setGeometry(100, 100, 300, 170)

    def get_input_values(self):
        category = self.category_input.text()
        age = self.age_input.text()
        sex = self.sex_input.text()

        print("Category:", category)
        print("Age:", age)
        print("Sex:", sex)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InputWindow()
    window.show()
    sys.exit(app.exec_())
