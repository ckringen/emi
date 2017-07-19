class conditional_decorator(object):
    def __init__(self, dec, condition):
        self.decorator = dec
        self.condition = condition

    def __call__(self, func):
        if not self.condition:
            return func
        return self.decorator(func)


def cond_dec( func, cflag ):
    if not cflag:
        return func
    else:
        def wrapper(*args, **kwargs):
            return func
        return wrapper
