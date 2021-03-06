import sys

from database.database import get_session, config


def get_script():
    if 'linux' in sys.platform:
        return 'LD_LIBRARY_PATH=. ./bedrock_server'
    elif 'win' in sys.platform:
        return 'bedrock_server.exe'


default = dict(
    bedrock_server_root='./bedrock_server',
    bedrock_server_script=get_script(),
    bedrock_server_properties='server.properties',
    bedrock_server_whitelist='whitelist.json',
    bedrock_server_permissions='permissions.json',
    web_listening_address='0.0.0.0',
    web_listening_port='5500',
    token_length='32',
    clear_log_on_start='true',
    use_the_same_token='false',
    bds_filter_enable='true',
    bds_filter_type='bds',
    bds_filter_filters='bds_filters.yaml'
)


def get_config(key: str):
    session = get_session()
    _c = session.query(config).filter_by(key=key).first()
    if (_c is None) and (key in default.keys()):
        _c = config(key=key, value=default[key])
        session.add(_c)
        session.commit()
        return get_config(key)
    session.close()
    if _c is None:
        return None
    else:
        return _c.value


def put_config(key: str, value: str):
    session = get_session()
    _c = session.query(config).filter_by(key=key).first()
    _c.value = value
    session.commit()
    session.close()
    return value


def init():
    session = get_session()
    for key in default:
        # noinspection PyBroadException
        try:
            _config = config(key=key, value=default[key])
            session.add(_config)
            session.commit()
        except:
            pass
    session.close()


# noinspection PyBroadException
def print_and_edit():
    configs_keys = []
    for v in default:
        configs_keys.append(v)
        print('%s %s=%s' % (
            len(configs_keys),
            v,
            get_config(v)
        ))
    print('Enter 0 to Exit')
    key_index = input('Enter the number before the config you want to edit: ')
    if key_index == '0':
        return
    try:
        _key = configs_keys[int(key_index) - 1]
        _value = input('Then enter the value: ')
        put_config(_key, _value)
    except:
        print('Failed!')
    print_and_edit()


def printConfig():
    configs_keys = []
    for v in default:
        configs_keys.append(v)
        print('%s=%s' % (
            v,
            get_config(v)
        ))
