from ..utils import project_data_from_master
from pathlib import Path
from typing import List, Tuple


class ProjectData:
    """
    ProjectData class
    """
    def __init__(self, d: dict):
        """
        ordered_dict is easiest to get from project_data_from_master[x]
        """
        self._data = d

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def key_filter(self, key: str) -> List[Tuple]:
        data = [item for item in self._data.items() if key in item[0]]
        if not data:
            raise KeyError("Sorry, there is no matching data")
        return (data)

    def pull_keys(self, input_iter) -> List:
        """
        Returns a list of (key, value) tuples from ProjectData if key matches a
        key. The order of tuples is based on the order of keys passed in the iterable.
        """
        xs = [item for item in self._data.items() for i in input_iter if item[0] == i]
        ts = sorted(xs, key=lambda x: input_iter.index(x[0]))
        return ts


class Master:
    """
    Master class.
    """
    def __init__(self, quarter, path: Path):
        self._quarter = quarter
        self.path = Path(path)
        self._data = project_data_from_master(self.path)
        self._project_titles = [item for item in self.data.keys()]
        self.year = self._quarter.year

    def __getitem__(self, project_name):
        return ProjectData(self._data[project_name])

    @property
    def data(self):
        return self._data

    @property
    def quarter(self):
        return self._quarter.quarter

    @property
    def filename(self):
        return self.path.name

    @property
    def projects(self):
        return self._project_titles
