
class TokenBucket:
    def __init__(self, capacity, refill_rate, name='Bucket'):
        self._capacity = capacity
        self._refill_rate = refill_rate
        self._token = capacity
        self._name = name

    def refill(self, rate):
        assert self._token >= 0
        if self._token + rate > self._capacity:
            overflow = self._token + rate - self._capacity
            self._token = self._capacity
            return overflow
        else:
            self._token = self._token + rate
            return 0

    def acquire(self, token=1):
        assert self._token >= 0
        if self._token - token >= 0:
            self._token = self._token - token
            return True, token, self.__str__()
        else:
            good_put = min(self._token, token)
            self._token = 0
            return False, good_put, self.__str__()

    def acquire_with_refill(self, ticker, token=1):
        if ticker % 1000 == 0:
            self.refill(self._refill_rate)
        return self.acquire(token)

    def get_token(self):
        return self._token

    def __repr__(self):
        return f'TokenBucket(name={self._name},token={self._token})'


if __name__ == '__main__':
    t1 = TokenBucket(2, 2)  # 1 TPS
    print(t1.acquire_with_refill(1))  # acquire 1 token at 1ms
    print(t1)
    print(t1.acquire_with_refill(2))  # acquire at 2ms
    print(t1)
    print(t1.acquire_with_refill(3))  # acquire at 3ms
    print(t1)

    print(t1.acquire_with_refill(1000))  # acquire at 1s
    print(t1)
