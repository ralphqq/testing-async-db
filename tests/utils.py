from unittest.mock import MagicMock


class MockedCoroutine(MagicMock):
    """Mocks coroutines."""

    def __call__(self, *args, **kwargs):
        sup = super(MockedCoroutine, self)
        async def coro():
            return sup.__call__(*args, **kwargs)
        return coro()

    def __await__(self):
        return self().__await__()
