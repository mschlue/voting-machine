from blinker import Namespace

__all__ = [
    'app_start',
    'app_stop',
]

_signals = Namespace()

# triggered when app is starting but not yet serving requests
app_start = _signals.signal('app-start')

# triggered when the app has finished serving requests and is being torn down
app_stop = _signals.signal('app-stop')