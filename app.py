from evolve.evoli import select_best, start_randomly
import streamlit as st
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import Band
import numpy as np
from benchmark_functions.ackley import ackley
from benchmark_functions.rosenbrock import rosenbrock

st.title("Benchmark test")
N = 500
x = np.linspace(-10, 10, N)
y = np.linspace(-10, 10, N)
xx, yy = np.meshgrid(x, y)
qual_fun = None
selection = st.selectbox("Select a benchmark function", [
                         "Ackley", "Rosenbrock"])
if selection == "Ackley":
    z = ackley(xx, yy)
    qual_fun = ackley
elif selection == "Rosenbrock":
    z = rosenbrock(xx, yy)
    qual_fun = rosenbrock
else:
    z = np.zeros(N, N)
p = figure(tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")])
p.x_range.range_padding = p.y_range.range_padding = 0

# must give a vector of image data for image parameter
p.image(image=[z], x=-10, y=-10, dw=20, dh=20,
        palette="Spectral11", level="image")
p.grid.grid_line_width = 0.5
iterations = st.slider("nnumber of iteration", 1, 100)
band_plot_data = {
    "best": [],
    "worst": [],
    "avg": [],
    "base": [],
}

for i in range(iterations):
    band_plot_data["base"].append(float(i))
    start = start_randomly(qual_fun, number_of_individuals=100)
    band_plot_data["best"].append(start[0]["z"])
    band_plot_data["worst"].append(start[-1]["z"])
    z = [ind["z"] for ind in start]

    band_plot_data["avg"].append(sum(z)/len(z))

    for ind in start[0:1]:
        p.hex(x=ind["x"], y=ind["y"], color="cyan", size=10)


benchmark = figure(x_axis_label='iterations',
                   y_axis_label='best fit (lower = better)')
source = ColumnDataSource(band_plot_data)
band = Band(base="base", lower="worst", upper="best", source=source, level='underlay',
            fill_alpha=1.0, line_width=1, line_color='black')

benchmark.add_layout(band)
benchmark.line(x="base", y="avg", source=source)
st.bokeh_chart(p)
st.bokeh_chart(benchmark)
