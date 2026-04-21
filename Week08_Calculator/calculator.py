import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QGridLayout, QPushButton, QLabel, QVBoxLayout, QWidget

# pip install PyQt6
# python calculator.py

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.expression = ''
        self.setWindowTitle('Calculator')
        self.setFixedSize(340, 560)
        self.setStyleSheet('background-color: black;')

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 20, 12, 12)
        layout.setSpacing(0)

        self.display = QLabel('0')
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.display.setStyleSheet('color: white; font-size: 64px; padding: 10px;')
        self.display.setFixedHeight(140)
        layout.addWidget(self.display)

        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7',  '8',   '9', '×'],
            ['4',  '5',   '6', '-'],
            ['1',  '2',   '3', '+'],
            ['0',  '.',   '='],
        ]

        grid = QGridLayout()
        grid.setSpacing(10)

        for row, row_data in enumerate(buttons):
            if row < 4:
                for col, label in enumerate(row_data):
                    btn = self._make_btn(label)
                    btn.setFixedSize(65, 65)
                    grid.addWidget(btn, row, col)
            else:
                btn0 = self._make_btn('0')
                btn0.setFixedSize(140, 65)
                btn0.setStyleSheet(btn0.styleSheet() + 'text-align: left; padding-left: 22px;')
                grid.addWidget(btn0, 4, 0, 1, 2)

                btn_dot = self._make_btn('.')
                btn_dot.setFixedSize(65, 65)
                grid.addWidget(btn_dot, 4, 2)

                btn_eq = self._make_btn('=')
                btn_eq.setFixedSize(65, 65)
                grid.addWidget(btn_eq, 4, 3)

        layout.addLayout(grid)
        self.setLayout(layout)

    def _make_btn(self, label):
        btn = QPushButton(label)
        if label in ('÷', '×', '-', '+', '='):
            color, text_color = '#FF9500', 'white'
        elif label in ('AC', '+/-', '%'):
            color, text_color = '#A5A5A5', 'black'
        else:
            color, text_color = '#333333', 'white'

        btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {color};
                color: {text_color};
                font-size: 26px;
                border-radius: 32px;
            }}
        ''')
        btn.clicked.connect(lambda _, l=label: self.on_click(l))
        return btn

    def on_click(self, label):
        if label == 'AC':
            self.expression = ''
            self.display.setText('0')
        elif label == '+/-':
            if self.expression:
                self.expression = str(eval(f'-({self.expression})'))
                self.display.setText(self.expression)
        elif label == '%':
            if self.expression:
                self.expression = str(eval(f'({self.expression})/100'))
                self.display.setText(self.expression)
        elif label == '=':
            try:
                result = eval(self.expression.replace('÷', '/').replace('×', '*'))
                self.expression = str(int(result) if float(result) == int(result) else result)
                self.display.setText(self.expression)
            except Exception:
                self.display.setText('오류')
                self.expression = ''
        elif label in ('÷', '×', '+', '-'):
            self.expression += label
            self.display.setText(self.expression)
        else:
            self.expression += label
            self.display.setText(self.expression)


app = QApplication(sys.argv)
window = Calculator()
window.show()
sys.exit(app.exec())