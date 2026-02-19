import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.5
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['legend.frameon'] = True
plt.rcParams['legend.facecolor'] = 'white'
plt.rcParams['legend.edgecolor'] = 'black'
plt.rcParams['legend.loc'] = 'best'


class ModelsVisualization:
    """
    Visualizer for Altman Z-Score analysis with support for bar charts and spider charts.
    """
    
    def __init__(self, altman_z_scores: dict = None, component_ratios: dict = None):
        """
        Initialize the visualizer with Z-scores and/or component ratios.
        
        Args:
            altman_z_scores (dict): {ticker: [z_score_2025, z_score_2024]}
            component_ratios (dict): {ticker: [ratio_arrays]} where each array is [2025, 2024]
        """
        self.altman_z_scores = altman_z_scores
        self.component_ratios = component_ratios
        self.categories = ['Liquidity', 'Profitability', 'Efficiency', 'Leverage', 'Turnover']
    
    def plot_z_score_comparison(self) -> None:
        """
        Plots bar chart comparing Altman Z-scores across years.
        
        Returns:
            fig: The matplotlib figure object for the Z-score comparison.
        """
        if self.altman_z_scores is None:
            raise ValueError("No Z-score data provided. Initialize with altman_z_scores.")
        
        tickers = list(self.altman_z_scores.keys())
        z_scores_current = [self.altman_z_scores[t][0] for t in tickers]
        z_scores_old = [self.altman_z_scores[t][1] for t in tickers]
        
        x = np.arange(len(tickers))
        width = 0.35

        fig, ax = plt.subplots(figsize=(10, 6))

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
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(10, 4 * n_rows), 
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
    
    def _add_threshold_zones(self, ax: plt.Axes) -> None:
        """Add Z-score threshold lines and zones."""
        ax.axhline(y=3.0, color='darkseagreen', linestyle='--', linewidth=1.5)
        ax.axhline(y=1.8, color='indianred', linestyle='--', linewidth=1.5)
        
        ax.axhspan(3.0, 5.0, color='darkseagreen', alpha=0.25, label='Low Bankruptcy Risk')
        ax.axhspan(0, 1.8, color='indianred', alpha=0.25, label='High Bankruptcy Risk')
    
    def _plot_bars(self, ax: plt.Axes, x: np.ndarray, width: float, 
                   z_scores_old: list[float], z_scores_current: list[float]) -> None:
        """Plot bar charts with value labels."""
        # 2024 bars
        ax.bar(x - width/2, z_scores_old, width, color='cornflowerblue', label='2024')
        for i, height in enumerate(z_scores_old):
            ax.text(x[i] - width/2, height - 0.15, f'{height:.2f}', 
                   ha='center', va='bottom', fontsize=9, color='black')

        # 2025 bars
        ax.bar(x + width/2, z_scores_current, width, color='navy', label='2025')
        for i, height in enumerate(z_scores_current):
            ax.text(x[i] + width/2, height - 0.15, f'{height:.2f}', 
                   ha='center', va='bottom', fontsize=9, color='white')
    
    def _customize_bar_plot(self, ax: plt.Axes, x: np.ndarray, tickers: list[str]) -> None:
        """Customize bar plot appearance."""
        ax.set_xlabel('Ticker', fontsize=12)
        ax.set_ylabel('Altman Z-Score', fontsize=12)
        ax.set_title('Altman Z-Score Comparison: 2025 vs 2024', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(tickers)
        ax.set_ylim(0, 4.2)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
    
    def _get_spider_angles(self) -> list[float]:
        """Calculate angles for spider chart."""
        angles = np.linspace(0, 2 * np.pi, len(self.categories), endpoint=False).tolist()
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
        ax.plot(angles, values_2024, 'o-', linewidth=2, label='2024', color='cornflowerblue')
        ax.fill(angles, values_2024, alpha=0.25, color='cornflowerblue')
        ax.plot(angles, values_2025, 'o-', linewidth=2, label='2025', color='navy')
        ax.fill(angles, values_2025, alpha=0.25, color='navy')
        
        # Customize
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(self.categories, size=10)
        
        max_val = max(max(values_2025[:-1]), max(values_2024[:-1]))
        min_val = min(min(values_2025[:-1]), min(values_2024[:-1]))
        ax.set_ylim(min_val * 1.2 if min_val < 0 else 0, max_val * 1.2)
        
        ax.set_title(ticker, size=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1))

