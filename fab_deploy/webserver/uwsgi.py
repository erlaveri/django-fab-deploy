# coding: utf-8
from __future__ import with_statement

from fabric.api import env, settings, sudo, run
from taskset import TaskSet, task_method

from fab_deploy import utils
from fab_deploy import system
from fab_deploy.pip import pip

__all__ = ['Uwsgi']


class Uwsgi(TaskSet):

    def __init__(self, config='uwsgi.ini'):
        self.config = config

    def _get_server_config_name(self):
        return '%s_%s' % (env.conf['INSTANCE_NAME'], self.config)

    @task_method
    @utils.run_as_sudo
    def install(self):
        """ Installs uwsgi. """
        system.aptitude_install(
            'build-essential python-dev uwsgi uwsgi-plugin-emperor uwsgi-plugin-python')
        # pip('install uwsgi')

        utils.upload_config_template('upstart_for_uwsgi.conf',
                                     '/etc/init/uwsgi.conf',
                                     use_sudo=True)
        sudo('chmod +x /etc/init.d/uwsgi')

        sudo('mkdir -p /etc/uwsgi/')
        name = self._get_server_config_name()
        utils.upload_config_template(self.config,
                                     '/etc/uwsgi/%s' % name,
                                     use_sudo=True)

    @task_method
    @utils.run_as_sudo
    def update_config(self):
        """ Updates uwsgi config and restarts uwsgi. """
        name = self._get_server_config_name()
        utils.upload_config_template(self.config,
                                     '/etc/uwsgi/%s' % name,
                                     use_sudo=True)
        sudo('service uwsgi restart')

    @task_method
    @utils.run_as_sudo
    def remove_config(self):
        """ Removes uwsgi config and reloads uwsgi. """
        # sudo('rm -rf /etc/uwsgi/')
        name = self._get_server_config_name()
        sudo('rm -f /etc/uwsgi/%s' % name)
        # sudo('invoke-rc.d uwsgi reload')


    @task_method
    @utils.run_as_sudo
    def touch(self):
        run('touch %s/touchme' % env.conf['PROJECT_DIR'])
