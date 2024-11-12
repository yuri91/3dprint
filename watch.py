#!/usr/bin/env python3

import logging
import sys
import os
import traceback
import importlib
import importlib.util
import inotify.adapters
import webbrowser

logging.basicConfig(level=logging.INFO)

from yacv_server import show

model_name = sys.argv[1]
module_name = "models." + model_name

module = importlib.import_module(module_name)
module.run(show)

def reload_and_run():
    global module
    module = importlib.reload(module)
    module.run(show)

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
