from multiprocessing import freeze_support
from traceback import format_exc
from asyncio import get_event_loop_policy, set_event_loop
from src.utils.development import createLogger
from src.cli import app


if __name__ == "__main__":
    freeze_support()
    logger = createLogger(__name__)
    loop = get_event_loop_policy().new_event_loop()
    set_event_loop(loop)
    try:
        loop.run_until_complete(app())
    except KeyboardInterrupt:
        pass
    except Exception:
        logger.error(format_exc())
