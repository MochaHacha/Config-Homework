from lark import Transformer, v_args, Token

@v_args(inline=True)
class ConfigTransformer(Transformer):
    def __init__(self):#словарь для хранения переменных
        self.vars = {}

    def number(self, token):#преобразует найденное число с текст
        return float(token)

    def STRING(self, token):#удаляет префикс 
        return str(token)[2:-1]

    def list(self, *items):#собирает все элементы внутри list в обычный питон список
        return list(items)

    def var_def(self, name, value):
        self.vars[str(name)] = value
        return value

    def postfix_expr(self, *parts):
        stack = []
        for part in parts:
            token_str = str(part)

            if isinstance(part, float):#если число
                stack.append(part)
            elif isinstance(part, list):#ессли список 
                stack.append(part)
            elif token_str in self.vars:#есои имя переменной берем из словаря
                stack.append(self.vars[token_str])
            #Обработка арифметических операций
            elif token_str == "+":
                b, a = stack.pop(), stack.pop()
                stack.append(a + b)
            elif token_str == "-":
                b, a = stack.pop(), stack.pop()
                stack.append(a - b)
            elif token_str == "*":
                b, a = stack.pop(), stack.pop()
                stack.append(a * b)
            elif token_str == "/":
                b, a = stack.pop(), stack.pop()
                stack.append(a / b)
            elif token_str == "len":
                val = stack.pop()
                stack.append(float(len(val)) if isinstance(val, list) else 1.0)
            else:
                try:
                    stack.append(float(token_str))
                except ValueError:
                    continue
        #результат - то что отслоась на верширне стека
        return stack[-1] if stack else 0.0

    # Обработка инструкций
    def instruction(self, item): return item
    def start(self, *items): return items
    def comment(self, *args): return None#комментарий