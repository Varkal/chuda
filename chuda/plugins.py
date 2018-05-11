'''
Module for Chuda Plugins
'''
class Plugin:
    '''
    Class represent a Plugin for a Chuda application
    A plugin can register hooks for import step in application lifecycle
    or enrich the app with new properties
    '''
    priority = 0

    def __init__(self):
        self.app = None

    def setup(self, app):
        '''
        Setup the app on the plugin
        '''
        self.app = app

    def enrich_app(self, name, value):
        '''
        Add a new property to the app
        '''
        #Method shouldn't be added:  https://stackoverflow.com/a/28060251/3042398
        if type(value) == type(self.enrich_app):
            raise ValueError("enrich_app can't add method")

        setattr(self.app, name, value)

    def on_create(self):
        '''
        Called at the app creation
        '''
        pass

    def on_arguments_parsed(self):
        '''
        Called after arguments have been parsed
        '''
        pass

    def on_config_read(self):
        '''
        Called after configurations files have been read
        '''
        pass

    def on_signals_handled(self):
        '''
        Called after signals handlers have been setuped
        '''
        pass

    def on_logger_created(self):
        '''
        Called after logger have been created
        '''
        pass

    def on_run(self):
        '''
        Called just before run the app
        '''
        pass

    def on_end(self):
        '''
        Called after all steps and code have been executed
        '''
        pass
