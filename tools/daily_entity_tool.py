#!/usr/bin/env python
# -*- coding: utf-8 -*-

from email_validator import validate_email, EmailNotValidError


class DailyEntityTool:

    @classmethod
    def is_email_valid(cls, value):
        """ 检查是否为邮箱地址 """
        try:
            validate_email(value)
            return True
        except EmailNotValidError as e:
            print(str(e))
            return False


if __name__ == '__main__':
    print(DailyEntityTool.is_email_valid("xxxfo@xmail.com"))
