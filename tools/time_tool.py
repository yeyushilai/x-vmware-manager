#!/usr/bin/env python
#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import datetime


class TimeTool:

    @classmethod
    def get_utc_timestamp(cls):
        """获取UTC时间的时间戳"""
        return cls.get_local_timestamp() + time.timezone

    @classmethod
    def get_local_timestamp(cls):
        """获取本地时间的时间戳"""
        return time.time()

    @classmethod
    def get_utc_time(cls):
        """
        获取datetime格式的UTC时间
        :return: datetime格式的utc时间
        """
        # 方法一: datetime.datetime(2022, 8, 29, 12, 19, 21, 889000)
        utc_time = datetime.datetime.fromtimestamp(cls.get_utc_timestamp())

        # 方法二: datetime.datetime(2022, 8, 29, 12, 19, 23, 69000)
        # utc_time = datetime.datetime.utcfromtimestamp(time.time())

        return utc_time

    @classmethod
    def get_local_time(cls):
        """
        获取datetime格式的本地时间
        :return: datetime格式的本地时间
        """
        # 方法一:
        local_time = datetime.datetime.fromtimestamp(cls.get_local_timestamp())

        # 方法二：
        # local_time = datetime.datetime.now()

        return local_time

    @classmethod
    def get_utc_time_str(cls):
        """
        获取字符串格式的UTC时间
        :return: 字符串格式的utc时间
        """

        utc_time = cls.get_utc_time()
        utc_time_str = cls.datetime_to_str(utc_time)
        return utc_time_str

    @classmethod
    def get_local_time_str(cls):
        """
        获取字符串格式的本地时间
        :return: 字符串格式的本地时间
        """
        local_time = cls.get_local_time()
        local_time_str = cls.datetime_to_str(local_time)
        return local_time_str

    @classmethod
    def get_yesterday_utc_time(cls):
        """
        获取昨天此刻的UTC时间
        :return: datetime格式的昨天此刻的UTC时间
        """

        utc_time = cls.get_utc_time()
        return utc_time + datetime.timedelta(days=-1)

    @classmethod
    def get_yesterday_local_time(cls):
        """
        获取昨天此刻的本地时间
        :return: datetime格式的昨天此刻的本地时间
        """
        local_time = cls.get_local_time()
        return local_time + datetime.timedelta(days=-1)

    @classmethod
    def timestamp_to_str(cls, timestamp=None):
        """
        获取字符串格式的时间
        :param timestamp: 时间戳，格式为浮点型，默认为本地时间
        :return: 返回字符串格式的时间，例如'2022-08-29T09:13:06Z'
        """
        timestamp = timestamp or cls.get_local_timestamp()
        datetime_time = cls.timestamp_to_datetime(timestamp)
        str_time = cls.datetime_to_str(datetime_time)
        return str_time

    @classmethod
    def timestamp_to_datetime(cls, timestamp):
        """
        将时间戳转换为本地datetime格式的时间
        :param timestamp: 时间戳
        :return: datetime格式的时间
        """
        return datetime.datetime.fromtimestamp(timestamp)

    @classmethod
    def datetime_to_str(cls, datetime_time, s_format="%Y-%m-%dT%H:%M:%SZ"):
        """
        将datetime格式的时间转换为字符串格式的时间
        :param datetime_time: datetime格式的时间
        :param s_format: 字符串格式时间的具体格式，常见的有"%Y-%m-%dT%H:%M:%SZ"
        :return: 字符串格式的时间，例如'2022-08-29T09:13:06Z'
        """
        return datetime_time.strftime(s_format)

    @classmethod
    def datetime_to_timestamp(cls, datetime_time):
        """
        将datetime格式的时间转换为浮点型的时间戳
        :param datetime_time: datetime格式的时间
        :return: 浮点型的时间戳，比如1661778641.0
        """
        assert isinstance(datetime_time, datetime.datetime)
        timetuple = datetime_time.timetuple()
        timestamp = time.mktime(timetuple)
        return timestamp

    @classmethod
    def str_to_datetime(cls, str_time, s_format="%Y-%m-%dT%H:%M:%SZ"):
        """
        将字符串格式的时间转换为datetime格式的时间
        :param str_time: 字符串格式的时间
        :param s_format: 字符串格式时间的具体格式，常见的有"%Y-%m-%dT%H:%M:%SZ"
        :return: datetime格式的时间
        """
        return datetime.datetime.strptime(str_time, s_format)

    @classmethod
    def str_to_timestamp(cls, str_time, s_format="%Y-%m-%dT%H:%M:%SZ"):
        """
        将字符串格式的时间转换为浮点型的时间戳
        :param str_time: 字符串格式的时间
        :param s_format: 字符串格式时间的具体格式，默认有"%Y-%m-%dT%H:%M:%SZ"
        :return: 浮点型的时间戳，比如1661778641.0
        """
        datetime_time = cls.str_to_datetime(str_time, s_format)
        timestamp = cls.datetime_to_timestamp(datetime_time)
        return timestamp

    @classmethod
    def utc_to_local(cls, datetime_time):
        """
        将datetime格式的UTC时间，转换为datetime格式的本地时间
        :param datetime_time: datetime格式的UTC时间
        :return: datetime格式的本地时间
        """
        pass

    @classmethod
    def local_to_utc(cls, datetime_time):
        """
        将datetime格式的本地时间，转换为datetime格式的UTC时间
        :param datetime_time: datetime格式的本地时间
        :return: datetime格式的UTC时间
        """
        pass

    @classmethod
    def utc_str_to_local_str(cls, str_time):
        """
        将字符串格式的UTC时间，转换为字符串格式的本地时间
        :param str_time: 字符串格式的UTC时间
        :return: 字符串格式的本地时间
        """
        utc_time = datetime.datetime.strptime(str_time, "%Y-%m-%dT%H:%M:%SZ")
        return utc_time + datetime.timedelta(hours=8)

    @classmethod
    def local_str_to_utc_str(cls, str_time):
        """
        将字符串格式的本地时间，转换为字符串格式的UTC时间
        :param str_time: 字符串格式的时间
        :return: 字符串格式的UTC时间
        """
        pass

    @classmethod
    def statistics_time(cls, func):
        def int_time(*args, **kwargs):
            start_time = datetime.datetime.now()
            res = func(*args, **kwargs)
            over_time = datetime.datetime.now()
            num = round(float((over_time - start_time).total_seconds()))
            print(f'函数{func.__name__}执行完毕，共计消耗{num}秒')
            return res

        return int_time


if __name__ == '__main__':
    print(TimeTool.get_local_time())
    print(TimeTool.get_local_time_str())
    print(TimeTool.get_local_timestamp())
    print(TimeTool.get_utc_time())
    print(TimeTool.get_utc_time_str())
    print(TimeTool.get_utc_timestamp())
    print(TimeTool.get_yesterday_local_time())
    print(TimeTool.get_yesterday_utc_time())
