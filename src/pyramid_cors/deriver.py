

def get_cors_headers(request):
    cors = request.registry.settings.get('cors', {})
    headers = cors.copy()
    # no predefined allow-origin
    if not cors.get('Access-Control-Allow-Origin', None):
        if (cors.get('Access-Control-Allow-Credentials') == 'true' and
            not request.headers.get('Origing', None)):
            headers['Access-Control-Allow-Origin'] = request.headers['Origin']
        else:
            headers['Access-Control-Allow-Origin'] = '*'
    return headers


def cors_view(view, info):
    # cors view deriver
    cors = info.options.get('cors')
    if cors:
        def add_cors_headers(context, request):
            response = view(context, request)
            response.headers.update(get_cors_headers(request))
            return response
        return add_cors_headers
    return view


cors_view.options = {'cors'}
