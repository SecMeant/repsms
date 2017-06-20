from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from jinja2 import Environment, PackageLoader, select_autoescape


def environment(**options):
    env = Environment(
        loader=PackageLoader('SMS','..\\templates\\jinja2'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'zip':zip,
    })
    return env