from collections import defaultdict, UserDict


class PQLDict(UserDict):
    _SEPARATOR = '->'
    _REPLACER = '|'

    def __init__(self, *args, **kwargs):
        _dict = args[0]
        prepared_dict = {}
        for key, item in _dict.items():
            cleared_key = key.replace(self._SEPARATOR, self._REPLACER)
            prepared_dict[cleared_key] = item
        new_args = (prepared_dict, *args[1:])
        super().__init__(*new_args, **kwargs)

    def __getitem__(self, key):
        key_chain, real_key = self._split_keys(key)
        return self._get_last_obj_in_chain(key_chain)[real_key]

    def __setitem__(self, key, val):
        key_chain, real_key = self._split_keys(key)
        self._get_last_obj_in_chain(key_chain)[real_key] = val

    def _get_last_obj_in_chain(self, key_chain):
        obj = self.data
        for key in key_chain:
            obj = obj[key]
        return obj

    def _split_keys(self, key):
        keys = key.split(self._SEPARATOR)
        return keys[:-1], keys[-1]


class Pipeline:
    def __init__(self, pipeline):
        self._pipeline = pipeline

    def execute(self, objects):
        objects = list(map(PQLDict, objects))
        for step in self._pipeline:
            objects = step.execute(objects)
        return objects


class BaseStep:
    def execute(self, objects):
        raise NotImplementedError


class Filter(BaseStep):
    def __init__(self, field, filter_func):
        self._field = field
        self._filter_func = filter_func

    def execute(self, objects):
        return [obj for obj in objects if self._filter_func(obj[self._field])]


class GroupBy(BaseStep):
    def __init__(self, field, aggregation_func):
        self._field = field
        self._aggregation_func = aggregation_func

    def execute(self, objects):
        groups = defaultdict(list)
        for obj in objects:
            groups[obj[self._field]].append(obj)

        aggregated = []
        for group_name, group_objects in groups.items():
            aggregation_field_name = self._aggregation_func.__name__
            aggregated.append(PQLDict(
                {self._field: group_name,
                 aggregation_field_name: self._aggregation_func(group_objects)}))

        return aggregated


class Limit(BaseStep):
    def __init__(self, limit):
        self._limit = limit

    def execute(self, objects):
        return objects[:self._limit]


class OrderBy(BaseStep):
    def __init__(self, field, reverse=False):
        self._field = field
        self._reverse = reverse

    def execute(self, objects):
        return sorted(objects, key=lambda obj: obj[self._field], reverse=self._reverse)
