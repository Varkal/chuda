'''
Module contains Chuda decorators
'''
def autorun():
    '''
    This decorator automaticaly call the run method of this class if
    it's in the main file
    '''
    def wrapper(cls):
        '''
        Wrapper for autorun
        '''

        import inspect
        if inspect.getmodule(cls).__name__ == "__main__":
            cls().run()
        return cls

    return wrapper


def signal_handler(sig):
    '''
    Flag a method to be used as a signal handler
    '''
    def wrapper(func):
        '''
        Wrapper for signal_handler
        '''
        setattr(func, "handle_signal", sig)
        return func

    return wrapper
