import asyncio
from functools import partial, wraps 
from ... import user_data

def _update_user_ldata(user_id: int, key: str, value):
    data = user_data.get(user_id)
    if data is None:
        data = {}
        user_data[user_id] = data
    if value is None:
        if key in data:
            data.pop(key)
        if not data:
            user_data.pop(user_id, None)
        return
    data[key] = value


def _get_readable_time(seconds: int) -> str:
    count = 0
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]
    while count < 4:
        count += 1
        remainder, result = divmod(int(seconds), 60) if count < 3 else divmod(
            int(seconds), 24
        )
        if seconds == 0 and result == 0:
            break
        time_list.append(f"{result}{time_suffix_list[count - 1]}")
        seconds = remainder
    time_list.reverse()
    return " ".join(time_list)


async def _sync_to_async(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    pfunc = partial(func, *args, **kwargs)
    return await loop.run_in_executor(None, pfunc)

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def _task(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        task = loop.create_task(func(*args, **kwargs))
        return task

    return wrapper
