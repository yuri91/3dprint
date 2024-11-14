#!/usr/bin/env python3

import logging
import sys
import importlib
import importlib.util
import build123d.exporters3d

from util import get_args_names

logging.basicConfig(level=logging.INFO)

model_name = sys.argv[1]
module_name = "models." + model_name

def load(name):
    print(f"Loading {name}...")
    module = importlib.import_module(name)
    return module

def export_impl(*args, names):
    for (a, n) in zip(args, names):
        if hasattr(a, "part"):
            a = a.part
        build123d.exporters3d.export_step(a, f"exports/{model_name}-{n}.step")

def export(*args, names=None):
    export_impl(*args, names=names if names is not None else get_args_names())

def show(*args, **kwargs):
    pass

def run():
    m = load(module_name)
    m.run(show, export)

run()

