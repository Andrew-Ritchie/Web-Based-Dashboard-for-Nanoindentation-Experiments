import plotly.graph_objects as go

import numpy as np
np.random.seed(1)

N = 2000

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x = np.random.randn(N),
        y = np.random.randn(N),
        mode = 'markers',
        marker = dict(
            line = dict(
                width = 1,
                color = 'DarkSlateGrey')
        )
    )
)

fig.update_layout(title_text = 'WebGL')

fig.show()