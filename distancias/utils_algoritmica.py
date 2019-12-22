import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f"Time required: {(time.time() - start_time)*1000:.2f} ms")
        return result
    return wrapper