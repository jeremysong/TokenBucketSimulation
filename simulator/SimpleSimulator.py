import numpy as np

from tb.TokenBucket import TokenBucket
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == '__main__':
    token_bucket_1 = TokenBucket(45, 45)  # 50 TPS
    token_bucket_2 = TokenBucket(95, 95)  # 100 TPS

    tier_1_traffic = list(zip(np.random.poisson(5, 100), np.arange(0, 10_000, 100)))  # 50 TPS * 10 seconds
    tier_2_traffic = list(zip(np.random.poisson(10, 100), np.arange(0, 10_000, 100)))  # 100 TPS * 10 seconds

    tier_1_throttle = np.array([(ticker, requests, token_bucket_1.acquire_with_refill(ticker, requests)[1]) for (requests, ticker) in tier_1_traffic])
    tier_2_throttle = np.array([(ticker, requests, token_bucket_2.acquire_with_refill(ticker, requests)[1]) for (requests, ticker) in tier_2_traffic])

    # print(tier_1_throttle)
    # print(tier_2_throttle)

    f, axes = plt.subplots(2, 1, figsize=(40, 8))

    sns.barplot(x=tier_1_throttle[:, 0] / 1000.0, y=tier_1_throttle[:, 1], color='b', alpha=.5, ax=axes[0])
    sns.barplot(x=tier_1_throttle[:, 0] / 1000.0, y=tier_1_throttle[:, 2], color='g', alpha=.5, ax=axes[0])

    sns.barplot(x=tier_2_throttle[:, 0] / 1000.0, y=tier_2_throttle[:, 1], color='b', alpha=.5, ax=axes[1])
    sns.barplot(x=tier_2_throttle[:, 0] / 1000.0, y=tier_2_throttle[:, 2], color='g', alpha=.5, ax=axes[1])

    plt.show()