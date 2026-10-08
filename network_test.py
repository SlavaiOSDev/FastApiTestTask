import asyncio
import time
import requests
import httpx
import multiprocessing
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

 # SYNC
def request(worker: str = None):
    time.sleep(10)
    print(f"Worker-{worker}, code-{200}")

    # response = requests.head("http://httpbin.org/get")
    # print(f"Worker-{worker}, code-{response.status_code}")
    # return response.status_code

def multiple_request(count: int):
    requests = [request() for _ in range(count)]
    print(requests)

# multiple_request(5)

# ASYNC
async def async_request(client: httpx.AsyncClient):
    await asyncio.sleep(3)
    return 200
    # response = await client.head("http://httpbin.org/get")
    # print(response.status_code)
    # return response.status_code


async def async_10000_request():
     async with httpx.AsyncClient() as client:
         tasks = [async_request(client) for _ in range(10000)]
         results = await asyncio.gather(*tasks)
         print(f"Всего обработано ответов: {len(results)}")


asyncio.run(async_10000_request())

# MULTITHREADING
def start_multithreading_v1(count: int):
    threads = [
        threading.Thread(target=request)
        for i in range(count)
    ]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

def start_multithreading_v2(count: int):
    threads = [
        threading.Thread(target=request, name=f"Thread-{i}", args=(f"Thread-{i}",))
        for i in range(count)
    ]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

def start_multithreading_v3(count: int):
    with ThreadPoolExecutor(max_workers=count) as executor:
        executor.map(request, range(count))


# start_multithreading_v1(count=50)
# start_multithreading_v2(count=5)
# start_multithreading_v3(count=5000)



# MULTIPROCESSING
def start_multiprocessing_v1(count: int):
    processes = [
        multiprocessing.Process(target=request)
        for i in range(count)
    ]
    for process in processes: process.start()
    for process in processes: process.join()


def start_multiprocessing_v2(count: int):
    processes = [
        multiprocessing.Process(target=request, name=f"Process-{i}", args=(f"Process-{i}",))
        for i in range(count)
    ]
    for process in processes: process.start()
    for process in processes: process.join()


def start_multiprocessing_v3(count: int):
    with ProcessPoolExecutor(max_workers=count) as executor:
        executor.map(request, range(count))#

# if __name__ == '__main__':
#     start_multiprocessing_v1(5)
#     start_multiprocessing_v2(5)
#     start_multiprocessing_v3(1500)



# ASYNCIO
# async def startAsync(count: int):
#     async with httpx.AsyncClient() as client:
#         asyncRequests = [asyncRequest() for _ in range(count)]
#         return await asyncio.gather(*asyncRequests)

# print(asyncio.run(startAsync(5)))