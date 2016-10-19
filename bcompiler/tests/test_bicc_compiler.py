import csv
import os
import unittest

import sys

from bcompiler.bcompiler import create_master_dict_transposed, clean_datamap, create_datamap_n_tuples
from bcompiler.utils import VALIDATION_REFERENCES
from bcompiler.compile import parse_source_cells
from bcompiler.datamap import Datamap, DatamapLine
from bcompiler.utils import DATAMAP_RETURN_TO_MASTER


class TestMasterFunctions(unittest.TestCase):
    def setUp(self):
        self.docs = os.path.join(os.path.expanduser('~'), 'Documents')
        bcomp_working_d = 'bcompiler'
        self.path = os.path.join(self.docs, bcomp_working_d)
        self.source_path = os.path.join(self.path, 'source')
        self.output_path = os.path.join(self.path, 'output')
        self.datamap_master_to_returns = os.path.join(self.source_path, 'datamap-master-to-returns')
        self.datamap_returns_to_master = os.path.join(self.source_path, 'datamap-returns-to-master')
        self.master = os.path.join(self.source_path, 'master.csv')
        self.transposed_master = os.path.join(self.source_path, 'master_transposed.csv')
        self.example_return = os.path.join(self.source_path, 'returns/Q2 16-17 BICC SAR H - Final.xlsx')

    #    def test_presence_working_directory_location(self):
    #        # let's say we'll create a new bcomipler directory in the user space
    #        # inside this directory will be a source and an output directory
    #        # which is where our key files will go
    #        # source/master.csv
    #        # source/bicc_template.xlsx
    #        # source/datamap
    #        # output/West Midlands Franchise Competition.xlsx
    #        create_working_directory()
    #        self.assertTrue(os.path.exists(self.path))
    #        self.assertTrue(os.path.exists(self.source_path))
    #        self.assertTrue(os.path.exists(self.output_path))

    def test_presence_base_master_csv(self):
        self.assertTrue(os.path.exists(self.master))

    def test_presence_transposed_csv(self):
        create_master_dict_transposed(self.master)
        self.assertTrue(os.path.exists(self.transposed_master))

    def test_for_individual_project_data_lines(self):
        test_st = "Project/Programme Name,Classification,SRO Sign-Off,FD Sign-Off,"
        len_test_st = len(test_st)
        with open(self.transposed_master, 'r') as f:
            f_line = f.readline(len_test_st)
            self.assertEqual(f_line, test_st)

    def test_presence_datamap(self):
        self.assertTrue(os.path.exists(self.datamap_master_to_returns))

    def test_clean_datamap(self):
        dirty_text = "Project/Programme Name,Summary,B5,\n" \
                     "Project/Programme Name,Classification,SRO Sign-Off,FD Sign-Off\n"
        clean_text = "Project/Programme Name,Summary,B5,\n" \
                     "Project/Programme Name,Classification,SRO Sign-Off,FD Sign-Off,\n"
        tmp_dirty = open('/tmp/dirty_temp', mode='w+', encoding='utf-8')
        tmp_dirty.write(dirty_text)
        tmp_dirty.close()
        tmp_clean = open('/tmp/clean_temp', mode='w+', encoding='utf-8')
        tmp_clean.write(clean_text)
        cmdm = clean_datamap('/tmp/dirty_temp')
        self.assertEqual(cmdm.read(), tmp_clean.read())
        tmp_clean.close()
        os.unlink('/tmp/dirty_temp')
        os.unlink('/tmp/clean_temp')

    def test_for_data_migrated_to_blank_form(self):
        selected_data = {}
        with open(self.transposed_master, 'r') as f:
            projects = list([row for row in csv.DictReader(f)])
            project = projects[0]
            selected_data['Project/Programme Name'] = project['Project/Programme Name']
            selected_data['SRO Sign-Off'] = project['SRO Sign-Off']
            selected_data['Change Delivery Methodology'] = project['Change Delivery Methodology']
        # pass for now
        pass

    @unittest.skip("skipping tests that reference old datamap file")
    def test_parse_returned_form(self):
        return_f = self.example_return
        data = parse_source_cells(return_f)
        self.assertEqual(data[0]['gmpp_key'], 'Project/Programme Name')

    @unittest.skip("skipping tests that reference old datamap file")
    def test_dropdown_not_passing_to_master_bug(self):
        return_f = self.example_return
        data = parse_source_cells(return_f)
        example_validated_cell = "IO1 - Monetised?"
        matches = [x for x in data if x['gmpp_key'] == example_validated_cell]
        self.assertEqual(matches[0]['gmpp_key'], example_validated_cell)

    # trial of creating list of named tuples from the datamap - not sure why yet
    def test_list_of_named_tuples_from_datamap(self):
        clean_datamap(DATAMAP_RETURN_TO_MASTER)
        datamap_data = create_datamap_n_tuples()
        self.assertEqual(datamap_data[0][0], 'Project/Programme Name')


class TestDatamapFunctionality(unittest.TestCase):
    def setUp(self):
        self.docs = os.path.join(os.path.expanduser('~'), 'Documents')
        bcomp_working_d = 'bcompiler'
        self.path = os.path.join(self.docs, bcomp_working_d)
        self.source_path = os.path.join(self.path, 'source')
        self.output_path = os.path.join(self.path, 'output')
        self.datamap_master_to_returns = os.path.join(self.source_path, 'datamap-master-to-returns')
        self.datamap_returns_to_master = os.path.join(self.source_path, 'datamap-returns-to-master')
        self.master = os.path.join(self.source_path, 'master.csv')
        self.transposed_master = os.path.join(self.source_path, 'master_transposed.csv')
        self.dm = Datamap(type='returns-to-master', source_file=self.datamap_returns_to_master)

    def test_verified_lines(self):
        # these are DatamapLine objects that have 4 attributes, the last of which is verification
        # dropdown text
        self.assertEqual(self.dm.verified_lines, 116)

    def test_verified_lines_for_dropdown_text(self):
        # we're expecting the dropdown_txt attr in the DatamapLine object to be what we expect
        for item in self.dm.dml_with_verification:
            self.assertTrue(item.dropdown_txt in VALIDATION_REFERENCES.keys())

    def test_non_verified_lines(self):
        # these are DatamapLine objects that have 3 attributes, the last of which is a regex
        self.assertEqual(self.dm.non_verified_lines, 715)

    @unittest.skip("Skip until sure about amounts")
    def test_cells_that_will_not_migrate(self):
        # these are DatamapLine objects that have 2 attributes, the last of which is a sheet ref
        self.assertEqual(self.dm.non_tranferring_value_lines, 20)

    @unittest.skip("Skip until sure about amounts")
    def test_single_item_lines(self):
        # DatamapLines that have a single attribute
        self.assertEqual(self.dm.single_item_lines, 20)

    def test_datamap_is_cleaned_attr(self):
        self.assertTrue(self.dm.is_cleaned)

    def test_dataline_object(self):
        dml = DatamapLine()
        pass


if __name__ == "__main__":
    unittest.main()
