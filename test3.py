#this is the test3.py file in which we are going to visualize the flight trajectory in 3D using Plotly.
# we will be using the dataset from Excel file and visualizing it in 3D with Plotly.
# data cleaning, time parsing, and adaptive data reduction.
# and many errors are handled in this code.
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Load and clean data
try:
    df = pd.read_excel("/Users/rajdeep/Documents/test/2023-07-04-09-36-14-5325-NAVIGATION.xlsx")
    print(f"Loaded {len(df)} rows from Excel file.")
except FileNotFoundError:
    print("Bro Errorrr: File not found. Please ensure the file path is correct.")
    exit()

# Standardize column names
df.columns = (df.columns.str.strip()
              .str.lower()
              .str.replace(r'[()\s]', '', regex=True)
              .str.replace('deg', '')
              .str.replace('meters', ''))

# Rename columns for consistency
df = df.rename(columns={'lattitude': 'latitude', 'trueheading': 'heading'})
print(f"Columns after renaming: {list(df.columns)}")

# Required columns
required_cols = ['time', 'latitude', 'longitude', 'altitude']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    print(f"Error: Missing required columns: {missing_cols}")
    exit()

# Inspect the first few time values
print("Sample time values before parsing:")
print(df['time'].head(10).to_list())

# Time formatting with multiple format attempts
time_formats = ['%H:%M:%S.%f', '%H:%M:%S', '%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S']
df['time'] = None
for fmt in time_formats:
    try:
        df['time'] = pd.to_datetime(df['time'].astype(str), format=fmt, errors='coerce')
        if df['time'].notna().sum() > 0:
            print(f"Successfully parsed time with format: {fmt}")
            break
    except Exception as e:
        print(f"Failed to parse with format {fmt}: {e}")
else:
    print("Warningggg Dude: All time parsing attempts failed. Using original data without time sorting.")

# Drop rows with invalid time (if parsing succeeded)
if df['time'].notna().sum() > 0:
    df = df.dropna(subset=['time']).sort_values('time').reset_index(drop=True)
else:
    print("Using all rows without time sorting due to parsing failure.")
    df['time'] = range(len(df))  # Fallback: use index as time
print(f"Rows after time cleaning: {len(df)}")

# Drop rows with missing required columns
df = df.dropna(subset=required_cols)
print(f"Rows after dropping missing values: {len(df)}")

# Adaptive data reduction: aim for 10–100 points
target_points = min(max(10, len(df) // 100), 100)
step = max(1, len(df) // target_points)
df_reduced = df.iloc[::step].copy()
print(f"Reduced to {len(df_reduced)} points with step={step}")

# Ensure sufficient data points
if len(df_reduced) < 2:
    print("Warninggggg : Using all available points due to small dataset.")
    df_reduced = df.copy()

if len(df_reduced) < 2:
    print("Error: Bro still not enough data points. At least 2 points required.")
    exit()

# Create start and end markers
start_marker = go.Scatter3d(
    x=[df_reduced['longitude'].iloc[0]],
    y=[df_reduced['latitude'].iloc[0]],
    z=[df_reduced['altitude'].iloc[0]],
    mode='markers+text',
    marker=dict(size=8, color='green'),
    text=["Start"],
    textposition="top center",
    name='Start'
)

end_marker = go.Scatter3d(
    x=[df_reduced['longitude'].iloc[-1]],
    y=[df_reduced['latitude'].iloc[-1]],
    z=[df_reduced['altitude'].iloc[-1]],
    mode='markers+text',
    marker=dict(size=8, color='red'),
    text=["End"],
    textposition="top center",
    name='End'
)

# Create animation frames (limit to 50 frames)
num_frames = min(50, len(df_reduced) - 1)
if num_frames > 0:
    frame_indices = np.linspace(1, len(df_reduced) - 1, num_frames, dtype=int)
else:
    frame_indices = [1]

frames = []
for i in frame_indices:
    frames.append(go.Frame(
        data=[go.Scatter3d(
            x=df_reduced['longitude'][:i+1],
            y=df_reduced['latitude'][:i+1],
            z=df_reduced['altitude'][:i+1],
            mode='lines+markers',
            marker=dict(size=3, color='blue'),
            line=dict(width=3, color='blue'),
            hoverinfo='text',
            text=df_reduced['time'].astype(str)[:i+1]
        )],
        name=f'frame{i}'
    ))

# Base figure
fig = go.Figure(
    data=[
        start_marker,
        end_marker,
        go.Scatter3d(
            x=df_reduced['longitude'][:1],
            y=df_reduced['latitude'][:1],
            z=df_reduced['altitude'][:1],
            mode='lines+markers',
            marker=dict(size=3, color='blue'),
            line=dict(width=3, color='blue'),
            name='Flight Path'
        )
    ],
    layout=go.Layout(
        title="3D Flight Trajectory Animation",
        scene=dict(
            xaxis_title='Longitude',
            yaxis_title='Latitude',
            zaxis_title='Altitude (m)',
            aspectmode='auto'
        ),
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[
                dict(label="Play",
                     method="animate",
                     args=[None, {"frame": {"duration": 100, "redraw": True},
                                  "fromcurrent": True,
                                  "mode": "immediate"}]),
                dict(label="Pause",
                     method="animate",
                     args=[[None], {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate"}])
            ],
            direction="left",
            pad={"r": 10, "t": 87},
            x=0.1,
            xanchor="left",
            y=0,
            yanchor="top"
        )],
        showlegend=True
    ),
    frames=frames
)

# Adjust axis ranges to fit data
fig.update_scenes(
    xaxis=dict(range=[df_reduced['longitude'].min() - 0.0001, df_reduced['longitude'].max() + 0.0001]),
    yaxis=dict(range=[df_reduced['latitude'].min() - 0.0001, df_reduced['latitude'].max() + 0.0001]),
    zaxis=dict(range=[df_reduced['altitude'].min() - 10, df_reduced['altitude'].max() + 10])
)

print("Rendering plot...")
fig.show()