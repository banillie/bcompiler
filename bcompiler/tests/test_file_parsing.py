import tempfile
from datetime import date

import bcompiler.compile as compile_module
from ..compile import parse_source_cells as parse
from ..compile import run
from ..process.datamap import Datamap

TEMPDIR = tempfile.gettempdir()

AUX_DIR = "/".join([TEMPDIR, 'bcompiler'])
SOURCE_DIR = "/".join([AUX_DIR, 'source'])
RETURNS_DIR = "/".join([SOURCE_DIR, 'returns'])
OUTPUT_DIR = "/".join([AUX_DIR, 'output'])

def test_compile(populated_template, datamap):
    """
    This tests bcompiler -b X essentially (or bcompiler -a, but for a single file.
    """
    data = parse(populated_template, datamap)
    assert data[0]['gmpp_key'] == 'Project/Programme Name'
    assert data[0]['gmpp_key_value'] == 'PROJECT/PROGRAMME NAME 9'


def test_run(datamap):
    """
    This tests 'bcompiler compile' or 'bcompiler' option.
    """
    # print([item for item in dir(compile_module) if not item.startswith("__")])
    # patching module attributes to get it working
    setattr(compile_module, 'RETURNS_DIR', RETURNS_DIR)
    setattr(compile_module, 'OUTPUT_DIR', OUTPUT_DIR)
    setattr(compile_module, 'TODAY', date.today().isoformat())
    setattr(compile_module, 'DATAMAP_RETURN_TO_MASTER', datamap)
    run()


def test_datamap_class(datamap):
    """
    This tests correct creation of Datamap object.
    """
    dm = Datamap()
    dm.cell_map_from_csv(datamap)
    assert dm.cell_map[1].cell_reference == 'B49'

