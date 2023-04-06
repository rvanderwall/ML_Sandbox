from os import path, makedirs
import pickle


def cache_results(fname, func, *args, **kwargs):
    if path.exists(fname):
        with open(fname, "rb") as f:
            data = pickle.load(f)
        return data

    dir_path = path.dirname(fname)
    if not path.exists(dir_path):
        try:
            makedirs(dir_path)
        except IOError as e:
            raise Exception('Unable to create dir at {}\n{}'.format(fname[:-1], e.strerror))

    data = func(*args, **kwargs)
    with open(fname, "wb") as f:
        pickle.dump(data, f)

    return data
