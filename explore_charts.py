import numpy as np
import matplotlib.pyplot as plt

def donut_chart(x)

    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    recipe = x

    data = [float(x.split()[0]) for x in recipe]
    ingredients = [x.split()[-1] for x in recipe]


    def func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        return "{:.1f}%\n({:d} g)".format(pct, absolute)


    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                      textprops=dict(color="w"))

    ax.legend(wedges, ingredients,
              title="Languages",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title("Types of Repository Languages")

    plt.show()