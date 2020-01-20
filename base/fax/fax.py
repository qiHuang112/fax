from matplotlib import pyplot as plt

# plt设置支持中文
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

# 工资划分的区间
sections = [36000, 144000, 300000, 420000, 660000, 960000]
# 每个区间对应的税率
rates = [0.03, 0.1, 0.2, 0.25, 0.3, 0.35, 0.45]
# 每个区间对应的速算扣除数
deductions = [0, 210, 1410, 2660, 4410, 7160, 15160]


def get_monthly_salary(default_salary, bonus: list, special, insurance):
    """
    :param default_salary: 基本工资
    :param bonus: 浮动奖金（绩效工资）一年内拿了几次工资就输入几个
    :param special: 专项扣除
    :param insurance: 五险一金比例
    :return: 返回每月工资
    """
    # 每月工资
    salary_list = []
    # 累计预扣缴额, 累计已缴税额
    total_need_tax, total_had_tax = 0, 0
    for i in bonus:
        # 当月预扣缴额(每月的应缴税 = 基本工资 + 浮动奖金(绩效工资) - 起征点 - 专项扣除 - 五险一金)
        should_tax = default_salary + i - 5000 - special - default_salary * insurance
        total_need_tax += should_tax
        # 税率区间
        index = get_index_from_sections(total_need_tax)
        # 累计应缴税额(累计应缴税额 * 税率 - 速算扣除数) 速算扣除数*12相当于一年
        total_tax = total_need_tax * rates[index] - deductions[index] * 12
        # 当月应缴税(当月累计应缴税 - 上月累计应缴税(累计已缴税))
        cur_tax = total_tax - total_had_tax
        # 当月工资(当月工资=基本工资 + 浮动奖金(绩效工资) - 当月应缴税 - 五险一金)
        cur_sal = default_salary + i - cur_tax - default_salary * insurance
        salary_list.append(cur_sal)
        total_had_tax = total_tax
    return salary_list


def get_index_from_sections(bonus):
    """
    :param bonus:税前年终奖
    :return:返回年终奖所在税率区间
    """
    index = 0
    while index < len(sections) and bonus > sections[index]:
        index = index + 1
    return index


def get_year_end_bonus(bonus):
    """
    :param bonus: 税前年终奖
    :return:返回税后年终奖
    """
    index = get_index_from_sections(bonus)
    # 年终奖纳税 = 税前年终奖 * 税率 - 速算扣除数
    tax = bonus * rates[index] - deductions[index]
    # 税后年终奖 = 税前年终奖 - 年终奖纳税
    return bonus - tax


def plot_bonus(r=range(0, 1000000), point: int = 0):
    """
    :param r: 税前年终奖区间
    :param point: 需要标出的点（税前年终奖的值）
    画出在r区间内的税前年终奖与税后年终奖曲线图，并标出point这个点
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
    返回不好的年终奖区间，如果你的年终奖在本方法返回区间，那你要注意了，你可能少拿了不少钱
    """

    def get_right(i):
        return (sections[i] - rates[i] * sections[i] + deductions[i] - deductions[i + 1]) / (1 - rates[i + 1])

    return [(sections[i], int(get_right(i))) for i in range(len(sections))]


if __name__ == '__main__':
    # plot_bonus()
    # plot_bonus(r=range(20000, 40000), point=36000)
    # plot_bonus(r=range(100000, 200000), point=144000)
    # print(get_bad_sections())
    print(get_monthly_salary(17000, [0, 500, 1000, 1200, 1500], 1500, 0.175))
