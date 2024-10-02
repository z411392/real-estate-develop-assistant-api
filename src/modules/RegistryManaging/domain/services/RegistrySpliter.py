from abc import ABCMeta, abstractmethod
from re import finditer, split
from typing import Optional, Iterable, Tuple


class RegistrySpliter(metaclass=ABCMeta):
    @abstractmethod
    def _parse(
        self, title: str, content: str
    ) -> Iterable[Tuple[Optional[str], int, str]]:
        return NotImplemented

    def _split(self, content: str):
        regexp = r"其他登記事項.*"
        index = -1
        for record, matchedNotes in zip(
            split(regexp, content), finditer(regexp, content)
        ):
            index += 1
            notes = matchedNotes.group(0)
            record += notes
            yield index, record

    def __call__(self, text: str):
        regexp = r"\*+ *(\S+部) *\*+"
        matches = finditer(regexp, text)
        title = None
        for match in matches:
            fullContent, text = text.split(match.group(0))
            yield from self._parse(title, fullContent)
            title = match.group(1)
        fullContent = text
        yield from self._parse(title, fullContent)
