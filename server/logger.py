import logging


async def on_startup(app):
    logger = logging.getLogger('data-server')
    logger.setLevel(app['config'].base.log_level)
    logger.addHandler(logging.StreamHandler())
    app['logger'] = logger
