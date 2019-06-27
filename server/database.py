import aiopg


async def cleanup_ctx(app):
    cfg = app['config']

    app['pg'] = await aiopg.connect(host=cfg.database.host,
                                    port=cfg.database.port,
                                    user=cfg.database.user,
                                    password=cfg.database.password,
                                    database=cfg.database.database)

    yield
    await app['pg'].close()
