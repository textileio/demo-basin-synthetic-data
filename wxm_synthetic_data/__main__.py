import sys

from wxm_synthetic_data.wxm_synthetic_data import fib

if __name__ == "__main__":
    n = int(sys.argv[1])
    print(fib(n))
