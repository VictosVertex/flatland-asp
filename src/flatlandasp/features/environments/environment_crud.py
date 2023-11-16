import json
from typing import Any

import numpy as np

from flatlandasp.core.utils.file_utils import create_path_if_not_exist
from flatlandasp.features.environments.schemas.environment_data_schema import \
    EnvironmentData


class TupleEncoder(json.JSONEncoder):
    """ Json encoder that turns tuples into dictionaries.

        Since json has no native representation of tuples,
        the TupleEncoder will encode every tuple into a dictionary
        with a list of elements.

    """

    def encode(self, object: Any) -> str:
        def recursion(inner_object: Any):
            # Recursive approach in order to deal with nested containers
            if isinstance(inner_object, list):
                return [recursion(element) for element in inner_object]
            if isinstance(inner_object, dict):
                return {key: recursion(value) for key, value in inner_object.items()}
            if isinstance(inner_object, tuple):
                return {'__tuple__': [recursion(element) for element in inner_object]}
            return inner_object

        return super(TupleEncoder, self).encode(recursion(object))

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def tuple_hook(object: Any):
    """ Turn tuple dictionaries back into actual tuples."""
    if '__tuple__' in object:
        return tuple(object['__tuple__'])

    if 'grid' in object:
        object['grid'] = np.array(object['grid'])

    return object


def create_data_as_json_file(*,
                             path: str,
                             file_name: str,
                             environment_data: EnvironmentData) -> None:

    create_path_if_not_exist(path=path)

    with open(f'{path}{file_name}', 'w') as f:
        f.write(json.dumps(environment_data.dict(), indent=4, cls=TupleEncoder))


def read_data_from_json_file(*,
                             path: str,
                             file_name) -> EnvironmentData:
    with open(f'{path}{file_name}', 'r') as f:
        data = json.load(f, object_hook=tuple_hook)
        return EnvironmentData(**data)
