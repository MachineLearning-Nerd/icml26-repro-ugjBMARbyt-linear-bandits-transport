"""Clean-room EntUCB (linear-UCB with Fourier features) from
"Linear Bandits beyond Inner Product Spaces" (arXiv 2502.07397). numpy, CPU.

EntUCB reduces bandit OT to linear bandit via Fourier isometry (c1). In finite-dim setting (c4),
this is standard linear-UCB on N basis coefficients with regret Õ(√(NT)).
"""
from __future__ import annotations
import numpy as np


def fourier_features(X, N, seed=0):
    """Random Fourier features: φ(x) = [cos(w_i·x + b_i)] for random w_i, b_i."""
    rng = np.random.default_rng(seed)
    d = X.shape[1]
    W = rng.standard_normal((N, d)) * 1.0
    b = rng.uniform(0, 2 * np.pi, N)
    return np.cos(X @ W.T + b) * np.sqrt(2.0 / N)


def entucb(Phi, theta_star, T, lam=1.0, beta_scale=1.0, seed=0):
    """Linear-UCB (EntUCB) on N-dim features Phi (K arms x N features).
    Returns cumulative regret trajectory."""
    rng = np.random.default_rng(seed)
    K, N = Phi.shape
    V = lam * np.eye(N)
    theta_hat = np.zeros(N)
    b_vec = np.zeros(N)
    regret = 0.0; regrets = []
    best_arm = int(np.argmax(Phi @ theta_star))
    for t in range(T):
        # UCB scores
        Vinv = np.linalg.inv(V)
        ucb = Phi @ theta_hat + beta_scale * np.sqrt(np.maximum(np.sum((Phi @ Vinv) * Phi, axis=1), 0))
        a = int(np.argmax(ucb))
        # observe reward
        reward = float(Phi[a] @ theta_star + rng.standard_normal() * 0.1)
        # update
        V += np.outer(Phi[a], Phi[a])
        b_vec += Phi[a] * reward
        theta_hat = np.linalg.solve(V, b_vec)
        # regret
        regret += float(Phi[best_arm] @ theta_star - Phi[a] @ theta_star)
        regrets.append(regret)
    return regrets


def random_problem(K, N, d, seed=0):
    """Random bandit: K arms with d-dim contexts, N Fourier features."""
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((K, d))
    Phi = fourier_features(X, N, seed=seed)
    theta = rng.standard_normal(N); theta /= np.linalg.norm(theta)
    return Phi, theta
