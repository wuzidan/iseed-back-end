import threading

class ThreadLocalStorage:
    _local = threading.local()

    @classmethod
    def set(cls, key, value):
        setattr(cls._local, key, value)

    @classmethod
    def get(cls, key, default=None):
        return getattr(cls._local, key, default)

    @classmethod
    def delete(cls, key):
        if hasattr(cls._local, key):
            delattr(cls._local, key)

    @classmethod
    def clear(cls):
        cls._local.__dict__.clear()