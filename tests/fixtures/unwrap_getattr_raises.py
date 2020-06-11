class TryMe:
    def __getattr__(self, item):
        raise ValueError


TRY_ME = TryMe()
