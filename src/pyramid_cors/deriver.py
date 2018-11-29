from .headers import get_cors_headers


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
