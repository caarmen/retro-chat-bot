import asyncio
import datetime as dt
import logging
from typing import Callable

from retrochatbot.framework.common.bounded_drop_queue import BoundedDropQueue
from retrochatbot.framework.domain.usecases.keys_to_text import KEY_BACKSPACE, KEY_ENTER

logger = logging.getLogger(__name__)


class ParticipantBuffer:
    def __init__(
        self,
        size: int,
        debounce_s: int,
        burst_callback: Callable[[], None],
    ):
        self.data: BoundedDropQueue[str | dt.datetime] = BoundedDropQueue(max_size=size)
        self._burst_callback = burst_callback
        self._task_emit: asyncio.Task | None = None
        self._debounce_s = debounce_s
        self.is_self = False
        self.last_event_datetime = None

    def _is_valid_key(self, key: str):
        return key and (len(key) == 1 or key in [KEY_BACKSPACE, KEY_ENTER])

    def append(self, key: str):
        if not self._is_valid_key(key):
            return
        self.data.append(item=key)
        self.last_event_datetime = dt.datetime.now(dt.timezone.utc)
        self._debounce_emit()

    def resize(self, size: int):
        self.data.resize(max_size=size)

    def _debounce_emit(self):
        if self._task_emit:
            self._task_emit.cancel()

        async def delay_emit():
            await asyncio.sleep(self._debounce_s)
            await self._emit()

        self._task_emit = asyncio.create_task(delay_emit())

    async def _emit(self):
        try:
            self.data.append(self.last_event_datetime)
            if not self.is_self:
                await self._burst_callback()
        except Exception as e:
            logger.exception("callback raised {e}", exc_info=e)
