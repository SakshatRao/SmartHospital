import plotly.graph_objs as go
import plotly.offline as pyo
import numpy as np

def update_graph():
    x = np.random.uniform(1, 100, 100)
    y = np.random.uniform(1, 100, 100)
    data = [go.Scatter(x = x, y = y, mode = 'markers')]
    temp = pyo.plot(data, filename = './templates/ehr/scatter.html', auto_open = False, output_type = 'file', include_plotlyjs = True)