#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import ROUND_HALF_UP, Decimal


class ArithmeticTool:

    @classmethod
    def safe_division(cls, numerator, denominator):
        """ 安全的除法 """
        return numerator / denominator if denominator else 0

    @classmethod
    def round_half_up(cls, number, ndigits: int = 0):
        """
        四舍五入计算
        具体使用时，需要根据实际情况调整
        """
        if number is None:
            return None

        multiplier = 10 ** ndigits
        number = Decimal(str(number))
        return (number * multiplier).to_integral_value(ROUND_HALF_UP) / multiplier


if __name__ == '__main__':
    print(ArithmeticTool.safe_division(3, 0))
