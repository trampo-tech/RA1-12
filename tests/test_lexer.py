import unittest

from src.rpn_compiler.lexer import LexicalError, parseExpressao


class LexerTests(unittest.TestCase):
    def test_expressao_valida(self) -> None:
        self.assertEqual(
            parseExpressao("(3.14 2.0 +)", []),
            ["(", "3.14", "2.0", "+", ")"],
        )

    def test_expressao_aninhada_valida(self) -> None:
        self.assertEqual(
            parseExpressao("((1.5 2.0 *) (3.0 4.0 *) /)", []),
            ["(", "(", "1.5", "2.0", "*", ")", "(", "3.0", "4.0", "*", ")", "/", ")"],
        )

    def test_comandos_especiais_validos(self) -> None:
        self.assertEqual(parseExpressao("(5 RES)", []), ["(", "5", "RES", ")"])
        self.assertEqual(parseExpressao("(10.5 MEMORIA)", []), ["(", "10.5", "MEMORIA", ")"])
        self.assertEqual(parseExpressao("(MEMORIA)", []), ["(", "MEMORIA", ")"])

    def test_operadores_validos(self) -> None:
        self.assertEqual(parseExpressao("(10 3 //)", []), ["(", "10", "3", "//", ")"])
        self.assertEqual(parseExpressao("(10 3 %)", []), ["(", "10", "3", "%", ")"])
        self.assertEqual(parseExpressao("(2 3 ^)", []), ["(", "2", "3", "^", ")"])

    def test_numero_negativo_valido(self) -> None:
        self.assertEqual(parseExpressao("(-3.5 2.0 +)", []), ["(", "-3.5", "2.0", "+", ")"])

    def test_operador_invalido(self) -> None:
        with self.assertRaises(LexicalError):
            parseExpressao("(3.14 2.0 &)", [])

    def test_numero_malformado(self) -> None:
        with self.assertRaises(LexicalError):
            parseExpressao("(3.14.5 2.0 +)", [])

    def test_numero_com_virgula(self) -> None:
        with self.assertRaises(LexicalError):
            parseExpressao("(3,45 2.0 +)", [])

    def test_parenteses_desbalanceados(self) -> None:
        with self.assertRaises(LexicalError):
            parseExpressao("(3.14 2.0 +", [])

    def test_identificador_invalido(self) -> None:
        with self.assertRaises(LexicalError):
            parseExpressao("(10.5 CONTADOr)", [])


if __name__ == "__main__":
    unittest.main()
