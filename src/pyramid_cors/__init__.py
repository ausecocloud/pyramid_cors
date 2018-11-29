import re

from .deriver import cors_view
from .preflight import CorsPreflightPredicate, add_cors_preflight_handler


def includeme(config):
    config.add_directive(
        'add_cors_preflight_handler',
        add_cors_preflight_handler
    )
    config.add_route_predicate('cors_preflight', CorsPreflightPredicate)
    config.add_view_deriver(cors_view)

    # read cors settings:
    prefix = 'cors.'
    settings = config.get_settings()
    # set defaults
    settings['cors.headers'] = headers = {
        'Access-Control-Allow-Methods': 'OPTIONS,HEAD,GET,POST,PUT,DELETE',
        'Access-Control-Allow-Headers': (
            'Accept,Accept-Language,Content-Language,Content-Type'
        )
    }
    settings.setdefault('cors.allowed_origins', None)
    response_headers = {
        'Access-Control-Allow-Origin'.lower(),
        'Access-Control-Expose-Headers'.lower(),
        'Access-Control-Max-Age'.lower(),
        'Access-Control-Allow-Credentials'.lower(),
        'Access-Control-Allow-Methods'.lower(),
        'Access-Control-Allow-Headers'.lower(),
    }
    for key, value in settings.items():
        if not key.startswith(prefix):
            continue
        name = key[len(prefix):]
        if name.lower() in response_headers:
            headers[name] = value
            continue
        if name == 'allowed_origins' and value is not None:
            # this can be a regexp if matched Allow-Origin will be set to
            # Origin
            settings['cors.allowed_origins'] = re.compile(value)
