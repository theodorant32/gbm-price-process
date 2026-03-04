# Geometric Brownian Motion — Monte Carlo Options Pricer

This project is concerned with simulating asset prices through the geometric Brownian motion (GBM). It makes use of Monte Carlo simulation to estimate the value of a European call option. After that, it checks the result against the exact Black, Scholes formula. It shows that the estimation from the Monte Carlo simulation approaches the analytical price when the number of paths is increased.

## What's in here

- **GBM simulation** — models a stock price path using log-normal returns with drift and volatility
- **Monte Carlo pricing** — simulates thousands of independent paths, computes the average discounted payoff of a call option
- **Black-Scholes pricing** — calculates the exact theoretical option price using the closed-form BS formula
- **Convergence analysis** — plots how the MC estimate homes in on the BS price as path count increases

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

This installs:
- `numpy` — numerical computation and random sampling
- `matplotlib` — plotting and visualization
- `scipy` — cumulative normal distribution for Black-Scholes

## Running the Simulation

```bash
python gbm.py
```

<<<<<<< HEAD
This will:
1. Print the Black-Scholes and Monte Carlo call prices side by side
2. Display a fan chart of 200 simulated price paths with the strike price overlaid
3. Display a convergence chart showing the MC price stabilizing toward the BS price

Example output:
```
========================================
  Black-Scholes Call Price : $8.0214
  Monte Carlo Call Price   : $7.9196
  Difference               : $0.1017
========================================
```
=======
A chart will appear showing the simulated price path.
>>>>>>> 7df2eb9ab0f908c988c5a6505c9de72212e335ba

## The Core Idea

A European call option gives the holder the right to buy a stock at a fixed **strike price K** at expiry. Its value today is the expected payoff discounted to present value:

```
Payoff = max(S_T - K, 0)
```

**Monte Carlo approach** — simulate many possible future prices `S_T`, average the payoffs, discount back:
```
C ≈ e^(-rT) * mean( max(S_T - K, 0) )
```

**Black-Scholes approach** — derive the same expectation analytically:
```
C = S0 * N(d1) - K * e^(-rT) * N(d2)

<<<<<<< HEAD
d1 = [ ln(S0/K) + (r + σ²/2)*T ] / (σ*√T)
d2 = d1 - σ*√T
```

Where `N(·)` is the cumulative standard normal distribution. Both methods price the same thing — BS is the exact shortcut, MC is the general-purpose simulation. They should agree.

## Experimenting with Parameters

Open `gbm.py` and adjust the parameters in `main()`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `S0` | 100 | Current stock price |
| `K` | 105 | Strike price |
| `r` | 0.05 | Risk-free rate |
| `sigma` | 0.2 | Volatility |
| `T` | 1.0 | Time to expiry (years) |

You can try increasing `sigma` to `0.4` or setting `K` below `S0` (in-the-money) to see how it affects the option price and path fan
=======
This helps build intuition for stochastic modeling and price dynamics.
>>>>>>> 7df2eb9ab0f908c988c5a6505c9de72212e335ba
