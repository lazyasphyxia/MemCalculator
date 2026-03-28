import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from logic import CalculatorLogic
from animations import AnimatedButton  # Импортируем нашу анимированную кнопку


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = CalculatorLogic()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Calculator")
        self.setFixedSize(300, 480)
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont("Arial", 32))
        self.display.setStyleSheet("background-color: black; color: white; border: none; padding: 15px;")
        layout.addWidget(self.display)

        grid = QGridLayout()
        grid.setSpacing(10)

        buttons = [
            ('C', 0, 0), ('±', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('−', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('.', 4, 2), ('=', 4, 3)
        ]

        for text, row, col in buttons:
            btn = self.create_button(text)
            btn.clicked.connect(lambda _, t=text: self.handle_click(t))
            grid.addWidget(btn, row, col)

        # Кнопка нуля
        zero_btn = self.create_button('0')
        zero_btn.setFixedSize(130, 60)
        zero_btn.clicked.connect(lambda: self.handle_click('0'))
        grid.addWidget(zero_btn, 4, 0, 1, 2)

        layout.addLayout(grid)
        self.setLayout(layout)

    def create_button(self, text):
        button = AnimatedButton(text)
        button.setFont(QFont("Arial", 18))

        # Стилизация (вынесена в условия для краткости)
        if text in {'÷', '×', '−', '+', '='}:
            style = "background-color: orange; color: white;"
        elif text in {'C', '±', '%'}:
            style = "background-color: #a5a5a5; color: black;"
        else:
            style = "background-color: #333333; color: white;"

        button.setStyleSheet(style + " border-radius: 30px;")
        return button

    def handle_click(self, char):
        if char == 'C':
            res = self.logic.clear()
        elif char == '=':
            res = self.logic.evaluate()
        elif char == '±':
            res = self.logic.toggle_sign()
        elif char == '%':
            res = self.logic.apply_percent()
        else:
            res = self.logic.append(char)

        self.display.setText(res)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())