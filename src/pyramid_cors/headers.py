

def get_cors_headers(request):
    if not request.headers.get('Origin'):
        # not a CORS request, don't return any CORS headers
        return {}
    headers = request.registry.settings.get('cors.headers', {}).copy()
    allow_origin = get_allow_origin(request, headers)

    # no predefined allow-origin
    if allow_origin:
        headers['Access-Control-Allow-Origin'] = allow_origin
    else:
        # remove header
        headers.pop('Access-Control-Allow-Origin', None)
    return headers


def get_allow_origin(request, headers):
    allowed_origins = request.registry.settings['cors.allowed_origins']
    if allowed_origins:
        # try to match origin
        origin = request.headers.get('Origin')
        if allowed_origins.match(origin or ''):
            return origin

        return None
    # fall back to configured static header
    return headers.get('Access-Control-Allow-Origin', None)
