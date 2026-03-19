import operator
from collections import deque


class MemoryAccessError(AttributeError):
    """Erro ao acessar valor na memoria"""


class Evaluator:
    def __init__(self):
        self.pilha: deque[str] = deque()
        self.memoria: float | None = None
        self.resultados: dict[str, str | None] = {}

    def _apply_binary_op(self, op_func, line_num: int, op_symbol: str):
        try:
            x2 = self._pega_numero()
            x1 = self._pega_numero()
            result = str(op_func(x1, x2))
            self.pilha.append(result)
        except ZeroDivisionError:
            print(f"Division by zero: {x1} {op_symbol} {x2}")
            self.resultados[str(line_num)] = None

    def _pega_numero(self) -> float:
        item = self.pilha.pop()
        if item != "(":
            return float(item)
        return self._pega_numero()

    def executarExpressao(self, linhas: list[list[str]]):
        for i, linha in enumerate(linhas, start=1):
            for token in linha:
                match token:
                    case "+":
                        self._apply_binary_op(operator.add, i, "+")

                    case "-":
                        self._apply_binary_op(operator.sub, i, "-")

                    case "*":
                        self._apply_binary_op(operator.mul, i, "*")

                    case "/":
                        self._apply_binary_op(operator.truediv, i, "/")

                    case "//":
                        self._apply_binary_op(operator.floordiv, i, "//")

                    case "%":
                        self._apply_binary_op(operator.mod, i, "%")

                    case "^":
                        self._apply_binary_op(operator.pow, i, "^")

                    case "MEM":
                        if self.pilha[-1] == "(" or self.pilha.count == 0:
                            if self.memoria is not None:
                                self.pilha.append(str(self.memoria))
                            else:
                                raise MemoryAccessError  # TODO this might be better handled by syntax analyzer but dont know
                        else:
                            value = self._pega_numero()
                            self.memoria = value

                    case "RES":
                        try:
                            linha = self.pilha.pop()
                            value = self.resultados[linha]
                            if value is not None:
                                self.pilha.append(value)
                            else:
                                print(
                                    f"Acesso de resultado inválido da linha : {linha}"
                                )
                                self.resultados[str(i)] = None
                                break
                        except KeyError:
                            print(f"Acesso via RES para linha inválida: {linha}")
                            self.resultados[str(i)] = None
                            break

                    case ")":  # only need the opening brackets for MEM calls
                        pass

                    case _:
                        self.pilha.append(token)
            # once the line loops finishes
            else:
                self.resultados[str(i)] = str(self._pega_numero())

    def get_resultados(self):
        return self.resultados


if __name__ == "__main__":
    eval = Evaluator()

    eval.executarExpressao(
        [
            [
                "(",
                "(",
                "1.5",
                "2.0",
                "*",
                ")",
                "(",
                "3.0",
                "MEM",
                "(",
                "MEM",
                ")",
                ")",
                "/",
                ")",
            ]
        ]
    )
    print(eval.resultados)
