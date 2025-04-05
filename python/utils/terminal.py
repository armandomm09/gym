import sys

def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """
    :param iteration: Current iteration.
    :param total: Total iterations.
    :param prefix: Text to display before the progress bar.
    :param suffix: Text to display after the progress bar.
    :param decimals: Number of decimals in the percentage.
    :param length: Length of the progress bar.
    :param fill: Character used to fill the progress bar.
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.write("\033[s")
    sys.stdout.write("\033[999;1H")
    sys.stdout.write("\033[K")
    sys.stdout.write(f'{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.write("\033[u")
    sys.stdout.flush()
    if iteration == total:
        print()