from src.constants import LanguageModel
from tiktoken import encoding_for_model, Encoding
from typing import Optional
from math import ceil

_encoding: Optional[Encoding] = None


def countTokens(text: str):
    global _encoding
    if _encoding is None:
        _encoding = encoding_for_model(LanguageModel)
    tokens = _encoding.encode(text)
    tokensCount = len(tokens)
    return tokensCount


def countCreditsToBeUsed(tokensCount: int):
    credits = ceil(tokensCount / 1000)
    if credits <= 0:
        return 0
    return credits
