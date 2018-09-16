import os
import re
from typing import List


class DotEnvReader:
    def __init__(self, path: str):
        self.path = path

    def read(self) -> None:
        try:
            with open(self.path) as f:
                content = f.read()
        except IOError:
            return

        for line in content.splitlines():
            match = re.match(r'\A(?P<key>[A-Za-z_0-9]+)=(?P<value>.*)\Z',
                             re.sub(r'( +)?#(.+)?', '', line))
            if match:
                os.environ.setdefault(*match.groupdict().values())


class EnvValue:
    def __init__(self, key: str, default_value=None):
        self.value = os.getenv(key, default_value)

    def to_bool(self) -> bool:
        return bool(int(self.value))

    def to_list(self, separator=',') -> List:
        return self.value.split(separator)
