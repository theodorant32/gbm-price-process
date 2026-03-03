README.md

# Geometric Brownian Motion Price Process 

This project simulates a price path using Geometric Brownian Motion (GBM), a common stochastic model used in quantitative finance to represent asset prices. The script generates random normal increments, accumulates them into log-returns, and converts them into a simulated price path. By adjusting the volatility parameter (`sigma`), you can observe how randomness affects the behavior of the price process. 

## Installation 

Install the required Python packages using:
pip install -r requirements.txt

This installs:
- numpy — numerical computation
- matplotlib — plotting and visualization

## Running the Simulation

Run the GBM script with:
python gbm.py


A chart will appear showing the simulated price path.

## Experimenting with Volatility

To observe how volatility affects randomness, open `gbm.py` and modify the `sigma` value inside the `main()` function:
sigma = 0.2


Try values like:

- `0.1` for a smoother path  
- `0.4` for more volatility  
- `1.0` for extreme randomness  

This helps build intuition for stochastic modeling and price dynamics.