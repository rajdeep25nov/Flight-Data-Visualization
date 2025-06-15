# test2.py
# This script reads an Excel file containing flight data, processes it, and visualizes the flight trajectory in 3D using Plotly.
#This is the base code for stating with dataset from Excel file and visualizing it in 3D with Plotly.
import pandas as pd
import plotly.graph_objects as go

# ✅ Load Excel
df = pd.read_excel("/Users/rajdeep/Documents/test/2023-07-04-09-36-14-5325-NAVIGATION.xlsx")

# ✅ Clean column names
df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("(", "").str.replace(")", "").str.lower()

# ✅ Parse time
df['time'] = df['time'].astype(str).str.replace(r'(\d{2}:\d{2}:\d{2}):', r'\1.', regex=True)
df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S.%f', errors='coerce')

# ✅ Drop rows with time parse issues
df = df.dropna(subset=['time'])

# ✅ Create plot
fig = go.Figure()

# Main 3D trajectory with hover
fig.add_trace(go.Scatter3d(
    x=df['longitude'],
    y=df['lattitude'],
    z=df['altitudemeters'],
    mode='lines+markers',
    marker=dict(
        size=4,
        color=df['altitudemeters'],
        colorscale='Viridis',
        opacity=0.7
    ),
    line=dict(color='blue', width=2),
    name='Flight Path',
    text=[
        f"Time: {t}<br>Roll: {r}°<br>Pitch: {p}°<br>Heading: {h}°<br>Altitude: {a} m"
        for t, r, p, h, a in zip(df['time'], df['rolldeg'], df['pitchdeg'], df['true_headingdeg'], df['altitudemeters'])
    ],
    hoverinfo='text'
))

# Start & End points
fig.add_trace(go.Scatter3d(
    x=[df['longitude'].iloc[0]],
    y=[df['lattitude'].iloc[0]],
    z=[df['altitudemeters'].iloc[0]],
    mode='markers+text',
    marker=dict(size=6, color='green'),
    text=["Start"],
    textposition="top center",
    name="Start"
))

fig.add_trace(go.Scatter3d(
    x=[df['longitude'].iloc[-1]],
    y=[df['lattitude'].iloc[-1]],
    z=[df['altitudemeters'].iloc[-1]],
    mode='markers+text',
    marker=dict(size=6, color='red'),
    text=["End"],
    textposition="top center",
    name="End"
))

fig.update_layout(
    title='3D Flight Trajectory with Hover',
    scene=dict(
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        zaxis_title='Altitude (m)'
    )
)

fig.show()
