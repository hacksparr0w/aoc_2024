from __future__ import annotations

from dataclasses import dataclass
from io import TextIOBase


@dataclass
class Integer:
    value: int


@dataclass
class FunctionCall:
    name: str
    args: list[Integer]


Token = FunctionCall


@dataclass
class Seeking:
    buffer: str


@dataclass
class ReadingFunctionCall:
    function_name: str
    args: list[Integer]
    buffer: str


TokenizerState = Seeking | ReadingFunctionCall
TokenizerStepResult = tuple[TokenizerState | None, list[Token]]


def seeking_step(
    state: Seeking,
    stream: TextIOBase,
    tokens: list[Token]
) -> TokenizerStepResult:
    buffer = state.buffer

    character = stream.read(1)

    if not character:
        return None, tokens
    if character.isalpha():
        return Seeking(buffer=buffer + character), tokens
    elif character == "(" and buffer:
        return (
            ReadingFunctionCall(
                function_name=buffer,
                args=[],
                buffer=""
            ),
            tokens
        )
    else:
        return Seeking(buffer=""), tokens


def reding_function_call_step(
    state: ReadingFunctionCall,
    stream: TextIOBase,
    tokens: list[Token]
) -> TokenizerStepResult:
    function_name = state.function_name
    args = state.args
    buffer = state.buffer

    character = stream.read(1)

    if not character:
        return None, tokens
    elif character.isdigit():
        return (
            ReadingFunctionCall(
                function_name=function_name,
                args=args,
                buffer=buffer + character
            ),
            tokens
        )
    elif character == "," and buffer:
        return (
            ReadingFunctionCall(
                function_name=function_name,
                args=args + [Integer(int(buffer))],
                buffer=""
            ),
            tokens
        )
    elif character == ")":
        if buffer:
            args = args + [Integer(int(buffer))]

        return (
            Seeking(buffer=""),
            tokens + [FunctionCall(name=function_name, args=args)]
        )
    else:
        return Seeking(buffer=""), tokens


def step(
    state: TokenizerState,
    stream: TextIOBase,
    tokens: list[Token]
) -> TokenizerStepResult:
    if isinstance(state, Seeking):
        return seeking_step(state, stream, tokens)
    elif isinstance(state, ReadingFunctionCall):
        return reding_function_call_step(state, stream, tokens)
    else:
        raise TypeError(f"Unknown state: {state}")


def tokenize(stream: TextIOBase) -> list[Token]:
    state = Seeking(buffer="")
    tokens = []

    while state is not None:
        state, tokens = step(state, stream, tokens)

    return tokens


def interpret(tokens: list[Token]) -> int:
    accumulator = 0

    for token in tokens:
        if not isinstance(token, FunctionCall):
            return
        
        if token.name.endswith("mul"):
            a = token.args[0].value
            b = token.args[1].value
            r = a * b

            accumulator += r

    return accumulator


with open("input/03.txt") as stream:
    tokens = tokenize(stream)
    result = interpret(tokens)
    print(result)
