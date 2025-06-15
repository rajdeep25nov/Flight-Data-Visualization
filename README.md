# 3D Flight Trajectory Animation

A Python-based data visualization project that creates an interactive 3D animation of flight navigation data, showcasing a flight's trajectory with a moving aircraft marker and hover tooltips. Developed as a data analyst project to process large datasets (\~380,744 rows) and produce professional visualizations and documentation.

## Table of Contents

* Project Overview
* Features
* Installation
* Usage
* Sample Output
* Dependencies
* Troubleshooting
* Related Artifacts
* Credits
* Contact

## Project Overview

This project visualizes flight navigation data from an Excel file (`2023-07-04-09-36-14-5325-NAVIGATION.xlsx`) in a 3D interactive plot using Python, Pandas, and Plotly. The script processes a large dataset (\~380,744 rows) containing flight parameters like time, roll, pitch, heading, longitude, latitude, and altitude, creating an animated trajectory with a moving aircraft marker. Hover tooltips display detailed flight data, and robust error handling ensures reliability. A professional LaTeX report documents the code and addresses technical FAQs, making this project a strong portfolio piece for data analyst roles.

**Objectives:**

* Transform raw flight data into an interactive 3D visualization.
* Optimize performance for large datasets through data reduction.
* Implement robust error handling for diverse data formats.
* Produce professional documentation for stakeholders and interviews.

## Features

* **Interactive 3D Visualization**: Renders flight trajectory in 3D using Plotly, with start (green) and end (red) markers.
* **Animated Aircraft Marker**: An orange marker moves along the trajectory, enhancing visual appeal.
* **Hover Tooltips**: Displays time, roll, pitch, heading, longitude, latitude, and altitude when hovering over points.
* **Data Reduction**: Reduces \~380,744 rows to 10–100 points for smooth performance.
* **Robust Error Handling**: Handles missing files, invalid time formats, and small datasets with debugging output.
* **Time Parsing Flexibility**: Supports multiple time formats (e.g., `HH:MM:SS.ssssss`, `YYYY-MM-DD HH:MM:SS`).
* **Professional Documentation**: Includes a LaTeX report (`Flight_Trajectory_Report.pdf`) with code explanations and FAQs.
* **Version Control**: Managed with Git for reproducibility.

## Installation

To run this project locally, follow these steps:

### Clone the Repository:

```bash
git clone https://github.com/yourusername/repo_name.git
cd flight-trajectory
```

### Set Up a Python Environment (recommended: Python 3.8+):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies:

```bash
pip install pandas matplotlib openpyxl plotly numpy
```

### Download Sample Data (optional):

The script expects an Excel file (`2023-07-04-09-36-14-5325-NAVIGATION.xlsx`) in the project directory. If you don’t have the file, contact the repository owner or modify the script’s file path to use your own navigation data.

## Usage

### Prepare the Data:

Place the Excel file in the project root or update the file path in `flight_trajectory_with_tooltips.py` (line \~10).

**Expected columns:**

* `TIME`
* `ROLL(DEG)`
* `PITCH(DEG)`
* `TRUE HEADING(DEG)`
* `LONGITUDE`
* `LATTITUDE`
* `ALTITUDE(METERS)`



### Interact with the Visualization:

* A browser window will open displaying the 3D plot.
* Use the Play/Pause buttons to control the animation.
* Hover over points to view tooltips with flight details.
* Rotate, zoom, or pan the plot using mouse controls.

### Example Code Snippet (from `flight_trajectory_with_tooltips.py`):

```python
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Load data
df = pd.read_excel("2023-07-04-09-36-14-5325-NAVIGATION.xlsx")
# ... (data cleaning, visualization setup, and animation logic)
fig.show()
```

## Sample Output

The script generates an interactive 3D plot with:

* A blue trajectory line showing the flight path.
* Green start and red end markers with labels.
* An orange aircraft marker moving along the trajectory.
* Hover tooltips displaying:

  * Time: `2023-07-04 07:21:15.359574`
  * Roll: `-0.42°`
  * Pitch: `2.15°`
  * Heading: `121.58°`
  * Longitude: `77.666298`
  * Latitude: `12.953511`
  * Altitude: `811.99 m`


## Dependencies

* Python: 3.8 or higher
* Pandas: `pip install pandas`
* Plotly: `pip install plotly`
* NumPy: `pip install numpy`
* OpenPyXL: `pip install openpyxl`
* Matplotlib (if needed): `pip install matplotlib`

## Troubleshooting

### Error: "File not found"

* Ensure the Excel file is in the project directory or update the file path in the script.

```python
df = pd.read_excel("path/to/your/file.xlsx")
```

### Error: "Not enough data points after reduction"

* Check if the Excel file has sufficient valid rows (at least 2).
* Inspect the `TIME` column format and update `time_formats` in the script if needed (e.g., add `%H:%M:%S,%f`).

### Slow Animation

* Reduce `target_points` in the script (e.g., from 100 to 50).

```python
target_points = min(max(10, len(df) // 200), 50)
```

### Time Parsing Issues

* Run the script and check console output for sample time values.
* Add correct format to `time_formats` if values don’t match existing formats.

### Plot Not Displaying

* Ensure Plotly is installed: `pip install plotly`
* Try running in a different browser or environment (e.g., Jupyter Notebook).

For further issues, open a GitHub issue or contact the repository owner.

## Related Artifacts



## Credits

* **Developer**: Rajdeep Jaiswal

* **Data Source**: Proprietary flight navigation data.

## Contact

* GitHub: [github.com/rajdeep25nov](https://github.com/rajdeep25nov)
* LinkedIn: [linkedin.com/in/rajdeepjaiswal25nov](https://linkedin.com/in/rajdeepjaiswal25nov)
* Email: [rajdeep25nov@gmail.com](mailto:rajdeep25nov@gmail.com)

Feel free to open an issue or contact me for questions, feedback, or collaboration opportunities!
