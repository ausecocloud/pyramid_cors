from pyramid.httpexceptions import HTTPNoContent
from pyramid.security import NO_PERMISSION_REQUIRED


def cors_options_view(context, request):
    # The default prefilght options view
    response = HTTPNoContent()
    cors = request.registry.settings.get('cors', {})

    response.headers.update(cors)

    if not cors.get('Access-Control-Allow-Origin', None):
        if (cors.get('Access-Control-Allow-Credentials', None) == 'true' and
            request.headers.get('Origin', None)):
            # test comment
            response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
        else:
            response.headers['Access-Control-Allow-Origin'] = '*'

    return response


def add_cors_preflight_handler(config, view=cors_options_view):
    config.add_route(
        'cors-options-preflight', '/{catch_all:.*}',
        cors_preflight=True,
        request_method='OPTIONS'
    )
    config.add_view(
        view,
        route_name='cors-options-preflight',
        request_method='OPTIONS',
        permission=NO_PERMISSION_REQUIRED,
    )


class CorsPreflightPredicate(object):

    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'cors_preflight = %s' % bool(self.val)

    phash = text

    def __call__(self, context, request):
        if not self.val:
            return False
        # is it a preflight request?
        return (
            request.method == 'OPTIONS' and
            'Origin' in request.headers and
            'Access-Control-Request-Method' in request.headers
        )
