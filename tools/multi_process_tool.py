#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Callable, Any

from multiprocessing import Manager, Pool, Process, SimpleQueue


class Multi:
    """
    多进程处理, 加快处理速度
    使用方法: 实例化Multi对象, 然后run

    example

    def porducer_func(i):
        time.sleep(0.5)
        return i

    def consumer_func(i):
        print(i)

    producer_args = [(i,) for i in range(100)]

    mu = Multi(producer_func, consumer_func, producer_args, debug=True)
    mu.run()

    """

    def __init__(
            self,
            producer_func: Callable,
            consumer_func: Callable,
            producer_args: list[tuple[Any, ...]],
            producer_num: int = 1,
            consumer_num: int = 1,
            jobs_limit: int = 0,
            debug: bool = False,
    ):
        """
        :param: producer_func: 生产者方法, 比如: lambda x: x
        :param: consumer_func: 消费者方法, 比如: lambda x: x
        :param: producer_args: 生产者任务, 比如 [(1,), (2,), (3,), (4,)]
        :param: producer_num:  生产者数量, 默认1, 建议限制6以下, 根据实际的测试情况来选择
        :param: producer_num:  消费者数量, 默认1, 建议限制6以下, 根据实际的测试情况来选择
        :param: jobs_limit:    队列中任务的数量, 默认不限制, 当生产者和消费者的比例搭配的比较合理时队列中的数据应会很少
        :param: debug:         是否进行任务执行情况的打印, 默认不输出

        producer_func 的输出是 consumer_func 的输入
        session 需要使用 scop_session

        """
        self.producer_func = producer_func
        self.consumer_func = consumer_func
        self.producer_args = producer_args

        self.jobs_q = Manager().Queue(jobs_limit)
        self.sign_q = SimpleQueue()

        self.producer = Pool(producer_num)
        self.consumer: list[Process] = []
        self.consumer_num = consumer_num

        self.debug = debug

    def create_jobs(self) -> None:
        self.sign_q.put(1)
        for i, args in enumerate(self.producer_args):
            self.producer.apply_async(
                func=self.create_job, args=(self.jobs_q, self.producer_func, args, i)
            )

    @staticmethod
    def create_job(jobs_q: Any, produce_func: Callable, args: tuple[Any, ...], i: int) -> None:
        res = produce_func(*args)
        jobs_q.put([i, res])

    def producer_join(self) -> None:
        self.producer.close()
        self.producer.join()
        self.sign_q.get()

    def consume_jobs(self, func: Callable) -> None:
        while not (self.sign_q.empty() and self.jobs_q.empty()):
            if self.jobs_q.empty():
                continue

            i, job = self.jobs_q.get()
            if self.debug:
                print(f"---{round(i / len(self.producer_args) * 100, 2)}%---", end="\r")

            func(job)

    def start_cunsome(self) -> None:
        for _ in range(self.consumer_num):
            p = Process(target=self.consume_jobs, args=(self.consumer_func,))
            self.consumer.append(p)

        for c in self.consumer:
            c.start()

    def consumer_join(self) -> None:
        for c in self.consumer:
            c.join()

    def run(self) -> None:
        self.create_jobs()
        self.start_cunsome()
        self.producer_join()
        self.consumer_join()
