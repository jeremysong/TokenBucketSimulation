import random

from tb.TokenBucket import TokenBucket


class HierarchicalTokenBucket:
    def __init__(self, capacity, refill_rate, num_tbs):
        self._capacity = capacity // num_tbs  # make sure capacity is an integer
        self._refill_rate = refill_rate // num_tbs  # make sure capacity is an integer
        self._token_buckets = list([TokenBucket(self._capacity, self._refill_rate, f"{i}") for i in range(0, num_tbs)])

    def refill(self, ticker):
        if ticker % 1000 == 0:  # refill every 1000 millisecond
            overflow = self._refill_rate
            for index, token_bucket in enumerate(self._token_buckets):
                # print(f"overflow: {overflow}")
                assert 0 <= overflow <= self._capacity
                overflow = token_bucket.refill(overflow)

    def acquire(self, ticker, tokens):
        self.refill(ticker)
        return list(self._token_buckets[bucket].acquire(token)[1] for bucket, token in enumerate(tokens))

    def get_token_buckets(self):
        return self._token_buckets

    def __str__(self):
        return self._token_buckets.__str__()


if __name__ == '__main__':
    htb = HierarchicalTokenBucket(2, 2, 2)  # 1 TPS for each bucket
    print(htb.acquire(1, [1, 1]))  # acquire 1 token at 1ms for bucket 0

    print(htb.acquire(2, [1, 1]))  # acquire at 2ms for bucket 0
    # print(htb)

    print(htb.acquire(3, [1, 1]))  # acquire at 3ms for bucket 0
    # print(htb)

    print(htb.acquire(1000, [1, 1]))  # acquire at 1s for bucket 0
    # print(htb)

    print(htb.acquire(1001, [1, 1]))  # acquire at 1s for bucket 0
    # print(htb)
