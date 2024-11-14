#!/usr/bin/env python3

import logging
import sys
import os
import traceback
import importlib
import importlib.util
import inotify.adapters
import webbrowser

from util import get_args_names

logging.basicConfig(level=logging.INFO)

import yacv_server

def export(*parts, **kwargs):
    pass

def show(*parts, names=None):
    if names is None:
        mynames = get_args_names()
    else:
        mynames = names
    yacv_server.show(*parts, names=mynames)

model_name = sys.argv[1]
module_name = "models." + model_name

module = importlib.import_module(module_name)
module.run(show, export)

def reload_and_run():
    global module
    module = importlib.reload(module)
    module.run(show, export)

def watch():
    dir_path = os.path.dirname(os.path.abspath(__file__)) + "/models"
    file_name = model_name + ".py"
    i = inotify.adapters.Inotify()
    i.add_watch(dir_path)
    try:
        for event in i.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event
            if filename != file_name:
                continue
            if "IN_CLOSE_WRITE" not in type_names:
                continue
            logging.info(f'Reloading...')
            try:
                reload_and_run()
            except KeyboardInterrupt:
                print("Exiting...")
                return
            except Exception:
                traceback.print_exc()
    except KeyboardInterrupt:
        print("Exiting...")
        return

webbrowser.open_new("https://yeicor-3d.github.io/yet-another-cad-viewer/")

watch()
