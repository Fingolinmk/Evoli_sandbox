from evolve.evoli import mutate, recombinate, select_best, start_randomly
import streamlit as st
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import Band
import numpy as np
from benchmark_functions.ackley import ackley
from benchmark_functions.rosenbrock import rosenbrock

print("----")
st.title("Benchmark test")
qual_fun = None
selection = st.selectbox("Select a benchmark function", ["Ackley", "Rosenbrock"])
N = 500
if selection == "Ackley":
    qual_fun = ackley
elif selection == "Rosenbrock":
    qual_fun = rosenbrock
else:
    z = np.zeros(N, N)
p = figure(tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")])
p.x_range.range_padding = p.y_range.range_padding = 0

# must give a vector of image data for image parameter
p.grid.grid_line_width = 0
iterations = st.slider("nnumber of iteration", 1, 100)
band_plot_data = {
    "best": [],
    "worst": [],
    "avg": [],
    "base": [],
}

winners = []
xmin = ymin = -10
xmax = ymax = 10


generation = start_randomly(qual_fun, number_of_individuals=1000)
for i in range(iterations):
    generation.extend(recombinate(generation, 2000))
    generation = select_best(generation, 1000, qual_fun)
    generation = mutate(generation)

    band_plot_data["base"].append(float(i))
    band_plot_data["best"].append(generation[0]["z"])
    band_plot_data["worst"].append(generation[-1]["z"])
    z = [ind["z"] for ind in generation]
    band_plot_data["avg"].append(sum(z) / len(z))
    winners.append(generation[0])
    for ind in generation[0:1]:
        p.hex(x=ind["x"], y=ind["y"], color="cyan", size=10)
        ymin = min(ymin, ind["y"] * 1.05)
        ymax = max(ymax, ind["y"] * 1.05)

        xmin = min(xmin, ind["x"] * 1.05)
        xmax = max(xmax, ind["x"] * 1.05)

benchmark = figure(x_axis_label="iterations", y_axis_label="best fit (lower = better)")
source = ColumnDataSource(band_plot_data)
band = Band(
    base="base",
    lower="worst",
    upper="best",
    source=source,
    level="underlay",
    fill_alpha=1.0,
    line_width=1,
    line_color="black",
)

benchmark.add_layout(band)
benchmark.line(x="base", y="avg", source=source)
benchmark.line(x="base", y="best", source=source, color="grey")
benchmark.line(x="base", y="worst", source=source, color="grey")

x = np.linspace(xmin, xmax, N)
y = np.linspace(ymin, ymax, N)
xx, yy = np.meshgrid(x, y)
z = qual_fun(xx, yy)
p.image(
    image=[z],
    x=xmin,
    y=ymin,
    dw=xmax - xmin,
    dh=ymax - ymin,
    palette="Spectral11",
    level="image",
)


st.bokeh_chart(p)
st.bokeh_chart(benchmark)
st.write(winners)
