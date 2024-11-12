#!/usr/bin/env python3

import logging
import sys
import importlib
import importlib.util
import build123d.exporters3d

logging.basicConfig(level=logging.INFO)

model_name = sys.argv[1]
module_name = "models." + model_name

def load(name):
    print(f"Loading {name}...")
    module = importlib.import_module(name)
    return module

def show(*args, names):
    for (a, n) in zip(args, names):
        build123d.exporters3d.export_step(a, f"exports/{model_name}-{n}.step")

def run():
    m = load(module_name)
    m.run(show)

run()

