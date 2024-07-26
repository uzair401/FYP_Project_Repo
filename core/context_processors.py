from django.urls import resolve, reverse
from django.utils.text import slugify

def breadcrumbs(request):
    url_name = resolve(request.path_info).url_name
    if not url_name:
        return {}

    breadcrumbs = [{'name': 'Dashboard', 'url': reverse('academics:Department_dashboard')}]

    # Split the path into components and create breadcrumb items
    path_components = request.path.strip('/').split('/')
    for i, component in enumerate(path_components):
        name = component.replace('_', ' ').capitalize()
        url = '/' + '/'.join(path_components[:i+1])
        breadcrumbs.append({'name': name, 'url': url})

    # Mark the last breadcrumb item as active
    if breadcrumbs:
        breadcrumbs[-1]['url'] = None

    return {'breadcrumbs': breadcrumbs}