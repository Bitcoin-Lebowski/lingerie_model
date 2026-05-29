# The Unified Bitcoin Price Model

By Bitcoin Lebowski

A long-horizon valuation model for Bitcoin that fuses the strongest parts of the existing models into one coherent structure, grounded in a power law of network growth, a damped halving cycle, and a supply and demand mechanism anchored to on-chain cost basis. Every parameter is fitted to 5,789 daily observations from 2010 to 2026, and the calibration is fully reproducible from open data.

Open index.html in any browser to use the interactive chart, or host it for free with GitHub Pages. Run calibrate.py to reproduce every number from source.

This is a thinking and positioning map, not a forecast, and nothing here is investment advice. See the disclaimer at the end.

## Why another model

Every popular Bitcoin model captures one true thing and then overreaches by treating it as the whole story.

Stock-to-flow captured scarcity but ignored demand entirely, which is why it implies an infinite price as issuance falls to zero, and why it failed out of sample after 2021. The power-law-in-time models captured the long arc but offered no mechanism for cycles and no account of how the model could be wrong. Metcalfe-style models captured the demand side but said nothing about supply. Diminishing-returns observations and rainbow charts are descriptions rather than models.

The resolution is to stop treating these as rivals. They describe different layers of one system: a secular trend, a cyclical oscillation around that trend, and a market-clearing mechanism that generates both. The Unified Bitcoin Price Model is that decomposition, written so each layer is testable and so the layers explain one another.

## The model in one equation

Working in base-ten logarithms, with t measured in days since the genesis block on 3 January 2009:

```
log10 P(t)  =  C(t)            power-law trend
            +  D(t)            damped halving cycle
            +  e(t)            residual, where supply meets demand

bounded below by   floor(t)   = 0.45 * 10^C(t)
bounded above by   ceiling(t) = (1 + e^(p + q*t)) * 10^C(t)
```

with the fitted forms

```
C(t) = a + b*log10(t)                                  a = -16.4565,  b = 5.6738
D(t) = A0 * e^(-lam*t/365.25) * sin(2*pi*(t - phi)/T)  A0 = 0.618, lam = 0.079/yr,
                                                       T = 1343 d (3.68 yr), phi = 1571 d
ceiling multiple: p = 4.3751,  q = -0.000929
```

The rest of this document explains where each piece comes from and why they belong together.

## Layer one: the trend is a power law in time

Plotted on log-log axes, Bitcoin's price has traced a near-straight line for fifteen years, which is the visual signature of a power law, P proportional to t to the power b. Fitting the full daily series gives an exponent of 5.67 with an R-squared of 0.962 and a residual standard deviation of 0.30 in log space, so one standard deviation around the trend is a factor of two either way.

This is not arbitrary curve fitting. The power law follows from composing two relationships. Adoption, measured by active users or addresses, has grown as a power law of time, which is what you see in many networks and technologies during their growth phase. Network value scales with adoption in a Metcalfe-like way, value rising faster than users. A composition of power laws is itself a power law, and the exponent near 5.7 is the product of those growth rates. The mining difficulty adjustment supplies the feedback that keeps the system self-regulating: a higher price attracts hash rate, which raises security, which supports adoption, which supports price, while difficulty re-targets to keep block production steady through it all.

Two consequences matter. First, diminishing returns are built in for free. A fixed exponent is a fixed slope on log-log axes, but in calendar terms a given period buys an ever-smaller fractional increase in t as t grows, so the multiple delivered per cycle shrinks automatically with no extra assumption. The fair-value doubling time is roughly 2.2 years now and lengthens to around 3.4 years by the mid-2030s. Second, the trend defines a fair value. At present it sits near 132,000 US dollars, against a spot price around 73,500, so the model reads Bitcoin as trading at roughly half its trend value, low in the band, which is where a post-peak correction belongs after the all-time high of 126,198 on 6 October 2025.

## Layer two: the cycle is a damped halving oscillation

Every four years the block subsidy halves, imposing a supply rhythm that has driven the boom and bust cycles. The right way to model a rhythm of decreasing intensity is a damped sinusoid, so the model takes the residuals from the trend and fits an oscillation whose amplitude decays exponentially.

The fit returns an amplitude of 0.62 in log space, a decay of 7.9 percent a year, and a period of 1,343 days. That period is 3.68 years, not the four years of folklore, and it is phase-locked to the halvings with the peak landing roughly eighteen months after each one. The decay is the important part. The half-amplitude of the cycle falls across successive tops, 0.31 then 0.23 then 0.16 then 0.12 in log terms, so the swing keeps narrowing. Halvings still matter, but their power to move price is fading. The interactive chart draws this fitted oscillation forward from the present, which places the next cyclical peak around late 2028 or early 2029, exactly where a halving in 2028 plus the historical lag would put it.

A damped sinusoid is a smooth curve and a real top is a spike, so the fitted cycle deliberately undershoots the sharpest peaks and undershoots the deepest troughs. It captures the rhythm and the decay, not the exact height of each blow-off. The rails in layer three handle the extremes.

## Layer three: cost basis sets the floor and the ceiling

This is where the model departs from its predecessors and where the supply and demand story becomes quantitative. The key on-chain measure is realised price, the supply-weighted average price at which all coins last moved, which is the network's aggregate cost basis. MVRV is the market price divided by that cost basis, in other words how far above or below aggregate cost the market is trading.

The ceiling. Measured at the four mature cycle tops, MVRV reads 5.06, then 4.25, then 2.72, then 2.29. It falls every cycle. The market tops out at a steadily smaller premium to what holders actually paid, because the pool of price-elastic supply keeps growing. Early on the existing stock was tiny and held by ideologically committed owners, so a surge of demand met almost no selling and price overshot the trend more than tenfold. Today the float is enormous, deeply intermediated by exchange-traded funds and derivatives, and increasingly elastic, so the same surge is absorbed by holders taking profit and the overshoot shrinks toward nothing. Expressed against the trend, the peaks have compressed from 11.1 times fair value, to 6.3, to 2.7, to 1.17. The fitted ceiling multiple decays toward one, which means future peaks merge into the trend line. By the next cycle the cycle high is only a few per cent above fair value, and by the mid-2030s it is indistinguishable from it.

The floor. At the cycle bottoms MVRV reads 0.56, then 0.69, then 0.78, in other words price falling to somewhat below aggregate cost basis, and that level is rising toward one over time. When the average holder is underwater, selling exhausts itself through capitulation and price reverts. So the lower rail is not an arbitrary fraction of the trend. It is the price at which the network sits at its aggregate cost basis, which today is about 54,000 US dollars and corresponds to roughly 0.45 times the trend. The chart draws realised price as a separate line so you can see the floor mechanism directly. Because the floor multiple of trend has held in the 0.43 to 0.57 range across every cycle, while the ceiling multiple is collapsing, the band is asymmetric and narrows from above. That narrowing is the diminishing-returns and volatility-maturation signature, measured rather than asserted.

## The engine that unifies the layers

The three layers are not independent decorations. They are produced by a single market-clearing condition. At any moment the price settles where the flow of demand equals the flow of available supply:

```
Demand(t, P)  =  new issuance(t)  +  elastic holder supply(P, t)
```

New issuance is the inelastic, shrinking flow. After the 2024 halving it runs at about 450 BTC per day, roughly 164,000 a year, and it halves again around 2028. Elastic holder supply is the price-sensitive mobilisation of the existing 19.8 million coins. As price rises relative to cost basis, dormant coins and corporate treasuries cross their reservation price and become sellers. This is the negative feedback that caps blow-off tops, and it is the mechanism behind the declining top-MVRV in layer three. The same forces set the trend, because adoption-driven demand is what pulls the centre line upward through time.

The recent data shows both sides at once. On demand, exchange-traded funds have at times absorbed several times the new issuance, with 2025 net inflows around 47 billion dollars and projections that demand could run several times supply through 2026. On the elastic-supply side, the largest corporate holder sits close to its average cost of about 75,500 dollars with its founder publicly floating a first treasury trim, and listed miners sold more Bitcoin in the first quarter of 2026 than in all of the prior year. A demand deficit pushing price up, met by holders who turn into sellers as price rises. That is the equilibrium, and it is why the model cannot run away to infinity the way a pure scarcity model does.

## The gold parallel and the long-run ceiling

Gold is the precedent for a monetary premium accruing along an S-curve and then maturing into low volatility once the float is deep and widely held. Bitcoin is compressing that process from centuries into a couple of decades. The power-law trend is the curbed S-curve of monetisation, and the collapsing cycle amplitude is the same volatility maturation that gold underwent after its own repricing decades ago.

Gold's monetary stock, worth somewhere in the region of 22 to 28 trillion dollars, is a natural anchor for Bitcoin's long-run ceiling. Parity with gold implies a price around 1.1 to 1.3 million dollars per coin, and the trend line crosses one million in the mid-2030s, so the two methods agree to within a cycle. That convergence is a useful sanity rail rather than a promise.

## Targets

For each year the model produces a floor, a fair value, and a cycle high. Rounded:

| Year | Floor (capitulation) | Fair value (trend) | Cycle high (ceiling) |
|------|----------------------|--------------------|----------------------|
| 2026 | 72,000 | 160,000 | 188,000 |
| 2027 | 98,000 | 217,000 | 245,000 |
| 2028 | 131,000 | 291,000 | 317,000 |
| 2029 | 173,000 | 384,000 | 408,000 |
| 2030 | 225,000 | 500,000 | 522,000 |
| 2032 | 368,000 | 819,000 | 838,000 |
| 2035 | 719,000 | 1,600,000 | 1,610,000 |

Read these as rails for thinking about risk and positioning, not as point predictions. The floor is the dependable line, because price has spent almost no sustained time below aggregate cost basis and that level only rises. The cycle high is the speculative line, and the fact that it has all but merged with fair value by the mid-2030s is the model telling you the four-year boom and bust is fading into a trend-following store of value.

## Calibration and reproducibility

The interactive model is calibrated on the Coin Metrics community dataset, which publishes daily price, market capitalisation, MVRV and supply back to 2010 under an open licence. The script calibrate.py downloads that file, fits all three layers, prints every constant used in index.html, and reports the MVRV reading at each cycle top and bottom.

```
pip install pandas numpy scipy
python calibrate.py
```

The headline fit is log10 P = -16.4565 + 5.6738 * log10(day), R-squared 0.962. Adjust the source window or the slope in the script to test sensitivity. The interactive chart also exposes the exponent, the intercept, the floor multiple, and a future trend haircut, so you can stress the model by hand.

## Limitations and honest caveats

The single largest risk is that adoption is a flattening S-curve rather than an endless power law. If it is, the forward trend is too steep and every fair-value figure above is too high. The trend-haircut control in the chart exists precisely to model that case, and in practice the floor is the line to lean on, not the ceiling. The exponent is also specification-dependent, sitting in the 5.5 to 5.8 range depending on the fitting window and data source, and alternative functional forms such as a stack of sigmoids can fit the same history.

The damped cycle explains about 62 per cent of the variance of the trend residuals, which is good for something this noisy but far from complete, and as noted it smooths over the spikiness of real tops and bottoms. Finally, the elastic-supply curve is grounded in its consequence, the declining top-MVRV, rather than estimated as a structural function. Making it fully mechanistic would require the cost-basis distribution by coin age, which is paywalled on-chain data rather than part of the free dataset used here.

## Disclaimer

This project is for research and educational purposes. It is a model of historical structure extrapolated forward, not a prediction, and not financial, investment, legal or tax advice. Bitcoin is volatile and you can lose your entire investment. Do your own research and consult a regulated professional before making any decision.

## Acknowledgements and references

Power-law-in-time framing: Giovanni Santostasi, The Bitcoin Power Law Theory, https://giovannisantostasi.medium.com/the-bitcoin-power-law-theory-962dfaf99ee9

Open data: Coin Metrics community data, https://github.com/coinmetrics/data

Critical perspective on power-law specification: see recent work testing shift-sensitivity and alternative forms, https://arxiv.org/abs/2605.21316

## Licence

MIT. See LICENSE.
