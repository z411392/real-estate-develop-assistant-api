from dataclasses import dataclass


@dataclass
class UploadingSnapshot:
    name: str
    content: str
