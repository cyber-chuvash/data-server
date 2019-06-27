import aiopg


async def cleanup_ctx(app):
    cfg = app['config']

    app['pg'] = await aiopg.connect(host=cfg.database.host,
                                    port=cfg.database.port,
                                    user=cfg.database.user,
                                    password=cfg.database.password,
                                    database=cfg.database.database)
    
    async with app['pg'].cursor() as cur:
        await cur.execute('CREATE TABLE IF NOT EXISTS data (timestamp TIMESTAMP (0), value INTEGER);')

    yield
    await app['pg'].close()
