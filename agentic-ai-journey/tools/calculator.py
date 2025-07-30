import math 

class CalculatorTool:
    def __init__(self):
        self.name = 'calculatoe'
        self.description = 'Advance calculator for mathematical operations'

    def calculate(self, expression):
        """Safe calculator that handles various math operation
        """
        try:
            #Replace common math symbol
            expression = expression.replace('^','**')
            expression = expression.replace('*','*')
            expression = expression.replace('÷', '/')

            safe_dict = {
                "__builtins__": {},
                "abs": abs,
                "round": round,
                "pow": pow,
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "log": math.log,
                "pi": math.pi,
                "e": math.e
            }

            result = eval(expression, safe_dict)
            return f"Result: {result}"
        except Exception as e:
            return f"Calculation error: {str(e)}"
        