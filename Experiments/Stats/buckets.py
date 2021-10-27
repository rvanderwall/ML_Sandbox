import random

def bucket_data(buckets, val, bucket_max):
    bucket_id = 0
    for max in bucket_max():
        if val < max:
            if bucket_id not in buckets:
                buckets[bucket_id] = 1
            else:
                buckets[bucket_id] += 1
            return
        bucket_id += 1

    if bucket_id not in buckets:
        buckets[bucket_id] = 1
    else:
        buckets[bucket_id] += 1
    return


def bucket_max():
    m = 10.0
    while m < 100_000.0:
        m *= 10.0
        yield m


def perc_buckets():
    m = 0.0
    while m < 1.0:
        m += 0.1
        yield m


def demo():
    histo = {}
    for ob in range(100):
        bucket_data(histo, ob, bucket_max)

    perc_histo = {}
    for p in range(100):
        v = random.random()
        bucket_data(perc_histo, v, perc_buckets)
