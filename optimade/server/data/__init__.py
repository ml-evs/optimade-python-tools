""" Test Data to be used with the OPTIMADE server """
import bson.json_util
from pathlib import Path


data_paths = {
    "structures": "test_structures.json",
    "references": "test_references.json",
    "links": "test_links.json",
}


for var, path in data_paths.items():
    with open(Path(__file__).parent / path) as f:
        globals()[var] = bson.json_util.loads(f.read())
