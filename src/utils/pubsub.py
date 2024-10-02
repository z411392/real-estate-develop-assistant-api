from google.cloud.pubsub_v1 import PublisherClient
from typing import Any
import json
from src.bootstrap import container
from asyncio import wrap_future
from os import getenv


async def publish(topicName: str, message: Any):
    data = bytes(json.dumps(message), 'utf-8')
    pubsub: PublisherClient = await container.pubsub()
    topic = f"""projects/{getenv("APP")}/topics/{topicName}"""
    messageId = await wrap_future(pubsub.publish(topic=topic, data=data))
    return messageId
