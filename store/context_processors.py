def base_breadcrumbs(request):
    path = request.path
    parts = path.strip('/').split('/')
    breadcrumbs = []
    url = ''
    for part in parts:
        url += f'/{part}'
        breadcrumbs.append({'name': part.replace('_', ' ').capitalize(), 'url': url})
    return {'breadcrumbs': breadcrumbs}