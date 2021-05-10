from results import Statistic
from sys import argv


if __name__ == "__main__":
    print(Statistic.save_results(argv[1], argv[2], argv[3]))