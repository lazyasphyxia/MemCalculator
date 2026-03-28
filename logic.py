class CalculatorLogic:
    def __init__(self):
        self.expression = ""

    def append(self, char):
        self.expression += char
        return self.expression

    def clear(self):
        self.expression = ""
        return self.expression

    def toggle_sign(self):
        if self.expression:
            if self.expression.startswith('-'):
                self.expression = self.expression[1:]
            else:
                self.expression = '-' + self.expression
        return self.expression

    def apply_percent(self):
        try:
            self.expression = str(float(self.expression) / 100)
        except ValueError:
            self.expression = "Error"
        return self.expression

    def evaluate(self):
        try:
            # Заменяем визуальные символы на операторы Python
            safe_expression = self.expression.replace('×', '*').replace('÷', '/').replace('−', '-')
            result = str(eval(safe_expression))
            self.expression = result
            return result
        except Exception:
            self.expression = ""
            return "Error"