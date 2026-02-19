import streamlit as st
import matplotlib.pyplot as plt
from models import Altman, Merton
from visualizations import ModelsVisualization

# Page config
st.set_page_config(page_title="Altman Z-Score Analysis", layout="wide")

def main():
    # Title
    st.title("Stock Market Risk Analysis with Altman Z-Score & Merton Model")
    st.markdown("**Diego Lozoya Morales | 745345")
    st.markdown("---")
    
    # Input section
    col1, col2 = st.columns([3, 1])
    with col1:
        ticker_input = st.text_input(
            "Enter ticker symbols (comma-separated):", 
            value='AMT, AVGO, LLY, TSM, V, WMT'
        )
    with col2:
        st.write("")
        st.write("")
        run_analysis = st.button("Run Analysis", type="primary")
    
    if run_analysis:
        tickers = [t.strip().upper() for t in ticker_input.split(",")]
        
        with st.spinner(f"Loading data for {', '.join(tickers)}..."):
            try:
                # Calculate data
                altman_z_scores = {}
                ratios = {}
                
                for ticker in tickers:
                    stock = Altman(ticker)
                    altman_z_scores[ticker] = stock.altman_z_score()
                    ratios[ticker] = stock.get_ratio_components()
                    
                default_probabilities = {}
                
                for ticker in tickers:
                    stock = Merton(ticker)
                    default_probabilities[ticker] = stock.default_probability()
                
                st.success(f"Analysis complete for {', '.join(tickers)}!")
                st.markdown("---")
                
                # Create visualizer
                visualizer = ModelsVisualization(
                    altman_z_scores=altman_z_scores,
                    component_ratios=ratios
                )
                
                # 1. Altman Z-Score Model
                st.header("Altman Z-Score Model")
                
                # a) Z-Score Comparison Bar Chart
                st.subheader("Z-Score Comparison")
                fig1 = visualizer.plot_z_score_comparison()
                st.pyplot(fig1, use_container_width=False)
                plt.close()
                                
                # b) Components spider Charts
                st.subheader("Component Analysis")
                fig2 = visualizer.plot_component_spider_charts()
                st.pyplot(fig2, use_container_width=False)
                plt.close()
                
                st.markdown("---")
                
                # 2. Merton Default Probability Model
                st.header("Merton Default Probability Model")
                
                # quick print of default probabilities
                st.subheader("Default Probabilities")
                for ticker, prob in default_probabilities.items():
                    st.markdown(f"- **{ticker}**: {prob:.2%}")
                
                
                # 3. Interpretation
                st.header("Interpretation")
                
                
                # 4. Sources
                st.header("Sources")
                st.markdown("- https://finance.yahoo.com/ - For financial data")

                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.exception(e)

if __name__ == "__main__":
    main()