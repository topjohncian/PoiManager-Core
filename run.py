import sys
from gevent.pywsgi import WSGIServer
from database import BdsLogger
from database.ConfigHelper import get_config
from core.core import app
import signal


# noinspection PyUnusedLocal
def CtrlC(*args):
    print('>stopped<')
    BdsLogger.put_log('manager', 'stop_done')
    sys.exit()


# noinspection PyTypeChecker
signal.signal(signal.SIGINT, CtrlC)
# noinspection PyTypeChecker
signal.signal(signal.SIGTERM, CtrlC)


BdsLogger.put_log('manager', 'start')
BdsLogger.put_log('manager', '%s:%s' % (
    get_config('web_listening_address'),
    get_config('web_listening_port')
))

print('>Listening at %s:%s' % (
    get_config('web_listening_address'),
    get_config('web_listening_port')
))

http_server = WSGIServer(
    (
        get_config('web_listening_address'),
        int(get_config('web_listening_port'))
    ),
    app)
http_server.serve_forever()
