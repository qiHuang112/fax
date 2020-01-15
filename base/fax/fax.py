from matplotlib import pyplot as plt


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


def plot_bonus():
    x = range(200000)
    y = [get_year_end_bonus(i) for i in x]
    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    plot_bonus()
