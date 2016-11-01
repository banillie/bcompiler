# we want to test the GMPP datamap functionality

import os

from bcompiler.datamap import DatamapGMPP

dm = DatamapGMPP(
    '/home/lemon/Documents/bcompiler/source/datamap-master-to-gmpp')
dm_file = '/home/lemon/Documents/bcompiler/source/datamap-master-to-gmpp'


def test_there_is_the_correct_datamap_source_file():
    assert os.path.exists(dm_file)


def test_clean_creation_of_dm_object():
    assert dm.data[0].cellname == 'Project/Programme Name'
    assert dm.data[1].cellref == 'C5'


def test_that_empty_cell_ref_returns_none():
    assert dm.data[3].cellref is None


def test_no_single_item_datamap_lines_thanks():
    assert dm.data[2].cellname != 'JUNK'


def test_create_gmpp_datamap_object():
    assert dm.data[0].cellname, 'Project/Programme Name'
    assert dm.data[0].sheet, 'GMPP Return'
    assert dm.data[0].cellref, 'C25'
    assert dm.data[1].cellname, 'SRO Sign-Off'
    assert dm.data[1].sheet, 'GMPP Return'
    assert dm.data[1].cellref, 'C5'


def test_object_attrs():
    # there shouldn't be any single item lines in the DatamapGMPP
    assert dm._dml_cname == []
    # there shouldn't be any 2 item lines either
    assert dm._dml_cname_sheet == []
    # there should be lots of 3 item lines though!
    assert len(dm._dml_cname_sheet_cref) == 613
