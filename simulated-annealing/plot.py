import matplotlib.pyplot as plt
import numpy as np
from glob import glob

OUTPUT_DIR = 'output'


def plot_graph(path: str):
    filename = path.split('/')[-1]
    tag = filename.split('.')[0]
    with open(path) as fh:
        distance = fh.readline()

    x, y = np.loadtxt(path, skiprows=1, unpack=True)
    plt.plot(x, y, 'g-', marker='o')
    plt.title(f'Distance: {distance}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig(f'{OUTPUT_DIR}/{tag}.png')
    plt.clf()


if __name__ == '__main__':
    for path in glob(f'{OUTPUT_DIR}/*.txt'):
        plot_graph(path)
