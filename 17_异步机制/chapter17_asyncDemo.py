import asyncio


async def compute(x: int, y: int, callback: callable):
    print('start compute')
    await asyncio.sleep(1)
    result = x + y
    print('finish compute')


def print_result(value: int):
    print(f'result is {value}')


async def another_task():
    print("Starting another task...")
    await asyncio.sleep(1)
    print("Finished another task...")


async def main():
    print('Main start')
    task1 = asyncio.create_task(compute(3, 4, print_result))
    task2 = asyncio.create_task(another_task())

    await task1
    await task2
    print('Main ends...')


asyncio.run(main())
