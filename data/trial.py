import main
from pathlib import Path
CSV_PATH = main.CSV_PATH


def converted():
    return Path(CSV_PATH).exists()


print(converted())
