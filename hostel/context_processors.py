def h_breadcrumbs(request):
    path = request.path
    parts = path.strip('/').split('/')
    h_breadcrumbs = []
    url = ''
    for part in parts:
        url += f'/{part}'
        h_breadcrumbs.append({'name': part.replace('_', ' ').capitalize(), 'url': url})
    return {'h_breadcrumbs': h_breadcrumbs}



def language(request):
    return {
        'lang': request.session.get('lang', 'en')
    }