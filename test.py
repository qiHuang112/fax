from matplotlib import pyplot as plt


def test1():
    x = [0.01 * i for i in range(1000)]
    plt.plot(x, [2 ** i for i in x])
    plt.show()


if __name__ == '__main__':
    test1()
