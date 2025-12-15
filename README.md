# AI Bubble Health Dashboard

A sophisticated financial analytics dashboard for monitoring AI bubble risk using real-time market data and advanced sentiment analysis.

## 🚀 Features

### Real-time Risk Assessment
- **Bubble Risk Score**: 0-100 scale with color-coded alerts
- **Market Regime Detection**: Healthy Expansion → Late-Cycle Froth → Bubble Risk → Unwind Risk
- **Multi-factor Analysis**: Fundamentals, Valuation, Leverage, Options, Sentiment

### Comprehensive Analytics
- **📊 Executive Summary**: Risk score, key drivers, live alerts
- **📈 Fundamentals Analysis**: Cash flow vs price action, divergence detection
- **📉 Options & Crash Risk**: IV surface, skew analysis, hedging indicators
- **🗺️ Exposure Map**: Portfolio concentration, leverage analysis
- **📰 Sentiment Analysis**: News sentiment, bubble language detection

### Data Integration
- **Alpha Vantage API**: Real-time stock data and fundamentals
- **NewsData.io**: Financial news and sentiment analysis
- **Yahoo Finance**: Alternative data source
- **Mock Data**: Built-in demo mode for testing

## 🛠️ Technology Stack

### Streamlit Deployment
- **Framework**: Streamlit (Python)
- **Visualization**: Plotly.js for interactive charts
- **Data Processing**: Pandas, NumPy
- **Styling**: Custom CSS with dark theme
- **Deployment**: Streamlit Cloud + GitHub

### Key Features
- **Responsive Design**: Works on desktop, tablet, mobile
- **Interactive Charts**: Hover details, zoom, pan
- **Real-time Updates**: Automatic data refresh
- **API Configuration**: Easy setup with configuration panel
- **Professional UI**: Dark theme with glass morphism effects

## 📋 Quick Start

### Local Development
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-bubble-dashboard.git

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run streamlit_app.py
```

### API Keys Setup
1. **Get Alpha Vantage API Key**: https://alphavantage.co (free tier)
2. **Get NewsData.io API Key**: https://newsdata.io (200 requests/day free)
3. **Configure in the app**: Use the sidebar configuration panel

### Deployment Options

#### Option 1: Streamlit Cloud (Recommended)
1. Fork this repository
2. Sign up at [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy automatically

#### Option 2: Local Server
```bash
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

#### Option 3: Docker
```bash
docker build -t ai-bubble-dashboard .
docker run -p 8501:8501 ai-bubble-dashboard
```

## 📊 Risk Scoring Methodology

The dashboard uses a 5-factor risk model:

1. **Fundamental Divergence (30%)**: Price vs cash flow reality
2. **Valuation Stretch (25%)**: P/E ratios and multiple expansion  
3. **Leverage & Liquidity (20%)**: Credit spreads and market breadth
4. **Options Euphoria (15%)**: IV levels and crash premium indicators
5. **Sentiment Crowding (10%)**: News sentiment and narrative analysis

**Risk Levels:**
- **0-35**: Healthy Expansion (Green)
- **35-55**: Late-Cycle Froth (Yellow)  
- **55-75**: Bubble Risk Elevated (Orange)
- **75-100**: Bubble/Unwind Risk (Red)

## 🔧 Configuration

### Environment Variables
```bash
ALPHA_VANTAGE_KEY=your_alpha_vantage_key_here
NEWSDATA_API_KEY=your_newsdata_key_here
```

### Streamlit Secrets
Create `.streamlit/secrets.toml`:
```toml
ALPHA_VANTAGE_KEY = "your_alpha_vantage_key_here"
NEWSDATA_API_KEY = "your_newsdata_key_here"
```

## 📈 Usage Examples

### Basic Usage
```python
# Get risk score
dashboard = AIBubbleDashboard()
score = dashboard.calculate_risk_score()

# Get stock data
data_provider = DataProvider()
stock_data = data_provider.get_stock_data('NVDA')

# Get sentiment
sentiment = data_provider.get_news_sentiment('AI bubble')
```

### API Integration
```python
# Alpha Vantage
alpha_vantage = AlphaVantageAPI(api_key)
quote = alpha_vantage.get_quote('NVDA')

# NewsData.io
newsdata = NewsDataAPI(api_key)
articles = newsdata.search('artificial intelligence')
```

## 🎯 Use Cases

### For Investors
- Monitor AI stock bubble risk
- Track portfolio concentration
- Identify market turning points
- Make informed investment decisions

### For Analysts
- Research market sentiment
- Analyze fundamental trends
- Track options market activity
- Generate research reports

### For Traders
- Real-time risk monitoring
- Options flow analysis
- Sentiment-based signals
- Risk management tools

## 📚 Documentation

### API Documentation
- [Alpha Vantage API](https://www.alphavantage.co/documentation/)
- [NewsData.io API](https://newsdata.io/docs)
- [Streamlit Documentation](https://docs.streamlit.io)

### Deployment Guides
- [GitHub Deployment Guide](GITHUB_DEPLOYMENT_GUIDE.md)
- [API Configuration Guide](API_CONFIGURATION_GUIDE.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes only. Not financial advice. Use at your own risk.

## 🔗 Links

- **Live Demo**: [Your Streamlit URL]
- **GitHub Repository**: [Your GitHub URL]
- **Documentation**: [Full documentation]
- **Support**: [Community forum or contact]

---

**⚠️ Important Disclaimer:**
This dashboard is for educational and research purposes only. It should not be used as the sole basis for investment decisions. Always consult with qualified financial professionals before making investment choices.

**Built with ❤️ using Streamlit, Python, and modern web technologies.**