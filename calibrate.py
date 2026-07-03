"""
calibrate.py  -  The Lingerie Model
Reproduces every constant used in index.html from open data.

Data source: Coin Metrics community data (open, attribution requested)
  https://raw.githubusercontent.com/coinmetrics/data/master/csv/btc.csv

Usage:
  pip install pandas numpy scipy
  python calibrate.py

It prints the fitted parameters for the three layers (trend, cycle, rails)
and the cost-basis (MVRV) readings at every cycle top and bottom.
"""
import io, urllib.request
import numpy as np, pandas as pd
from scipy.optimize import curve_fit

CSV = "https://raw.githubusercontent.com/coinmetrics/data/master/csv/btc.csv"
GENESIS = pd.Timestamp("2009-01-03")

def load():
    raw = urllib.request.urlopen(CSV, timeout=60).read()
    df = pd.read_csv(io.BytesIO(raw),
                     usecols=["time", "PriceUSD", "CapMrktCurUSD", "CapMVRVCur", "SplyCur"],
                     parse_dates=["time"])
    df = df[(df.PriceUSD > 0)].dropna(subset=["PriceUSD"]).copy()
    df["day"] = (df.time - GENESIS).dt.days
    df = df[df.day > 0]
    df["rp"] = df.CapMrktCurUSD / df.CapMVRVCur / df.SplyCur   # realised price = aggregate cost basis
    return df

def main():
    df = load()
    X, Y = np.log10(df.day.values), np.log10(df.PriceUSD.values)

    # ---- Layer 1: power-law trend  log10 P = a + b*log10(day) ----
    b, a = np.polyfit(X, Y, 1)
    resid = Y - (a + b * X)
    R2 = 1 - np.sum(resid ** 2) / np.sum((Y - Y.mean()) ** 2)
    df["centre"] = 10 ** (a + b * np.log10(df.day))
    print("LAYER 1  power-law trend")
    print(f"  log10 P = {a:.4f} + {b:.4f} * log10(day since genesis)")
    print(f"  R^2 = {R2:.4f}   residual sd = {resid.std():.3f} (1 sigma = x{10**resid.std():.2f})")

    # ---- Layer 2: damped halving cycle on the residuals ----
    sub = df[df.time >= "2012-01-01"]
    t, r = sub.day.values.astype(float), (np.log10(sub.PriceUSD) - np.log10(sub.centre)).values
    f = lambda t, A0, lam, T, phi, c: c + A0 * np.exp(-lam * t / 365.25) * np.sin(2 * np.pi * (t - phi) / T)
    popt, _ = curve_fit(f, t, r, p0=[0.6, 0.15, 1430, 1000, 0],
                        bounds=([0.1, 0, 1200, -2000, -0.3], [1.5, 0.6, 1700, 4000, 0.3]), maxfev=40000)
    A0, lam, T, phi, c = popt
    print("\nLAYER 2  damped halving cycle (fitted on residuals)")
    print(f"  amplitude A0 = {A0:.3f}   decay = {lam:.3f}/yr   period = {T:.0f}d ({T/365.25:.2f}yr)   phase = {phi:.0f}d")

    # ---- Layer 3: cost-basis rails (MVRV at tops/bottoms) ----
    tops = {"2013": "2013-11-30", "2017": "2017-12-17", "2021": "2021-11-10", "2025": "2025-10-06"}
    bots = {"2015": "2015-01-14", "2018": "2018-12-15", "2022": "2022-11-21"}
    near = lambda d: df.loc[(df.time - pd.Timestamp(d)).abs().idxmin()]
    print("\nLAYER 3  cost-basis rails")
    print("  cycle tops  (MVRV = price / aggregate cost basis):")
    for k, v in tops.items():
        row = near(v)
        print(f"    {k}: MVRV {row.CapMVRVCur:.2f}   price/trend {row.PriceUSD/row.centre:.2f}")
    print("  cycle bottoms:")
    for k, v in bots.items():
        row = near(v)
        print(f"    {k}: MVRV {row.CapMVRVCur:.2f}   price/trend {row.PriceUSD/row.centre:.2f}")

    # declining ceiling envelope fitted to price/trend at the tops:  mult = 1 + exp(p + q*day)
    td = np.array([near(v).day for v in tops.values()])
    tm = np.array([near(v).PriceUSD / near(v).centre for v in tops.values()])
    q, p = np.polyfit(td, np.log(tm - 1), 1)
    print(f"\n  ceiling multiple = 1 + exp({p:.4f} {q:+.6f}*day)   (decays toward 1: peaks merge into trend)")
    print(f"  floor multiple ~ 0.45 x trend (price at aggregate cost basis, where capitulation exhausts supply)")

    now = df.iloc[-1]
    print(f"\nLATEST ({now.time.date()}): price ${now.PriceUSD:,.0f}  fair ${now.centre:,.0f}  "
          f"cost basis ${now.rp:,.0f}  MVRV {now.CapMVRVCur:.2f}")

if __name__ == "__main__":
    main()
