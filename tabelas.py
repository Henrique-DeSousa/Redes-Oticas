from tabulate import tabulate


def tabelas(tab, flag, index=True):
    print(tabulate(tab, headers=flag, tablefmt="simple_grid", showindex=index))