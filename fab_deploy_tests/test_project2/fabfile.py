from fab_deploy.utils import define_host
from fab_deploy.webserver.apache import Apache
from fab_deploy.webserver.nginx import Nginx
from fab_deploy.django import Django
from fab_deploy.project import WebProject

LAYOUT_OPTIONS = dict(
    PROJECT_PATH = 'src',
    PIP_REQUIREMENTS_PATH = '',
    PIP_REQUIREMENTS = 'requirements.txt',
    PIP_REQUIREMENTS_ACTIVE = 'requirements.txt',
    CONFIG_TEMPLATES_PATHS = ['hosting/staging', 'hosting'],
)

apps = dict(
    django=Django(
        Nginx(), 
        Apache(wsgi='django_wsgi.py'),
        local_config='local_settings.py',
        remote_config='staging_settings.py'
    )
)
project = WebProject(apps).expose_as_module('project')

@define_host('foo2@127.0.0.1:2222', LAYOUT_OPTIONS)
def foo_site():
    return dict(
        VCS = 'git',
        SERVER_NAME = 'foo.example.com',

        SUDO_USER = 'sudouser',

        DB_ROOT_PASSWORD = '123',
        DB_USER = 'foouser',
        DB_PASSWORD = 'foo123',
        DB_BACKEND = 'mysql',
    )