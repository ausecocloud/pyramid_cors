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
    cors = {
        'Access-Control-Allow-Methods': 'OPTIONS,HEAD,GET,POST,PUT,DELETE',
        'Access-Control-Allow-Headers': (
            'Accept,Accept-Language,Content-Language,Content-Type'
        )
    }
    for key, value in settings.items():
        if not key.startswith(prefix):
            continue
        cors[key[len(prefix):]] = value
    settings['cors'] = cors
