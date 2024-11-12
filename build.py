import logging
import sys
import os
import importlib
import importlib.util
import build123d.exporters3d

logging.basicConfig(level=logging.INFO)

file_path = os.path.abspath(sys.argv[1])
base = os.path.basename(file_path).removesuffix(".py")

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def show(*args, names):
    for (a, n) in zip(args, names):
        build123d.exporters3d.export_step(a, f"exports/{base}-{n}.step")

def run():
    m = load(file_path, "model")
    m.run(show)

run()

