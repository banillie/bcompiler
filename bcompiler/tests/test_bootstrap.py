import pytest

from ..process.bootstrap import AuxReport, AuxReportBlock


class TestAuxReportBlock(object):

    def test_base_AuxReportBlock(self):
        rb = AuxReportBlock('modified')
        assert rb.output[0] == """
        *******MODIFIED FILES********
        """


class TestAuxReportBase(object):

    def test_base_AuxReport(self):
        assert AuxReport.modified_files == []
        assert AuxReport.untracked_files == []
        assert AuxReport.master_files == []


    def test_add_attribute_value_Auxreport(self):
        AuxReport.modified_files.append('test')
        assert AuxReport.modified_files[0] == 'test'


    def test_add_AuxReport_instance(self):
        r = AuxReport()
        assert str(r) == "Report(['modified', 'untracked', 'master'])"


    def test_change_instance_expect_attribute_change(self):
        AuxReport.modified_files.append('test')
        assert AuxReport.modified_files[0] == 'test'
        r = AuxReport()
        assert hasattr(r, 'modified_files')
        assert r.modified_files[0] == 'test'

    def test_for_non_existing_attribute(self):
        assert not hasattr(AuxReport, 'non-existant-attr')


    def test_dynamically_adding_attribute(self):
        AuxReport.add_check_component('log')
        r = AuxReport()
        assert r.log_files == []


    def test_wrong_component_type_added(self):
        with pytest.raises(TypeError) as excinfo:
            AuxReport.add_check_component(1)
        assert excinfo.value.args[0] == "component must be a string"


    def test_get_list_of_check_components_from_instance(self):
        r = AuxReport()
        r.add_check_component('log')
        assert r.check_components[-1] == 'log'
