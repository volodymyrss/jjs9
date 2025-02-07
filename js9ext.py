from notebook.utils import url_path_join

from jupyter_server.base.handlers import JupyterHandler, FileFindHandler

import tornado.web
import os
import subprocess
import logging

import jupyter_server.serverapp

print('\033[31mimporting JS9!\033[0m')


class MainHandler(JupyterHandler):
    @tornado.web.authenticated
    def get(self):
        self.finish(self.render_template("index_jjs9.html", jid=None, **self.application.settings))

class NewHandler(JupyterHandler):
    @tornado.web.authenticated
    def get(self, jid_id):
        self.finish(self.render_template("index_jjs9.html", jid=jid_id, **self.application.settings))


def _load_jupyter_server_extension(serverapp: jupyter_server.serverapp.ServerApp):
    """
    This function is called when the extension is loaded.
    """
    logging.error('\033[31mloading JS9!\033[0m')
    print('\033[31mloading JS9!\033[0m')
    return load_jupyter_server_extension(serverapp)

def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    logger = logging.getLogger('tornado.access')
    logger.info('Jjs9 - Launching js9Helper')
    localf = os.path.dirname(__file__)
    jhelper = os.path.join(localf, 'js9Helper.js')
    logger.warning('\033[31mjs9 helper in %s\033[0m', jhelper)
    subprocess.Popen(['node', '{}'.format(jhelper)])
    web_app = nb_server_app.web_app
    web_app.settings["jinja2_env"].loader.searchpath += [os.path.dirname(__file__)]
    host_pattern = '.*$'

    logger.warning('js9: loading, web_app.settings[base_url] = %s', web_app.settings['base_url'])

    route_pattern_main = url_path_join(web_app.settings['base_url'], '/jjs9/')
    route_pattern_files = url_path_join(web_app.settings['base_url'], '/jjs9/(.*)')
    route_pattern_new = url_path_join(web_app.settings['base_url'], '/jjs9/([0-9a-zA-Z]+)')
    web_app.add_handlers(host_pattern, [(route_pattern_main, MainHandler)])
    web_app.add_handlers(host_pattern, [(route_pattern_new, NewHandler)])
    web_app.add_handlers(host_pattern, [(route_pattern_files, FileFindHandler, {"path": os.path.dirname(__file__)})])


def _jupyter_server_extension_points():
    """
    Returns a list of dictionaries with metadata describing
    where to find the `_load_jupyter_server_extension` function.
    """
    return [
        {
            "js9ext": "js9ext"
        }
    ]
