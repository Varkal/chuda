def autorun():
    '''
    Call the run method of the decorated class if the current file is the main file
    '''
    def wrapper(cls):

        import inspect
        if inspect.getmodule(cls).__name__ == "__main__":
            cls().run()
        return cls

    return wrapper


def signal_handler(sig):
    '''
    Flag a method to be used as a signal handler

    Args:
        sig (signal): The signal, from the :mod:`~signal` module
    '''
    def wrapper(func):
        setattr(func, "handle_signal", sig)
        return func

    return wrapper
