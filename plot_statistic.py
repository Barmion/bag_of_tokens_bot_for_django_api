import matplotlib.pylab as plt
import io
from PIL import Image

my_dict = {"Khan": 4, "Ali": 2, "Luna": 6, "Mark": 11, "Pooja": 8, "Sara": 1}

myList = sorted(my_dict.items())
x, y = zip(*myList)

plt.plot(x, y)
plt.show()

def get_plot(statistic):
    x, y = zip(statistic.items())
    plt.plot(x, y)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')

    return buf.seek(0)
