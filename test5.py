#this script processes flight data from an Excel file and creates a 3D animated plot of the flight trajectory using Plotly.
#     in this code we have added hover tooltips to display detailed information about each point in the flight path.
# this is the final version of the code that visualizes the flight trajectory in 3D using Plotly.
# Drop rows with missing required columns

import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Load and clean data
try:
    df = pd.read_excel("/Users/rajdeep/Documents/test/2023-07-04-09-36-14-5325-NAVIGATION.xlsx")
    print(f"Loaded {len(df)} rows from Excel file.")
except FileNotFoundError:
    print("Errorrrrrrr dude fix it: File not found. Please ensure the file path is correct.")
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
    print(f"Errorrrrr bro: Missing required columns: {missing_cols}")
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
    print("Warninggg bro: All time parsing attempts failed. Using original data without time sorting.")

# Drop rows with invalid time (if parsing succeeded)
if df['time'].notna().sum() > 0:
    df = df.dropna(subset=['time']).sort_values('time').reset_index(drop=True)
else:
    print("Using all rows without time sorting due to parsing failurerrr.")
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
    print("Warninggggg bro: Using all available points due to small dataset.")
    df_reduced = df.copy()

if len(df_reduced) < 2:
    print("Error: Still not enough data points. at least 2 points required.")
    exit()

# Create hover text for all points
hover_text = [
    f"Time: {row['time']}<br>"
    f"Roll: {row['roll']:.2f}°<br>"
    f"Pitch: {row['pitch']:.2f}°<br>"
    f"Heading: {row['heading']:.2f}°<br>"
    f"Longitude: {row['longitude']:.6f}<br>"
    f"Latitude: {row['latitude']:.6f}<br>"
    f"Altitude: {row['altitude']:.2f} m"
    for _, row in df_reduced.iterrows()
]

# Create start and end markers
start_marker = go.Scatter3d(
    x=[df_reduced['longitude'].iloc[0]],
    y=[df_reduced['latitude'].iloc[0]],
    z=[df_reduced['altitude'].iloc[0]],
    mode='markers+text',
    marker=dict(size=8, color='green'),
    text=["Start"],
    textposition="top center",
    hoverinfo='text',
    hovertext=[hover_text[0]],
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
    hoverinfo='text',
    hovertext=[hover_text[-1]],
    name='End'
)

# Create aircraft marker (initial position)
aircraft_marker = go.Scatter3d(
    x=[df_reduced['longitude'].iloc[0]],
    y=[df_reduced['latitude'].iloc[0]],
    z=[df_reduced['altitude'].iloc[0]],
    mode='markers',
    marker=dict(size=10, color='orange', symbol='circle', opacity=0.8),
    hoverinfo='text',
    hovertext=[hover_text[0]],
    name='Aircraft'
)

# Create animation frames (limit 50 frames)
num_frames = min(50, len(df_reduced) - 1)
if num_frames > 0:
    frame_indices = np.linspace(1, len(df_reduced) - 1, num_frames, dtype=int)
else:
    frame_indices = [1]

frames = []
for i in frame_indices:
    frames.append(go.Frame(
        data=[
            go.Scatter3d(  # Trajectory
                x=df_reduced['longitude'][:i+1],
                y=df_reduced['latitude'][:i+1],
                z=df_reduced['altitude'][:i+1],
                mode='lines+markers',
                marker=dict(size=3, color='blue'),
                line=dict(width=3, color='blue'),
                hoverinfo='text',
                hovertext=hover_text[:i+1],
                name='Flight Path'
            ),
            go.Scatter3d(  # flight marker at current pos.
                x=[df_reduced['longitude'].iloc[i]],
                y=[df_reduced['latitude'].iloc[i]],
                z=[df_reduced['altitude'].iloc[i]],
                mode='markers',
                marker=dict(size=10, color='orange', symbol='circle', opacity=0.8),
                hoverinfo='text',
                hovertext=[hover_text[i]],
                name='Aircraft'
            )
        ],
        name=f'frame{i}'
    ))

# Base fig
fig = go.Figure(
    data=[
        start_marker,
        end_marker,
        go.Scatter3d(  # Initial traject.
            x=df_reduced['longitude'][:1],
            y=df_reduced['latitude'][:1],
            z=df_reduced['altitude'][:1],
            mode='lines+markers',
            marker=dict(size=3, color='blue'),
            line=dict(width=3, color='blue'),
            hoverinfo='text',
            hovertext=[hover_text[0]],
            name='Flight Path'
        ),
        aircraft_marker  # Initial flight marker
    ],
    layout=go.Layout(
        title="3D Flight Trajectory Animation with Hover Tooltips",
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

# Adjust axis range to fit data
fig.update_scenes(
    xaxis=dict(range=[df_reduced['longitude'].min() - 0.0001, df_reduced['longitude'].max() + 0.0001]),
    yaxis=dict(range=[df_reduced['latitude'].min() - 0.0001, df_reduced['latitude'].max() + 0.0001]),
    zaxis=dict(range=[df_reduced['altitude'].min() - 10, df_reduced['altitude'].max() + 10])
)

print("Yo Bro Wait ...Rendering plot...")
fig.show()