import asyncio
import datetime
import time


def function_1(end_time, loop):
    print("function_1 called")
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, function_2, end_time, loop)


def function_2(end_time, loop):
    print("function_2 called")
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, function_3, end_time, loop)


def function_3(end_time, loop):
    print("function_3 called")
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, function_1, end_time, loop)


def function_4(end_time, loop):
    print("function_4 called")
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, function_4, end_time, loop)


loop = asyncio.get_event_loop()

end_loop = loop.time() + 2.0
loop.call_soon(function_1, end_loop, loop)
# loop.call_soon(function_4, end_loop, loop)
loop.run_forever()
loop.close()
