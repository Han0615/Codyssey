import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QGridLayout, QPushButton, QLabel, QVBoxLayout, QWidget


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.current_value = '0'  # 현재 화면에 표시되는 숫자
        self.stored_value = 0    # 계산을 위해 저장된 이전 숫자
        self.pending_operation = None  # 대기 중인 연산자
        self.is_typing = False   # 사용자가 숫자를 입력 중인지 여부

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Calculator')
        self.setFixedSize(340, 560)
        self.setStyleSheet('background-color: black;')

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 20, 12, 12)
        layout.setSpacing(0)

        # 결과 표시창
        self.display = QLabel('0')
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.display.setStyleSheet('color: white; font-size: 64px; padding: 10px;')
        self.display.setFixedHeight(140)
        layout.addWidget(self.display)

        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
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
                # '0' 버튼은 두 칸을 차지함
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
        btn.clicked.connect(lambda _, l=label: self.handle_button(l))
        return btn

    def update_display(self):
        """출력 값의 길이에 따라 폰트 크기를 조정하고 숫자를 포맷팅합니다."""
        display_text = self.current_value

        # 천 단위 콤마 추가 (소수점 제외)
        if '오류' not in display_text and 'inf' not in display_text:
            try:
                parts = display_text.split('.')
                parts[0] = format(int(parts[0]), ',')
                display_text = '.'.join(parts)
            except ValueError:
                pass

        # 폰트 크기 조정 (보너스 과제)
        length = len(display_text)
        if length > 12:
            font_size = 30
        elif length > 8:
            font_size = 40
        else:
            font_size = 64
        
        self.display.setStyleSheet(f'color: white; font-size: {font_size}px; padding: 10px;')
        self.display.setText(display_text)

    def handle_button(self, label):
        if label.isdigit():
            self.append_number(label)
        elif label == '.':
            self.append_dot()
        elif label == 'AC':
            self.reset()
        elif label == '+/-':
            self.negative_positive()
        elif label == '%':
            self.percent()
        elif label in ('÷', '×', '-', '+'):
            self.prepare_operation(label)
        elif label == '=':
            self.equal()
        
        self.update_display()

    def append_number(self, number):
        if not self.is_typing or self.current_value == '0':
            self.current_value = number
            self.is_typing = True
        else:
            self.current_value += number

    def append_dot(self):
        if not self.is_typing:
            self.current_value = '0.'
            self.is_typing = True
        elif '.' not in self.current_value:
            self.current_value += '.'

    def reset(self):
        self.current_value = '0'
        self.stored_value = 0
        self.pending_operation = None
        self.is_typing = False

    def negative_positive(self):
        if self.current_value != '0':
            if self.current_value.startswith('-'):
                self.current_value = self.current_value[1:]
            else:
                self.current_value = '-' + self.current_value

    def percent(self):
        try:
            val = float(self.current_value) / 100
            self.current_value = self.format_result(val)
        except Exception:
            self.current_value = '오류'

    def prepare_operation(self, op):
        if self.pending_operation and self.is_typing:
            self.equal()
        
        self.stored_value = float(self.current_value)
        self.pending_operation = op
        self.is_typing = False

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            return '오류'
        return a / b

    def format_result(self, value):
        """결과값을 소수점 6자리 반올림 및 정수 처리합니다."""
        if value == '오류':
            return '오류'
        
        # 소수점 6자리 반올림 (보너스 과제)
        value = round(value, 6)
        
        # 정수로 표현 가능하면 정수로 변환
        if value == int(value):
            return str(int(value))
        return str(value)

    def equal(self):
        if self.pending_operation is None or not self.is_typing:
            return

        second_value = float(self.current_value)
        result = 0

        if self.pending_operation == '+':
            result = self.add(self.stored_value, second_value)
        elif self.pending_operation == '-':
            result = self.subtract(self.stored_value, second_value)
        elif self.pending_operation == '×':
            result = self.multiply(self.stored_value, second_value)
        elif self.pending_operation == '÷':
            result = self.divide(self.stored_value, second_value)

        self.current_value = self.format_result(result)
        self.pending_operation = None
        self.is_typing = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())