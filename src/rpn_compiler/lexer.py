"""
Integrantes do grupo:
- Gabriel Baú Herkert (@ogabrielbau)

Grupo no Canvas:
- RA1-12
"""

from __future__ import annotations

from typing import Any, Callable

EstadoFn = Callable[["LexerFSM"], Any]

OPERADORES = {"+", "-", "*", "/", "//", "%", "^"}
PALAVRA_RESERVADA = "RES"


class LexicalError(ValueError):
    """Erro encontrado durante a analise lexica."""


def parseExpressao(linha: str, tokens: list[str]) -> list[str]:
    """
    Analisa uma linha da linguagem e acumula os tokens encontrados.
    """
    lexer = LexerFSM(linha)
    tokens.extend(lexer.run())
    return tokens


class LexerFSM:
    def __init__(self, linha: str) -> None:
        self.linha = linha.rstrip("\n")
        self.posicao = 0
        self.inicio_token = 0
        self.parenteses = 0
        self.tokens: list[str] = []

    def run(self) -> list[str]:
        estado: EstadoFn | None = estado_inicial
        while estado is not None:
            estado = estado(self)

        if self.parenteses != 0:
            raise LexicalError("parenteses desbalanceados")

        return self.tokens

    def atual(self) -> str | None:
        if self.posicao >= len(self.linha):
            return None
        return self.linha[self.posicao]

    def proximo(self) -> str | None:
        if self.posicao + 1 >= len(self.linha):
            return None
        return self.linha[self.posicao + 1]

    def avancar(self) -> None:
        if self.atual() is not None:
            self.posicao += 1

    def iniciar_token(self) -> None:
        self.inicio_token = self.posicao

    def emitir_token(self) -> None:
        self.tokens.append(self.linha[self.inicio_token : self.posicao])

    def token_anterior(self) -> str | None:
        if not self.tokens:
            return None
        return self.tokens[-1]

    def permite_numero_com_sinal(self) -> bool:
        anterior = self.token_anterior()
        if anterior is None:
            return True
        if anterior == "(":
            return True
        return anterior in OPERADORES


def estado_inicial(lexer: LexerFSM) -> EstadoFn | None:
    caractere = lexer.atual()

    if caractere is None:
        return None

    if caractere in " \t\r":
        lexer.avancar()
        return estado_inicial

    if caractere == "(":
        lexer.iniciar_token()
        lexer.avancar()
        lexer.parenteses += 1
        lexer.emitir_token()
        return estado_inicial

    if caractere == ")":
        lexer.iniciar_token()
        lexer.avancar()
        lexer.parenteses -= 1
        if lexer.parenteses < 0:
            raise LexicalError("parentese de fechamento sem abertura")
        lexer.emitir_token()
        return estado_inicial

    if caractere in "+-":
        proximo = lexer.proximo()
        if proximo is not None and (proximo.isdigit() or proximo == "."):
            if lexer.permite_numero_com_sinal():
                lexer.iniciar_token()
                lexer.avancar()
                return estado_numero_com_sinal
        lexer.iniciar_token()
        lexer.avancar()
        lexer.emitir_token()
        return estado_inicial

    if caractere.isdigit():
        lexer.iniciar_token()
        lexer.avancar()
        return estado_numero_inteiro

    if caractere == ".":
        raise LexicalError("numero real malformado")

    if caractere == "/":
        lexer.iniciar_token()
        lexer.avancar()
        return estado_barra

    if caractere in "*%^":
        lexer.iniciar_token()
        lexer.avancar()
        lexer.emitir_token()
        return estado_inicial

    if "A" <= caractere <= "Z":
        lexer.iniciar_token()
        lexer.avancar()
        return estado_identificador

    raise LexicalError(f"token invalido: {caractere}")


def estado_numero_com_sinal(lexer: LexerFSM) -> EstadoFn:
    caractere = lexer.atual()

    if caractere is None:
        raise LexicalError("numero real malformado")

    if caractere.isdigit():
        lexer.avancar()
        return estado_numero_inteiro

    if caractere == ".":
        lexer.avancar()
        return estado_numero_fracionario

    raise LexicalError("numero real malformado")


def estado_numero_inteiro(lexer: LexerFSM) -> EstadoFn | None:
    caractere = lexer.atual()

    if caractere is None:
        lexer.emitir_token()
        return None

    if caractere.isdigit():
        lexer.avancar()
        return estado_numero_inteiro

    if caractere == ".":
        lexer.avancar()
        return estado_numero_fracionario

    if caractere in " \t\r()":
        lexer.emitir_token()
        return estado_inicial

    raise LexicalError("numero real malformado")


def estado_numero_fracionario(lexer: LexerFSM) -> EstadoFn:
    caractere = lexer.atual()

    if caractere is None:
        raise LexicalError("numero real malformado")

    if caractere.isdigit():
        lexer.avancar()
        return estado_numero_fracionario_digitos

    raise LexicalError("numero real malformado")


def estado_numero_fracionario_digitos(lexer: LexerFSM) -> EstadoFn | None:
    caractere = lexer.atual()

    if caractere is None:
        lexer.emitir_token()
        return None

    if caractere.isdigit():
        lexer.avancar()
        return estado_numero_fracionario_digitos

    if caractere in " \t\r()":
        lexer.emitir_token()
        return estado_inicial

    raise LexicalError("numero real malformado")


def estado_identificador(lexer: LexerFSM) -> EstadoFn | None:
    caractere = lexer.atual()

    if caractere is None:
        return finalizar_identificador(lexer)

    if "A" <= caractere <= "Z":
        lexer.avancar()
        return estado_identificador

    if caractere in " \t\r()":
        return finalizar_identificador(lexer)

    raise LexicalError("identificador de memoria invalido")


def finalizar_identificador(lexer: LexerFSM) -> EstadoFn:
    lexema = lexer.linha[lexer.inicio_token : lexer.posicao]

    if lexema == PALAVRA_RESERVADA:
        lexer.emitir_token()
        return estado_inicial

    lexer.emitir_token()
    return estado_inicial


def estado_barra(lexer: LexerFSM) -> EstadoFn:
    caractere = lexer.atual()

    if caractere == "/":
        lexer.avancar()
        lexer.emitir_token()
        return estado_inicial

    lexer.emitir_token()
    return estado_inicial
