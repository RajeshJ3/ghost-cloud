
def pop_from_data(data, **items):
    for _ in items:
        if _ in data:
            data.pop(_)
    return data
