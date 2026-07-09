# F1 Tyre Degradation Analyser

A Python program that analyses Formula One tyre degradation by fitting a linear model to real race data. It retrieves live timing data using the FastF1 library and uses least squares approximation to estimate how much slower a car gets per lap as its tyres wear.

## Features

- Pulls real lap-by-lap timing data for any F1 race from 2021 onwards using the FastF1 library
- Automatically filters out outlier laps caused by yellow flags, pit lane traffic, or other anomalies
- Fits a linear model to the selected stint and calculates the degradation rate in seconds per lap
- Outputs the base lap time, degradation rate, and R² value
- Generates and saves a plot of the actual lap times alongside the fitted line as a PNG file

## Tech Stack

- **Python**
- **NumPy** — matrix construction and solving the normal equations
- **FastF1** — F1 timing data retrieval
- **Matplotlib** — visualisation

## Getting Started

### Prerequisites

- Python 3.8 or later

### Installation

1. Clone the repository:

```bash
git clone https://github.com/shreyanshSingh06/F1-Tyre-Degradation-Analyser.git
cd F1-Tyre-Degradation-Analyser
```

2. Install the required libraries:

```bash
pip install fastf1 numpy matplotlib
```

### Running the program

```bash
python main.py
```

The program will prompt you for inputs step by step:

1. **Year** — the season to analyse (2021 or later)
2. **Round number** — a list of races for that season is printed; enter the round number of the race you want
3. **Driver abbreviation** — a list of drivers in that race is printed with their three-letter codes (e.g. `HAM`, `VER`, `NOR`); enter one of these exactly
4. **Stint number** — the driver's stints are listed with lap counts and tyre compounds; enter the stint number to analyse

After the results are shown, enter `y` to analyse another stint or `n` to exit.

## Output

The program prints the base lap time, degradation rate, and R² value to the terminal. A plot is also generated and saved automatically to the project folder as a PNG, with the filename including the driver, race, year, and stint number — for example, `HAM_Belgian_Grand_Prix_2025_stint2.png`.

## Notes

- The first time a race is loaded, data is downloaded from the F1 timing servers which can take 30–60 seconds. A `cache` folder is created automatically to store this — subsequent runs on the same race are near-instant.
- `WARNING` and `INFO` messages may appear during loading. These come from the FastF1 library and can be ignored.
- Data is available from the 2021 season onwards.
