def list_to_str(onelist: list) -> str:
    res = ''
    for piece in onelist:
        res += str(piece) + ';'
    return res.strip(';')


def str_to_list(onestr: str, data_type) -> list:
    return list(map(data_type, onestr.split(';')))
