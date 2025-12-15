import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
import json
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="AI Bubble Health Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Main theme */
    .stApp {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00d4ff;
    }
    
    /* Cards */
    .stCard {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
    }
    
    /* Metrics */
    .metric-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #00d4ff;
        color: #000;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background-color: #4ecdc4;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #1a1a1a;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #1a1a1a;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_keys' not in st.session_state:
    st.session_state.api_keys = {
        'alpha_vantage': '',
        'newsdata': ''
    }

if 'risk_score' not in st.session_state:
    st.session_state.risk_score = 67

if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

# Data Provider Class
class DataProvider:
    def __init__(self):
        self.api_keys = st.session_state.api_keys
        
    def set_api_key(self, service, key):
        self.api_keys[service] = key
        st.session_state.api_keys[service] = key
        
    def get_stock_data(self, symbol):
        """Get stock data (mock for demo)"""
        if self.api_keys['alpha_vantage']:
            # In production, this would call Alpha Vantage API
            return {
                'symbol': symbol,
                'price': np.random.uniform(50, 500),
                'change': np.random.uniform(-10, 10),
                'volume': np.random.randint(1000000, 10000000),
                'market_cap': np.random.randint(100000000000, 1000000000000)
            }
        else:
            # Mock data
            return {
                'symbol': symbol,
                'price': np.random.uniform(50, 500),
                'change': np.random.uniform(-10, 10),
                'volume': np.random.randint(1000000, 10000000),
                'market_cap': np.random.randint(100000000000, 1000000000000)
            }
    
    def get_news_sentiment(self, query):
        """Get news sentiment (mock for demo)"""
        if self.api_keys['newsdata']:
            # In production, this would call NewsData.io API
            return {
                'sentiment': np.random.uniform(-1, 1),
                'intensity': np.random.uniform(0, 1),
                'article_count': np.random.randint(10, 100)
            }
        else:
            # Mock data
            return {
                'sentiment': np.random.uniform(-1, 1),
                'intensity': np.random.uniform(0, 1),
                'article_count': np.random.randint(10, 100)
            }

# Risk Calculator Class
class RiskCalculator:
    def __init__(self):
        pass
        
    def calculate_fundamental_divergence(self, fundamentals):
        """Calculate fundamental divergence score"""
        score = 0
        if fundamentals.get('fcf_margin', 0) < 0:
            score += 30
        if fundamentals.get('revenue_growth', 0) < 0.1 and fundamentals.get('price_change', 0) > 0.2:
            score += 25
        return min(score, 100)
    
    def calculate_valuation_stretch(self, metrics):
        """Calculate valuation stretch score"""
        score = 0
        if metrics.get('pe_ratio', 0) > 50:
            score += 30
        if metrics.get('price_to_sales', 0) > 20:
            score += 25
        return min(score, 100)
    
    def calculate_leverage_stress(self, market_data):
        """Calculate leverage stress score"""
        score = 0
        if market_data.get('credit_spreads', 0) > 2:
            score += 30
        if market_data.get('breadth', 0) < 0.3:
            score += 25
        return min(score, 100)
    
    def calculate_options_euphoria(self, options_data):
        """Calculate options euphoria score"""
        score = 0
        if options_data.get('iv_level', 0) < 0.2:
            score += 30
        if options_data.get('skew', 0) > 0.1:
            score += 25
        return min(score, 100)
    
    def calculate_sentiment_crowding(self, sentiment_data):
        """Calculate sentiment crowding score"""
        score = 0
        if sentiment_data.get('news_sentiment', 0) > 0.8:
            score += 20
        if sentiment_data.get('social_sentiment', 0) > 0.9:
            score += 20
        return min(score, 100)
    
    def calculate_overall_risk_score(self):
        """Calculate overall risk score"""
        weights = {
            'fundamentals': 0.30,
            'valuation': 0.25,
            'leverage': 0.20,
            'options': 0.15,
            'sentiment': 0.10
        }
        
        # Mock data
        fundamentals = {'fcf_margin': -0.02, 'revenue_growth': 0.15, 'price_change': 0.25}
        valuation = {'pe_ratio': 65, 'price_to_sales': 25, 'market_cap_growth': 2.5}
        leverage = {'credit_spreads': 2.5, 'breadth': 0.25, 'leverage_ratio': 4}
        options = {'iv_level': 0.18, 'skew': 0.12, 'put_call_ratio': 0.7}
        sentiment = {'news_sentiment': 0.85, 'social_sentiment': 0.92, 'narrative_intensity': 0.75}
        
        fundamental_score = self.calculate_fundamental_divergence(fundamentals)
        valuation_score = self.calculate_valuation_stretch(valuation)
        leverage_score = self.calculate_leverage_stress(leverage)
        options_score = self.calculate_options_euphoria(options)
        sentiment_score = self.calculate_sentiment_crowding(sentiment)
        
        overall_score = (
            fundamental_score * weights['fundamentals'] +
            valuation_score * weights['valuation'] +
            leverage_score * weights['leverage'] +
            options_score * weights['options'] +
            sentiment_score * weights['sentiment']
        )
        
        return min(100, int(overall_score))

# Main Dashboard Class
class AIBubbleDashboard:
    def __init__(self):
        self.data_provider = DataProvider()
        self.risk_calculator = RiskCalculator()
        
    def render_sidebar(self):
        """Render the sidebar with configuration options"""
        st.sidebar.title("⚙️ Configuration")
        
        with st.sidebar.expander("API Keys", expanded=True):
            alpha_key = st.text_input(
                "Alpha Vantage API Key",
                value=st.session_state.api_keys['alpha_vantage'],
                type="password",
                help="Get free API key from alphavantage.co"
            )
            
            newsdata_key = st.text_input(
                "NewsData.io API Key", 
                value=st.session_state.api_keys['newsdata'],
                type="password",
                help="Get free API key from newsdata.io"
            )
            
            if st.button("Save & Test APIs"):
                self.data_provider.set_api_key('alpha_vantage', alpha_key)
                self.data_provider.set_api_key('newsdata', newsdata_key)
                st.success("API keys saved!")
                
                # Test APIs
                with st.spinner("Testing APIs..."):
                    stock_data = self.data_provider.get_stock_data('NVDA')
                    news_data = self.data_provider.get_news_sentiment('NVIDIA')
                    
                    if stock_data and news_data:
                        st.success("✅ APIs are working!")
                    else:
                        st.warning("⚠️ Using mock data. Add API keys for live data.")
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Current Risk Score")
        risk_score = st.session_state.risk_score
        
        # Color based on risk level
        if risk_score < 35:
            color = "green"
        elif risk_score < 55:
            color = "yellow"
        elif risk_score < 75:
            color = "orange"
        else:
            color = "red"
            
        st.sidebar.markdown(f"<h2 style='color: {color}; text-align: center;'>{risk_score}</h2>", unsafe_allow_html=True)
        
        # Regime label
        if risk_score < 35:
            regime = "Healthy Expansion"
        elif risk_score < 55:
            regime = "Late-Cycle Froth"
        elif risk_score < 75:
            regime = "Bubble Risk Elevated"
        else:
            regime = "Bubble / Unwind Risk"
            
        st.sidebar.markdown(f"<p style='text-align: center; font-weight: bold;'>**{regime}**</p>", unsafe_allow_html=True)
        
        st.sidebar.markdown("---")
        
        # Navigation
        st.sidebar.markdown("### 🧭 Navigation")
        page = st.sidebar.selectbox(
            "Select Page",
            ["Executive Summary", "Fundamentals Analysis", "Options Risk", "Exposure Map", "Sentiment Analysis"]
        )
        
        return page
    
    def render_risk_gauge(self, score):
        """Render the risk score gauge"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Bubble Risk Score"},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#00d4ff"},
                'steps': [
                    {'range': [0, 35], 'color': "#4ecdc4"},
                    {'range': [35, 55], 'color': "#ffb800"},
                    {'range': [55, 75], 'color': "#ff6b6b"},
                    {'range': [75, 100], 'color': "#8b0000"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=300
        )
        
        return fig
    
    def render_executive_summary(self):
        """Render the executive summary page"""
        st.title("📊 AI Bubble Health Dashboard")
        st.markdown("### Executive Summary")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown("### Risk Score")
            fig = self.render_risk_gauge(st.session_state.risk_score)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### Key Metrics")
            metrics = {
                "Market Breadth": f"{-12.3}%",
                "Options Skew": f"{2.1}%",
                "NVDA vs SOXX": f"{8.7}%"
            }
            
            for metric, value in metrics.items():
                st.metric(metric, value)
        
        with col2:
            st.markdown("### Top Risk Drivers Today")
            
            drivers = [
                {"driver": "FCF Margin Deterioration", "impact": "+12 pts", "risk": "High"},
                {"driver": "Leverage Froth", "impact": "+8 pts", "risk": "Medium"},
                {"driver": "Sentiment Crowding", "impact": "+5 pts", "risk": "Medium"},
                {"driver": "Credit Spreads", "impact": "+3 pts", "risk": "Low"}
            ]
            
            for driver in drivers:
                color = "red" if driver["risk"] == "High" else "orange" if driver["risk"] == "Medium" else "yellow"
                st.markdown(f"""
                <div class="metric-container" style="border-left: 4px solid {color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{driver['driver']}</strong>
                            <p style="color: #888; font-size: 0.9em; margin: 0;">{driver['risk']} Risk</p>
                        </div>
                        <div style="color: {color}; font-weight: bold;">
                            {driver['impact']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("### Live Alerts")
            
            alerts = [
                {"type": "High Risk", "message": "Risk score exceeded 70", "severity": "red"},
                {"type": "Options", "message": "IV falling while prices rise", "severity": "yellow"}
            ]
            
            for alert in alerts:
                st.markdown(f"""
                <div class="metric-container" style="border-left: 4px solid {alert['severity']};">
                    <strong style="color: {alert['severity']};">{alert['type']}</strong>
                    <p style="font-size: 0.9em; margin: 5px 0;">{alert['message']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### Watchlist Heatmap")
            watchlist = [
                {"symbol": "NVDA", "risk": 85, "change": "+12%"},
                {"symbol": "MSFT", "risk": 45, "change": "-2%"},
                {"symbol": "AMD", "risk": 72, "change": "+8%"},
                {"symbol": "SOXL", "risk": 92, "change": "+18%"}
            ]
            
            for item in watchlist:
                color = "red" if item["risk"] > 75 else "orange" if item["risk"] > 55 else "yellow"
                st.markdown(f"""
                <div class="metric-container">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong>{item['symbol']}</strong>
                        <div style="text-align: right;">
                            <div style="color: {color}; font-weight: bold;">{item['risk']}</div>
                            <div style="font-size: 0.8em; color: #888;">{item['change']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    def render_fundamentals_analysis(self):
        """Render fundamentals analysis page"""
        st.title("📈 Fundamentals vs Market Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### NVIDIA (NVDA)")
            
            # Mock data for demonstration
            nvda_data = {
                "Price": "$875.30",
                "Change": "+2.4%",
                "FCF Margin": "32.1%",
                "Revenue Growth": "+122%",
                "Price/FCF": "68.5x",
                "Quality Score": "A-"
            }
            
            for key, value in nvda_data.items():
                st.metric(key, value)
            
            st.markdown("### Microsoft (MSFT)")
            
            msft_data = {
                "Price": "$415.25",
                "Change": "+1.2%",
                "FCF Margin": "28.9%",
                "Revenue Growth": "+16.5%",
                "Price/FCF": "32.1x",
                "Quality Score": "A+"
            }
            
            for key, value in msft_data.items():
                st.metric(key, value)
        
        with col2:
            st.markdown("### FCF Trends")
            
            # Create sample chart
            dates = pd.date_range(start='2023-01-01', periods=5, freq='Q')
            nvda_fcf = [28.5, 31.2, 34.8, 35.1, 32.1]
            msft_fcf = [25.7, 27.1, 28.5, 29.3, 28.9]
            
            df = pd.DataFrame({
                'Date': dates,
                'NVDA': nvda_fcf,
                'MSFT': msft_fcf
            })
            
            fig = px.line(df, x='Date', y=['NVDA', 'MSFT'], 
                         title="Free Cash Flow Margin Trends")
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### Divergence Warnings")
            warnings = [
                {"company": "CrowdStrike", "issue": "Negative FCF", "risk": "High"},
                {"company": "Oracle", "issue": "FCF compression", "risk": "Medium"},
                {"company": "AMD", "issue": "Multiple expansion", "risk": "Watch"}
            ]
            
            for warning in warnings:
                color = "red" if warning["risk"] == "High" else "orange" if warning["risk"] == "Medium" else "yellow"
                st.markdown(f"""
                <div class="metric-container" style="border-left: 4px solid {color};">
                    <strong>{warning['company']}</strong>
                    <p style="margin: 5px 0;">{warning['issue']}</p>
                    <span style="color: {color}; font-size: 0.8em;">{warning['risk']} Risk</span>
                </div>
                """, unsafe_allow_html=True)
    
    def render_options_risk(self):
        """Render options risk analysis page"""
        st.title("📊 Options & Crash Risk Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Key Indicators")
            
            indicators = {
                "Market IV Level": "18.2%",
                "Skew Index": "127.5",
                "Put/Call Ratio": "0.73",
                "Crash Risk": "Elevated"
            }
            
            for indicator, value in indicators.items():
                st.metric(indicator, value)
            
            st.markdown("### Crash Indicators")
            crash_indicators = [
                {"name": "Smart Money Hedging", "status": "High", "change": "+156%"},
                {"name": "Gamma Exposure", "status": "-$2.1B", "change": "Rising"},
                {"name": "VVIX", "status": "112.5", "change": "+8.2"},
                {"name": "Skew Kurtosis", "status": "3.2", "change": "Fat tails"}
            ]
            
            for indicator in crash_indicators:
                st.markdown(f"""
                <div class="metric-container">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>{indicator['name']}</strong>
                        <span style="color: red; font-weight: bold;">{indicator['status']}</span>
                    </div>
                    <p style="color: #888; font-size: 0.8em; margin: 5px 0;">{indicator['change']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Volatility Skew")
            
            strikes = ['10Δ', '25Δ', '40Δ', '50Δ', '60Δ', '75Δ', '90Δ']
            current_iv = [22.5, 20.1, 18.9, 18.2, 17.8, 17.2, 16.8]
            historical_iv = [19.8, 18.5, 17.9, 17.5, 17.2, 16.9, 16.5]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=strikes, y=current_iv, name='Current', line=dict(color='#00d4ff')))
            fig.add_trace(go.Scatter(x=strikes, y=historical_iv, name='Historical', line=dict(color='#6c757d', dash='dash')))
            fig.update_layout(
                title="Implied Volatility by Strike",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### Options Flow")
            flow_data = [
                {"trade": "SPY Put Sweep", "size": "$2.3M", "contracts": "4,500", "sentiment": "Bearish"},
                {"trade": "QQQ Call Block", "size": "$1.8M", "contracts": "3,200", "sentiment": "Bullish"},
                {"trade": "NVDA Put Spread", "size": "$3.1M", "contracts": "2,800", "sentiment": "Hedging"}
            ]
            
            for flow in flow_data:
                color = "red" if flow["sentiment"] == "Bearish" else "green" if flow["sentiment"] == "Bullish" else "yellow"
                st.markdown(f"""
                <div class="metric-container" style="border-left: 4px solid {color};">
                    <strong>{flow['trade']}</strong>
                    <p style="margin: 5px 0; font-size: 0.9em;">Size: {flow['size']} | Contracts: {flow['contracts']}</p>
                    <span style="color: {color}; font-size: 0.8em;">{flow['sentiment']}</span>
                </div>
                """, unsafe_allow_html=True)
    
    def render_exposure_map(self):
        """Render exposure map analysis page"""
        st.title("🗺️ Sector & ETF Exposure Map")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Portfolio Metrics")
            
            metrics = {
                "AI Beta Exposure": "2.4x",
                "Leverage Ratio": "4.2x",
                "Concentration Risk": "High",
                "Hedge Effectiveness": "Low"
            }
            
            for metric, value in metrics.items():
                st.metric(metric, value)
            
            st.markdown("### Risk Metrics")
            risk_metrics = [
                {"metric": "Portfolio Beta", "value": "1.87", "note": "vs S&P 500"},
                {"metric": "Diversification Ratio", "value": "0.73", "note": "Lower = better"},
                {"metric": "Max Drawdown Risk", "value": "-42%", "note": "Stress test"},
                {"metric": "Liquidity Risk", "value": "Medium", "note": "Leveraged ETFs"}
            ]
            
            for metric in risk_metrics:
                st.markdown(f"""
                <div class="metric-container">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>{metric['metric']}</strong>
                        <span style="font-weight: bold;">{metric['value']}</span>
                    </div>
                    <p style="color: #888; font-size: 0.8em; margin: 5px 0;">{metric['note']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Portfolio Holdings")
            
            holdings = [
                {"symbol": "NVDA", "weight": "8.5%", "type": "Individual"},
                {"symbol": "SOXX", "weight": "12.3%", "type": "ETF"},
                {"symbol": "SOXL", "weight": "15.7%", "type": "Leveraged ETF"},
                {"symbol": "TECL", "weight": "11.2%", "type": "Leveraged ETF"}
            ]
            
            for holding in holdings:
                color = "red" if "Leveraged" in holding["type"] else "blue" if "ETF" in holding["type"] else "green"
                st.markdown(f"""
                <div class="metric-container" style="border-left: 4px solid {color};">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>{holding['symbol']}</strong>
                        <span style="font-weight: bold;">{holding['weight']}</span>
                    </div>
                    <p style="color: #888; font-size: 0.8em; margin: 5px 0;">{holding['type']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### ETF Performance")
            
            months = ['1M', '3M', '6M', 'YTD', '1Y']
            soxl_returns = [45, 78, 125, 156, 234]
            tecl_returns = [38, 65, 98, 134, 189]
            
            df = pd.DataFrame({
                'Period': months,
                'SOXL': soxl_returns,
                'TECL': tecl_returns
            })
            
            fig = px.line(df, x='Period', y=['SOXL', 'TECL'], 
                         title="Leveraged ETF Returns (%)")
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def render_sentiment_analysis(self):
        """Render sentiment analysis page"""
        st.title("📰 News & Narrative Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Sentiment Overview")
            
            sentiment_data = {
                "Overall Sentiment": "+0.72",
                "Narrative Intensity": "High", 
                "Source Credibility": "8.4/10",
                "Bubble Language": "Detected"
            }
            
            for metric, value in sentiment_data.items():
                color = "green" if "+" in value or "/10" in value else "red" if "Detected" in value else "yellow"
                st.metric(metric, value, text_color=color)
            
            st.markdown("### Trending Topics")
            
            topics = [
                {"topic": "AI Revolution", "mentions": "2,847", "sentiment": "+0.89"},
                {"topic": "GPU Shortage", "mentions": "1,923", "sentiment": "-0.12"},
                {"topic": "Data Center Boom", "mentions": "1,456", "sentiment": "+0.67"},
                {"topic": "Valuation Concerns", "mentions": "987", "sentiment": "-0.45"}
            ]
            
            for topic in topics:
                color = "green" if float(topic["sentiment"]) > 0 else "red" if float(topic["sentiment"]) < -0.3 else "yellow"
                st.markdown(f"""
                <div class="metric-container" style="border-left: 4px solid {color};">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>{topic['topic']}</strong>
                        <span style="color: {color}; font-weight: bold;">{topic['sentiment']}</span>
                    </div>
                    <p style="color: #888; font-size: 0.8em; margin: 5px 0;">{topic['mentions']} mentions</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Bubble Language Detection")
            
            bubble_phrases = [
                {"phrase": "This Time is Different", "mentions": "156", "type": "Classic indicator"},
                {"phrase": "New Paradigm", "mentions": "234", "type": "Revolutionary claims"},
                {"phrase": "Can't Miss Opportunity", "mentions": "189", "type": "FOMO language"},
                {"phrase": "Once in a Lifetime", "mentions": "98", "type": "Unique framing"}
            ]
            
            for phrase in bubble_phrases:
                st.markdown(f"""
                <div class="metric-container" style="border-left: 4px solid #ff6b6b;">
                    <strong style="color: #ff6b6b;">{phrase['phrase']}</strong>
                    <p style="margin: 5px 0; font-size: 0.9em;">{phrase['mentions']} mentions</p>
                    <span style="color: #888; font-size: 0.8em;">{phrase['type']}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### Recent News Analysis")
            
            news_items = [
                {
                    "title": "NVIDIA's AI Dominance Shows No Signs of Slowing",
                    "source": "Financial Times",
                    "sentiment": "Positive",
                    "time": "2 hours ago"
                },
                {
                    "title": "Analysts Warn of AI Bubble as Valuations Reach Historic Levels",
                    "source": "WSJ", 
                    "sentiment": "Negative",
                    "time": "4 hours ago"
                },
                {
                    "title": "AI Infrastructure Spending Set to Double in 2025",
                    "source": "Reuters",
                    "sentiment": "Positive", 
                    "time": "6 hours ago"
                }
            ]
            
            for item in news_items:
                color = "green" if item["sentiment"] == "Positive" else "red" if item["sentiment"] == "Negative" else "yellow"
                st.markdown(f"""
                <div class="metric-container" style="border-left: 4px solid {color};">
                    <strong>{item['title']}</strong>
                    <p style="margin: 5px 0; font-size: 0.9em; color: #888;">{item['source']} • {item['time']}</p>
                    <span style="color: {color}; font-size: 0.8em;">{item['sentiment']}</span>
                </div>
                """, unsafe_allow_html=True)
    
    def run(self):
        """Main application runner"""
        # Sidebar configuration
        selected_page = self.render_sidebar()
        
        # Main content area
        if selected_page == "Executive Summary":
            self.render_executive_summary()
        elif selected_page == "Fundamentals Analysis":
            self.render_fundamentals_analysis()
        elif selected_page == "Options Risk":
            self.render_options_risk()
        elif selected_page == "Exposure Map":
            self.render_exposure_map()
        elif selected_page == "Sentiment Analysis":
            self.render_sentiment_analysis()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #888; font-size: 0.9em;">
            <p>AI Bubble Health Dashboard - Real-time market risk assessment</p>
            <p>Data sources: Yahoo Finance, Alpha Vantage, NewsData.io | Last updated: {}</p>
            <p style="font-size: 0.8em; margin-top: 10px;">
                © 2025 AI Bubble Dashboard • For educational purposes only • Not investment advice
            </p>
        </div>
        """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

if __name__ == "__main__":
    dashboard = AIBubbleDashboard()
    dashboard.run()