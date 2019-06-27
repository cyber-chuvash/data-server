import json
import argparse
from datetime import datetime

import aiohttp.web

from server import config
from server import database


routes = aiohttp.web.RouteTableDef()


@routes.post('/data/{table}')
async def post_data(request):
    # Check that request has a JSON body
    if not (request.content_type == 'application/json' and request.can_read_body):
        raise aiohttp.web.HTTPBadRequest

    try:
        data = (await request.json())['data']
    except (json.JSONDecodeError, KeyError):
        raise aiohttp.web.HTTPBadRequest from None

    # Get values from request data and check for None
    value = data.get('value')
    timestamp = data.get('timestamp')

    if value is None or timestamp is None:
        raise aiohttp.web.HTTPBadRequest

    # Check timestamp to be a valid timestamp
    try:
        timestamp = datetime.fromisoformat(timestamp)
    except (ValueError, TypeError):
        raise aiohttp.web.HTTPBadRequest from None

    # Check value to be an integer or a numeric string
    try:
        value = int(value)
    except ValueError:
        raise aiohttp.web.HTTPBadRequest from None

    table = request.match_info['table']

    print(f'[{table}] {timestamp.isoformat()}: {value}')

    return aiohttp.web.Response(status=200, text='ok')


def create_app(*args, config_file=None):
    app = aiohttp.web.Application()

    app['config_file'] = config_file
    app.on_startup.append(config.on_startup)
    app.cleanup_ctx.append(database.cleanup_ctx)

    app.add_routes(routes)

    return app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1')
    parser.add_argument('-P', '--port', default=8080, type=int)
    parser.add_argument('-c', '--config-file', default=None)

    args = parser.parse_args()

    aiohttp.web.run_app(create_app(args.config_file), host=args.host, port=args.port)


if __name__ == '__main__':
    main()