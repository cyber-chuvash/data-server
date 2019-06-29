import os
import logging
import configparser


class ConfigurationError(Exception):
    pass


class ConfigSection(dict):
    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            raise AttributeError(f'"{item}" not in CONF_FIELDS') from None

    __getattr__ = __getitem__


class _Config:
    CONF_FIELDS = {
        'base': {
            'log_level': str,
            'access_tokens': str.split
        },

        'database': {
            'host': str,
            'port': int,
            'database': str,
            'user': str,
            'password': str,
        },
    }

    def __init__(self, config_file=None):
        self._conf = {}

        _conf_data = configparser.ConfigParser()
        _conf_data.read(config_file or os.environ['CONFIG_FILE'])
        _conf_data['DEFAULT'] = {
            'log_level': 'INFO',
            'host': '127.0.0.1',
            'port': '5432'
        }

        self.load_conf(_conf_data)

    @property
    def log_level(self):
        return logging.getLevelName(self.base.log_level)

    def load_conf(self, conf_data):
        for section in conf_data.sections():
            self._conf[section] = {}
            for field, loader in self.CONF_FIELDS[section].items():
                try:
                    self._conf[section][field] = loader(conf_data[section][field])
                except KeyError:
                    raise ConfigurationError(f'CONF_FIELDS["{section}"]["{field}"] was not found in config') from None

    def __getitem__(self, item):
        try:
            return ConfigSection(**self._conf[item])
        except KeyError:
            raise AttributeError(f'"{item}" not in CONF_FIELDS') from None

    __getattr__ = __getitem__


async def cleanup_ctx(app):
    app['config'] = _Config(app['config_file'])
    yield
