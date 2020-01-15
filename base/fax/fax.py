from matplotlib import pyplot as plt

# plt设置支持中文
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']


def get_index_from_sections(bonus, sections: list):
    """
    :param bonus:税前年终奖
    :param sections:根据年终奖划分的不同税率区间
    :return:返回年终奖所在税率区间
    """
    index = 0
    while index < len(sections) and bonus > sections[index]:
        index = index + 1
    return index


def get_year_end_bonus(bonus):
    """
    :param bonus: 税前年终奖
    :return:税后年终奖
    """
    sections = [36000, 144000, 300000, 420000, 660000, 960000]
    rates = [0.03, 0.1, 0.2, 0.25, 0.3, 0.35, 0.45]
    deductions = [0, 210, 1410, 2660, 4410, 7160, 15160]
    index = get_index_from_sections(bonus, sections)
    # 年终奖纳税 = 税前年终奖 * 税率 - 速算扣除数
    tax = bonus * rates[index] - deductions[index]
    # 税后年终奖 = 税前年终奖 - 年终奖纳税
    return bonus - tax


def plot_bonus(r=range(0, 1000000), point: int = 0):
    """
    :param r: 税前年终奖区间
    :param point: 需要标出的点（税前年终奖的值）
    """
    x = r
    y = [get_year_end_bonus(i) for i in x]
    plt.plot(x, y)
    plt.xlabel('税前年终奖')
    plt.ylabel('税后年终奖')

    if point != 0:
        plt.scatter(x=point, y=get_year_end_bonus(point))
        p1 = r'(%d, %d)' % (point, get_year_end_bonus(point))
        plt.annotate(p1, xy=(point, get_year_end_bonus(point)))
    plt.show()


def get_bad_sections():
    """
    如果你的年终奖在本方法打印的区间，那你要注意了，你可能少拿了不少钱
    """
    sections = [36000, 144000, 300000, 420000, 660000, 960000]
    rates = [0.03, 0.1, 0.2, 0.25, 0.3, 0.35, 0.45]
    deductions = [0, 210, 1410, 2660, 4410, 7160, 15160]

    def get_right(i):
        return (sections[i] - rates[i] * sections[i] + deductions[i] - deductions[i + 1]) / (1 - rates[i + 1])

    res = [(sections[i], int(get_right(i))) for i in range(len(sections))]
    print(res)


if __name__ == '__main__':
    # plot_bonus()
    # plot_bonus(r=range(20000, 40000), point=36000)
    # plot_bonus(r=range(100000, 200000), point=144000)
    get_bad_sections()
