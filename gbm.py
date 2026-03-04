# GBM Price Process Simulation
# Author: theodorant32
# Description: Simulates Geometric Brownian Motion (GBM) price paths,
# prices a European call option via Monte Carlo simulation,
# and validates against the Black-Scholes closed-form formula.

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


# ─────────────────────────────────────────────
# 1. CORE GBM SIMULATION (single path — original)
# ─────────────────────────────────────────────

def simulate_gbm(
    S0=100.0, mu=0.05, sigma=0.2,
    T=1.0, steps=252, seed=None
):
    """Simulate a single GBM price path."""
    if seed is not None:
        np.random.seed(seed)
    dt = T / steps
    Z = np.random.normal(0, 1, steps)
    drift = (mu - 0.5 * sigma**2) * dt
    diffusion = sigma * np.sqrt(dt) * Z
    log_returns = drift + diffusion
    log_price = np.cumsum(log_returns)
    prices = S0 * np.exp(log_price)
    return prices


# ─────────────────────────────────────────────
# 2. MONTE CARLO — many paths
# ─────────────────────────────────────────────

def simulate_gbm_paths(
    S0=100.0, mu=0.05, sigma=0.2,
    T=1.0, steps=252, n_paths=1000, seed=None
):
    """
    Simulate N independent GBM paths.
    Returns a (steps, n_paths) array — each column is one path.
    """
    if seed is not None:
        np.random.seed(seed)
    dt = T / steps
    Z = np.random.normal(0, 1, (steps, n_paths))
    drift = (mu - 0.5 * sigma**2) * dt
    diffusion = sigma * np.sqrt(dt) * Z
    log_returns = drift + diffusion
    log_price = np.cumsum(log_returns, axis=0)
    prices = S0 * np.exp(log_price)
    return prices


def monte_carlo_call_price(
    S0=100.0, K=105.0, r=0.05, sigma=0.2,
    T=1.0, steps=252, n_paths=10000, seed=None
):
    """
    Price a European call option via Monte Carlo.

    A call option pays max(S_T - K, 0) at expiry.
    We simulate many final prices, average the payoffs,
    then discount back to today using e^(-rT).
    """
    paths = simulate_gbm_paths(
        S0=S0, mu=r, sigma=sigma, T=T,
        steps=steps, n_paths=n_paths, seed=seed
    )
    S_T = paths[-1, :]                      # Final price of each path
    payoffs = np.maximum(S_T - K, 0)        # Call payoff: max(S_T - K, 0)
    price = np.exp(-r * T) * np.mean(payoffs)  # Discount to present value
    return price


# ─────────────────────────────────────────────
# 3. BLACK-SCHOLES — closed-form exact price
# ─────────────────────────────────────────────

def black_scholes_call_price(
    S0=100.0, K=105.0, r=0.05, sigma=0.2, T=1.0
):
    """
    Price a European call option using the Black-Scholes formula.

        C = S0 * N(d1) - K * e^(-rT) * N(d2)

    where:
        d1 = [ ln(S0/K) + (r + sigma^2/2)*T ] / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)

    N(.) is the cumulative standard normal distribution.
    """
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price


# ─────────────────────────────────────────────
# 4. CONVERGENCE — watch MC approach BS
# ─────────────────────────────────────────────

def mc_convergence(
    S0=100.0, K=105.0, r=0.05, sigma=0.2,
    T=1.0, steps=252, max_paths=10000, seed=42
):
    """
    Compute MC call price at increasing path counts.
    Returns (path_counts, mc_prices) for plotting convergence.
    """
    path_counts = np.unique(
        np.logspace(1, np.log10(max_paths), 50).astype(int)
    )
    mc_prices = [
        monte_carlo_call_price(
            S0=S0, K=K, r=r, sigma=sigma, T=T,
            steps=steps, n_paths=int(n), seed=seed
        )
        for n in path_counts
    ]
    return path_counts, mc_prices


# ─────────────────────────────────────────────
# 5. MAIN — run everything and plot
# ─────────────────────────────────────────────

def main():
    S0    = 100.0   # Current stock price
    K     = 105.0   # Strike price
    r     = 0.05    # Risk-free rate
    sigma = 0.2     # Volatility
    T     = 1.0     # Time to expiry (years)
    steps = 252     # Trading days
    n_display_paths = 200  # Paths to draw in fan chart

    # ── Prices ──────────────────────────────────────
    bs_price = black_scholes_call_price(S0, K, r, sigma, T)
    mc_price  = monte_carlo_call_price(S0, K, r, sigma, T,
                                       steps=steps, n_paths=10000, seed=42)

    print("=" * 40)
    print(f"  Black-Scholes Call Price : ${bs_price:.4f}")
    print(f"  Monte Carlo Call Price   : ${mc_price:.4f}")
    print(f"  Difference               : ${abs(bs_price - mc_price):.4f}")
    print("=" * 40)

    # ── Simulate paths for fan chart ────────────────
    paths = simulate_gbm_paths(
        S0=S0, mu=r, sigma=sigma, T=T,
        steps=steps, n_paths=n_display_paths, seed=42
    )
    path_counts, mc_prices = mc_convergence(
        S0=S0, K=K, r=r, sigma=sigma, T=T, steps=steps
    )

    # ── Plot ────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("GBM Monte Carlo vs Black-Scholes", fontsize=14, fontweight="bold")

    # Left: fan of simulated paths
    ax1 = axes[0]
    for i in range(n_display_paths):
        ax1.plot(paths[:, i], alpha=0.08, linewidth=0.7, color="steelblue")
    ax1.axhline(K, color="tomato", linewidth=1.5,
                linestyle="--", label=f"Strike K={K}")
    ax1.set_title(f"{n_display_paths} Simulated GBM Paths")
    ax1.set_xlabel("Trading Day")
    ax1.set_ylabel("Price")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Right: convergence of MC toward BS
    ax2 = axes[1]
    ax2.plot(path_counts, mc_prices, color="steelblue",
             linewidth=2, label="MC Price")
    ax2.axhline(bs_price, color="tomato", linewidth=1.5,
                linestyle="--", label=f"BS Price ${bs_price:.3f}")
    ax2.set_xscale("log")
    ax2.set_title("MC Convergence to Black-Scholes")
    ax2.set_xlabel("Number of Paths (log scale)")
    ax2.set_ylabel("Estimated Call Price ($)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()