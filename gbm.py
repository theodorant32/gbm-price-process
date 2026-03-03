import numpy as np
import matplotlib.pyplot as plt

def simulate_gbm(
    S0=100.0,
    mu=0.05,
    sigma=0.2,
    T=1.0,
    steps=252,
    seed=None
):
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

def main():
    S0 = 100
    mu = 0.05
    sigma = 0.2
    T = 1.0
    steps = 252

    prices = simulate_gbm(S0=S0, mu=mu, sigma=sigma, T=T, steps=steps, seed=42)

    plt.figure(figsize=(10, 5))
    plt.plot(prices)
    plt.title(f"GBM Price Path (sigma={sigma})")
    plt.xlabel("Step")
    plt.ylabel("Price")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
