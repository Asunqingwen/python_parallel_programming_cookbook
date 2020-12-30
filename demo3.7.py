# import multiprocessing
# import random
# import time
#
#
# class Producer(multiprocessing.Process):
#     def __init__(self, queue):
#         multiprocessing.Process.__init__(self)
#         self.queue = queue
#
#     def run(self):
#         for i in range(10):
#             item = random.randint(0, 256)
#             self.queue.put(item)
#             print("Process Producer : item %d appended to queue %s" % (item, self.name))
#             time.sleep(1)
#             print("The size of queue is %s" % self.queue.qsize())
#
#
# class Consumer(multiprocessing.Process):
#     def __init__(self, queue):
#         multiprocessing.Process.__init__(self)
#         self.queue = queue
#
#     def run(self):
#         while True:
#             if self.queue.empty():
#                 print("the queue is empty")
#                 break
#             else:
#                 time.sleep(2)
#                 item = self.queue.get()
#                 print('Process Consumer : item %d popped from by %s \n' % (item, self.name))
#                 time.sleep(1)
#
#
# if __name__ == '__main__':
#     queue = multiprocessing.Queue()
#     process_producer = Producer(queue)
#     process_consumer = Consumer(queue)
#     process_producer.start()
#     process_consumer.start()
#     process_producer.join()
#     process_consumer.join()

import multiprocessing


def create_items(pipe):
    output_pipe, _ = pipe
    for item in range(10):
        output_pipe.send(item)
    output_pipe.close()


def multiply_items(pipe_1, pipe_2):
    close, input_pipe = pipe_1
    close.close()
    output_pipe, _ = pipe_2
    try:
        while True:
            item = input_pipe.recv()
            output_pipe.send(item * item)
    except EOFError:
        output_pipe.close()


if __name__ == '__main__':
    # 第一个进程管道发出数字
    pipe_1 = multiprocessing.Pipe(True)
    process_pipe_1 = multiprocessing.Process(target=create_items, args=(pipe_1,))
    process_pipe_1.start()

    # 第二个进程管道接收数字并计算
    pipe_2 = multiprocessing.Pipe(True)
    process_pipe_2 = multiprocessing.Process(target=multiply_items, args=(pipe_1, pipe_2,))
    process_pipe_2.start()
    pipe_1[0].close()
    pipe_2[0].close()
    try:
        while True:
            print(pipe_2[1].recv())
    except EOFError:
        print("End")
