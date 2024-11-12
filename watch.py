# Optional: enable logging to see what's happening
import logging
import sys
import os
import traceback
import importlib
import importlib.util
import inotify.adapters

logging.basicConfig(level=logging.INFO)

from yacv_server import show, export_all  # Check out other exported methods for more features!

file_path = os.path.abspath(sys.argv[1])

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run():
    m = load(file_path, "model")
    m.run(show)

run()

def watch(path, cb):
    dir_path = os.path.dirname(path)
    file_name = os.path.basename(path)
    i = inotify.adapters.Inotify()
    i.add_watch(dir_path)
    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        if filename != file_name:
            continue
        if "IN_CLOSE_WRITE" not in type_names:
            continue
        logging.info(f'Reloading...')
        try:
            cb()
        except Exception:
            traceback.print_exc()

watch(file_path, run)
