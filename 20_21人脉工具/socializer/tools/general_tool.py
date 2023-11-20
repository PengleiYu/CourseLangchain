import re
from typing import Optional, Union


def is_object_not_contains_chinese(value: object) -> bool:
    return isinstance(value, (int, float, bool)) or not contains_chinese(str(value))


def contains_chinese(s: str) -> bool:
    return bool(re.search('[\u4e00-\u9fa5]', s))


def remove_non_chinese_fields(d: Union[dict, list]):
    if isinstance(d, dict):
        to_remove = [k for k, v in d.items() if is_object_not_contains_chinese(v)]
        for k in to_remove:
            del d[k]

        for k, v in d.items():
            if isinstance(v, (dict, list)):
                remove_non_chinese_fields(v)

    elif isinstance(d, list):
        to_remove_indices = []
        for index, item in enumerate(d):
            if is_object_not_contains_chinese(item):
                to_remove_indices.append(index)
            else:
                remove_non_chinese_fields(item)

        for index in to_remove_indices:
            d.pop(index)
