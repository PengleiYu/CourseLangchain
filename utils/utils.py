import functools
import logging


# 配置日志记录器，只在程序启动时执行一次


def log_function_call(func):
    """装饰器：打印函数名和函数入参"""

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # 使用functools.wraps来保留原始函数的元数据
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 获取位置参数和关键字参数的字符串表示形式，以便打印
        args_repr = [repr(a) for a in args]  # 生成位置参数列表
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 生成关键字参数的列表
        signature = ", ".join(args_repr + kwargs_repr)  # 拼接参数字符串

        # 打印函数名和参数
        # logging.debug(f"Calling function {func.__name__}({signature})")
        print(f"Calling function {func.__name__}({signature})")

        # 调用原始函数
        result = func(*args, **kwargs)

        # 打印函数结果
        # logging.debug(f"{func.__name__} returned {result!r}")
        print(f"{func.__name__} returned {result!r}")
        return result

    return wrapper


# 使用装饰器
@log_function_call
def my_function(a, b, c=None):
    return a + b if c is None else a + b + c
