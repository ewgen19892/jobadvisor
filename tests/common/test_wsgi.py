from django.core.handlers.wsgi import WSGIHandler

from jobadvisor import wsgi


def test_handler():
    assert type(wsgi.application) is WSGIHandler
