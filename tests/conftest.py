# Lets pytest find the pllmodel package when run from the repo root.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
