#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


class SystemTool:

    @classmethod
    def get_python_version(cls) -> sys.version_info:
        return sys.version_info


if __name__ == '__main__':
    print(SystemTool.get_python_version())
