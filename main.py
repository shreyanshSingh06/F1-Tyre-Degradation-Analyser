import os
import logging
import fastf1
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

logging.getLogger('fastf1').setLevel(logging.WARNING)
os.makedirs('cache', exist_ok=True)
fastf1.Cache.enable_cache('cache')

while True:
    print("Welcome to F1 Stint Lap Time Analysis")
    year = 0
    while year < 2021 or year > 2026:
        try:
            year = int(input("Which year (2021 or on) do you want to analyse? "))
        except ValueError:
            continue

    schedule = fastf1.get_event_schedule(year)
    races = schedule[schedule['EventFormat'] != 'testing']

    print(races[['RoundNumber', 'EventName', 'Location']].to_string(index=False))

    gp = 0
    while gp not in races['RoundNumber'].values:
        try:
            gp = int(input(f"Enter round number (1-{len(races)}): " if gp == 0 else f"Invalid. Enter round number (1-{len(races)}): "))
        except ValueError:
            continue

    print("Loading session data...")
    session = fastf1.get_session(year, gp, 'R')
    session.load()

    drivers = session.drivers
    abb = []
    driver_info = [session.get_driver(d) for d in drivers]
    for info in driver_info:
        print(info['Abbreviation'], '-', info['FullName'])

    abb = [info['Abbreviation'] for info in driver_info]

    while True:
        driver = ""
        while driver not in abb:
            driver = input("Enter the driver abbreviation whose data you want to analyse: ").upper()

        laps = session.laps.pick_drivers(driver).pick_quicklaps().copy()

        if not laps.empty:
            break

        print(f"\nNo lap data available for {driver} (may have retired early).")
        con = ""
        while con not in ['y', 'n', 'yes', 'no']:
            con = input("Try another driver? ").lower()
        if con in ['n', 'no']:
            break

    if laps.empty:
        continue

    stint_summary = laps.groupby(['Stint', 'Compound'])['LapNumber'].count()
    print(f"\nAvailable stints:")
    print(stint_summary.to_string())

    available_stints = laps['Stint'].unique().tolist()

    chosen = None
    while chosen not in available_stints:
        try:
            chosen = float(input("Which stint do you want to analyse? "))
        except ValueError:
            continue
        if chosen not in available_stints:
            print(f"Invalid. Available stints: {[int(s) for s in available_stints]}")

    stint = laps[laps['Stint'] == chosen].copy()
    compound = stint['Compound'].iloc[0]
    stint['TyreAge'] = range(1, len(stint) + 1)
    stint['LapSeconds'] = stint['LapTime'].dt.total_seconds()

    A = np.column_stack([
        np.ones(len(stint)),
        stint['TyreAge'].values
    ])
    b_vec = stint['LapSeconds'].values

    ATA = A.T @ A
    ATb = A.T @ b_vec
    x = np.linalg.solve(ATA, ATb)
    a_intercept, slope = x

    mins = int(a_intercept // 60)
    secs = a_intercept % 60
    print(f"\nCompound: {compound}")
    print(f"Base lap time: {mins}:{secs:06.3f}")
    print(f"Degradation rate: {slope:.3f}s per lap")

    event_name = races[races['RoundNumber'] == gp]['EventName'].values[0]

    tyre_ages = stint['TyreAge'].values
    fitted = a_intercept + slope * tyre_ages

    def fmt_laptime(x, _):
        m = int(x // 60)
        s = x % 60
        return f"{m}:{s:05.2f}"

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(tyre_ages, b_vec, label='Actual lap times', color='steelblue')
    ax.plot(tyre_ages, fitted, label='Least squares fit', color='red', linewidth=2)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(fmt_laptime))
    ax.set_xlabel('Tyre Age (laps)')
    ax.set_ylabel('Lap Time (min:sec)')
    ax.set_title(f'Tyre Degradation — {driver}, {event_name} {year}')
    ax.legend()
    fig.tight_layout()
    filename = f"{driver}_{event_name.replace(' ', '_')}_{year}_stint{int(chosen)}.png"
    fig.savefig(filename, dpi=150)

    residuals = b_vec - fitted
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((b_vec - np.mean(b_vec))**2)
    r_squared = 1 - ss_res / ss_tot
    print(f"R² (goodness of fit): {r_squared:.4f}")

    print(f"Plot saved to {filename}")

    plt.show()


    con = ""
    while con not in ['y', 'n', "yes", "no"]:
        con = input("Analyze another stint? ").lower()

    if con == "n" or con == "no":
        break

print("Thank you for using F1 Stint Lap Time Analysis")