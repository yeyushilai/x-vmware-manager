#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import time
import random


class IDGenerator:

    @classmethod
    def gen_uuid(cls):
        new_uuid = uuid.uuid4()
        return str(new_uuid)

    @classmethod
    def gen_timestamp_id(cls):
        return int(time.time() * 1000000) + random.randint(1000, 9999)


if __name__ == '__main__':
    print(IDGenerator.gen_uuid())
    print(IDGenerator.gen_timestamp_id())
