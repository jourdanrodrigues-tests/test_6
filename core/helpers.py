import os
import re


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
