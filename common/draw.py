from matplotlib import pyplot as plt


def draw_functions(left, right, cells_count, name, *functions):
    x = [i / cells_count for i in range(int(left * cells_count), int(right * cells_count))]
    for function, style in functions:
        y = [function(i) for i in x]
        plt.plot(x, y, style)
    plt.title(name)
    plt.grid()
    plt.draw()
    plt.show()
