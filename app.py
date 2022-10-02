import streamlit as st
from bokeh.plotting import figure, show
import numpy as np
from benchmark_functions.ackley import ackley
from benchmark_functions.rosenbrock import rosenbrock

st.title("Benchmark test")
N = 500
x = np.linspace(-10, 10, N)
y = np.linspace(-10, 10, N)
xx, yy = np.meshgrid(x, y)
selection=st.selectbox("Select a benchmark function",["Ackley","Rosenbrock"])
if selection=="Ackley":
    z = ackley(xx,yy)
elif selection=="Rosenbrock":
    z=rosenbrock(xx,yy)
else:
    z=np.zeros(N,N)
p = figure(tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")])
p.x_range.range_padding = p.y_range.range_padding = 0

# must give a vector of image data for image parameter
p.image(image=[z], x=0, y=0, dw=10, dh=10, palette="Spectral11", level="image")
p.grid.grid_line_width = 0.5

st.bokeh_chart(p)