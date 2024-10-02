from google.cloud.firestore import (
    AsyncClient,
    SERVER_TIMESTAMP,
)
from src.utils.events import Event


class EventPublisher:
    _db: AsyncClient

    def __init__(self, db: AsyncClient):
        self._db = db

    async def publish(self, path: str, event: Event):
        eventId = event.id()
        documentReference = self._db.collection(path).document(eventId)
        await documentReference.set(
            dict(type=event.type(), data=event.data(), timestamp=SERVER_TIMESTAMP),
            merge=True,
        )
        return eventId
