import pytest
from src.utils.pubsub import publish


@pytest.mark.it('要能夠 pub/sub')
@pytest.mark.skip()
async def test_PubSub():

    messageId = await publish("hello", dict(message="Hello, world!"))
    assert bool(messageId)
