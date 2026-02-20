import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from models import CreditDecision

plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.5
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['legend.frameon'] = True
plt.rcParams['legend.facecolor'] = 'white'
plt.rcParams['legend.edgecolor'] = 'black'
plt.rcParams['legend.loc'] = 'best'


class ModelsVisualization(CreditDecision):
    """
    Visualizer for Altman Z-Score analysis with support for bar charts and spider charts.
    """

    def __init__(self, results: dict, altman_z_scores: dict = None,
                 component_ratios: dict = None, default_probabilities: dict = None):
        super().__init__(results)
        self.altman_z_scores = altman_z_scores
        self.component_ratios = component_ratios
        self.default_probabilities = default_probabilities
        self.categories = ['Liquidity', 'Profitability',
                           'Efficiency', 'Leverage', 'Turnover']

    def plot_z_score_comparison(self) -> None:
        """
        Plots bar chart comparing Altman Z-scores across years.

        Returns:
            fig: The matplotlib figure object for the Z-score comparison.
        """
        if self.altman_z_scores is None:
            raise ValueError(
                "No Z-score data provided. Initialize with altman_z_scores.")

        tickers = list(self.altman_z_scores.keys())
        z_scores_current = [self.altman_z_scores[t][0] for t in tickers]
        z_scores_old = [self.altman_z_scores[t][1] for t in tickers]

        x = np.arange(len(tickers))
        width = 0.35

        fig, ax = plt.subplots(figsize=(6, 4))

        # Threshold areas
        self._add_threshold_zones(ax)

        # Plot bars with labels
        self._plot_bars(ax, x, width, z_scores_old, z_scores_current)

        # Customize plot
        self._customize_bar_plot(ax, x, tickers)

        plt.tight_layout()
        return fig

    def plot_component_spider_charts(self) -> None:
        """
        Plots spider charts showing component ratios for each ticker.

        Returns:
            fig: The matplotlib figure object containing the spider charts.
        """
        n_tickers = len(self.component_ratios)
        n_cols = 2
        n_rows = (n_tickers + 1) // 2

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(7, 3 * n_rows),
                                 subplot_kw=dict(projection='polar'))
        axes = axes.flatten() if n_tickers > 1 else [axes]

        angles = self._get_spider_angles()

        for idx, (ticker, ratio_arrays) in enumerate(self.component_ratios.items()):
            self._plot_single_spider(axes[idx], ticker, ratio_arrays, angles)

        # Hide unused subplots
        for idx in range(n_tickers, len(axes)):
            axes[idx].axis('off')

        plt.tight_layout()
        return fig

    def plot_credit_decision_analysis(self):
        """
        Plot Z-Score vs Default Probability with credit decision boundaries.

        Returns:
            fig: The matplotlib figure object for credit decision analysis.
        """
        if self.altman_z_scores is None or self.default_probabilities is None:
            raise ValueError(
                "Both Z-scores and default probabilities required for credit decision plot.")

        # Prepare combined metrics
        combined_metrics = {
            ticker: [self.altman_z_scores[ticker][0],
                     self.default_probabilities[ticker]]
            for ticker in self.altman_z_scores.keys()
        }

        fig, ax = plt.subplots(figsize=(6, 4))

        # Get axis limits first to properly fill zones
        all_z_scores = [z_score for _, [z_score, _]
                        in combined_metrics.items()]
        all_pds = [default_prob * 100 for _,
                   [_, default_prob] in combined_metrics.items()]

        x_min = min(min(all_z_scores) * 0.9, 0)
        x_max = max(max(all_z_scores) * 1.1, 4)
        y_max = max(max(all_pds) * 1.2, 20)

        # Define decision zones with full coloring
        # APPROVAL ZONE
        ax.fill([1.8, x_max, x_max, 1.8], [0, 0, 15, 15],
                color='darkseagreen', alpha=0.2, label='Approval Zone')

        # DENIAL ZONE
        ax.fill([x_min, x_max, x_max, x_min], [15, 15, y_max, y_max],
                color='indianred', alpha=0.2, label='Denial Zone')
        ax.fill([x_min, 1.8, 1.8, x_min], [0, 0, 15, 15],
                color='indianred', alpha=0.2, label='Denial Zone')

        # Add decision boundary lines
        ax.axvline(x=3.0, color='darkseagreen',
                   linestyle='--', alpha=0.7, zorder=2)
        ax.axvline(x=1.8, color='indianred',
                   linestyle='--', alpha=0.7, zorder=2)
        ax.axhline(y=5, color='darkseagreen',
                   linestyle='--', alpha=0.7, zorder=2)
        ax.axhline(y=15, color='indianred',
                   linestyle='--', alpha=0.7, zorder=2)

        # Plot each ticker
        for ticker, [z_score, default_prob] in combined_metrics.items():
            decision = self.credit_decision(z_score, default_prob)

            # Color and marker based on decision
            if decision == "APPROVED":
                color = 'darkseagreen'
                marker = 'o'
                size = 50
            else:  # DENIED
                color = 'indianred'
                marker = 'x'
                size = 50

            ax.scatter(z_score, default_prob * 100, c=color, marker=marker, s=size,
                       linewidth=2, alpha=0.9, zorder=3)
            ax.text(z_score + 0.08, 0.5 + default_prob * 100, ticker, fontsize=6,
                    va='center', zorder=4)

        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='darkseagreen',
                   markersize=6, markeredgecolor='darkseagreen', markeredgewidth=2,
                   label='APPROVED'),
            Line2D([0], [0], marker='x', color='w', markerfacecolor='indianred',
                   markersize=6, markeredgewidth=2, label='DENIED'),
            Patch(facecolor='darkseagreen', alpha=0.25, label='Approval Zone'),
            Patch(facecolor='indianred', alpha=0.25, label='Denial Zone')
        ]

        # Add legend
        ax.legend(handles=legend_elements, loc='best',
                  fontsize=6, framealpha=0.95, edgecolor='black')

        # Labels and styling
        ax.set_xlabel('Altman Z-Score', fontsize=8)
        ax.set_ylabel('Default Probability (%)', fontsize=8)
        ax.set_title('Credit Decision Analysis: Z-Score vs Default Probability',
                     fontsize=10, fontweight='bold', pad=20)
        ax.grid(alpha=0.3, linestyle=':', linewidth=0.5, zorder=1)
        ax.tick_params(axis='x', labelsize=7)
        ax.tick_params(axis='y', labelsize=7)

        # Set axis limits
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(0, y_max)

        plt.tight_layout()
        return fig

    def _add_threshold_zones(self, ax: plt.Axes) -> None:
        """Add Z-score threshold lines and zones."""
        ax.axhline(y=3.0, color='darkseagreen', linestyle='--')
        ax.axhline(y=1.8, color='indianred', linestyle='--')

        ax.axhspan(3.0, 5.0, color='darkseagreen',
                   alpha=0.25, label='Low Bankruptcy Risk')
        ax.axhspan(0, 1.8, color='indianred', alpha=0.25,
                   label='High Bankruptcy Risk')

    def _plot_bars(self, ax: plt.Axes, x: np.ndarray, width: float,
                   z_scores_old: list[float], z_scores_current: list[float]) -> None:
        """Plot bar charts with value labels."""
        # 2024 bars
        ax.bar(x - width/2, z_scores_old, width,
               color='cornflowerblue', label='2024')
        for i, height in enumerate(z_scores_old):
            ax.text(x[i] - width/2, height - 0.15, f'{height:.2f}',
                    ha='center', va='bottom', fontsize=5, color='black')

        # 2025 bars
        ax.bar(x + width/2, z_scores_current,
               width, color='navy', label='2025')
        for i, height in enumerate(z_scores_current):
            ax.text(x[i] + width/2, height - 0.15, f'{height:.2f}',
                    ha='center', va='bottom', fontsize=5, color='white')

    def _customize_bar_plot(self, ax: plt.Axes, x: np.ndarray, tickers: list[str]) -> None:
        """Customize bar plot appearance."""
        ax.set_xlabel('Ticker', fontsize=8)
        ax.set_ylabel('Altman Z-Score', fontsize=8)
        ax.set_title('Altman Z-Score Comparison: 2025 vs 2024',
                     fontsize=10, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(tickers, fontsize=7)
        ax.set_ylim(0, 4.2)
        ax.legend(fontsize=6)
        ax.grid(axis='y', alpha=0.3)
        ax.tick_params(axis='y', labelsize=7)

    def _get_spider_angles(self) -> list[float]:
        """Calculate angles for spider chart."""
        angles = np.linspace(
            0, 2 * np.pi, len(self.categories), endpoint=False).tolist()
        angles += angles[:1]  # close the circle
        return angles

    def _plot_single_spider(self, ax: plt.Axes, ticker: str,
                            ratio_arrays: list, angles: list[float]) -> None:
        """Plot a single spider chart for one ticker."""
        # Extract values
        values_2025 = [arr[0] for arr in ratio_arrays]
        values_2024 = [arr[1] for arr in ratio_arrays]

        # Close the circle
        values_2025 += values_2025[:1]
        values_2024 += values_2024[:1]

        # Plot
        ax.plot(angles, values_2024, 'o-', linewidth=2,
                label='2024', color='cornflowerblue')
        ax.fill(angles, values_2024, alpha=0.25, color='cornflowerblue')
        ax.plot(angles, values_2025, 'o-', linewidth=2,
                label='2025', color='navy')
        ax.fill(angles, values_2025, alpha=0.25, color='navy')

        # Customize
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(self.categories, size=7)

        max_val = max(max(values_2025[:-1]), max(values_2024[:-1]))
        min_val = min(min(values_2025[:-1]), min(values_2024[:-1]))
        ax.set_ylim(min_val * 1.2 if min_val < 0 else 0, max_val * 1.2)

        ax.set_title(ticker, size=10, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), fontsize=6)
        ax.tick_params(axis='both', labelsize=6)
