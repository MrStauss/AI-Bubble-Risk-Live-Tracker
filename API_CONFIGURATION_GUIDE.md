# AI Bubble Health Dashboard - API Configuration Guide

## Overview
This guide explains how to configure the AI Bubble Health Dashboard with live data APIs, including the switch from NewsAPI to NewsData.io and Alpha Vantage API setup.

## 🔄 NewsData.io Integration (Replaced NewsAPI)

### Why NewsData.io?
NewsData.io offers several advantages over NewsAPI:
- **Better financial news coverage** with real-time updates
- **More affordable pricing** (free tier available)
- **Better sentiment analysis** capabilities
- **More reliable** for financial news sources

### Setup Instructions

#### 1. Get Your NewsData.io API Key
1. Visit [NewsData.io](https://newsdata.io/)
2. Sign up for a free account or choose a paid plan
3. Navigate to your dashboard to get your API key
4. The free tier includes 200 requests per day

#### 2. Configure in the Dashboard
Replace `'YOUR_NEWSDATA_API_KEY'` in `/main.js` with your actual API key:

```javascript
// In DataProvider constructor
this.apiKeys = {
    alphaVantage: 'YOUR_ALPHA_VANTAGE_KEY',
    newsData: 'your_actual_newdata_api_key_here'  // Replace this
};
```

#### 3. API Usage Example
```javascript
// Get news data with sentiment analysis
const newsData = await dataProvider.getNewsDataFromNewsData('AI bubble NVIDIA', '2024-01-01', '2024-12-16');
console.log('Sentiment Score:', newsData.sentiment);
console.log('Article Count:', newsData.articleCount);
console.log('Articles:', newsData.articles);
```

## 📊 Alpha Vantage API Configuration

### Setup Instructions

#### 1. Get Your Alpha Vantage API Key
1. Visit [Alpha Vantage](https://www.alphavantage.co/)
2. Click "Get Free API Key"
3. Fill out the registration form
4. Check your email for the API key
5. The free tier includes 5 API calls per minute, 500 per day

#### 2. Configure in the Dashboard
Replace `'YOUR_ALPHA_VANTAGE_KEY'` in `/main.js` with your actual API key:

```javascript
// In DataProvider constructor
this.apiKeys = {
    alphaVantage: 'your_actual_alpha_vantage_key_here',  // Replace this
    newsData: 'YOUR_NEWSDATA_API_KEY'
};
```

#### 3. Available Alpha Vantage Endpoints

**Stock Data:**
```javascript
// Get real-time stock quote
const quote = await dataProvider.getAlphaVantageQuote('NVDA');

// Get historical data
const historical = await dataProvider.getAlphaVantageHistorical('NVDA', 'TIME_SERIES_DAILY');

// Get company fundamentals
const fundamentals = await dataProvider.getAlphaVantageFundamentals('NVDA');
```

**Technical Indicators:**
```javascript
// Get RSI
const rsi = await dataProvider.getAlphaVantageIndicator('RSI', 'NVDA', 'daily', 14);

// Get MACD
const macd = await dataProvider.getAlphaVantageIndicator('MACD', 'NVDA', 'daily', null, { fastperiod: 12, slowperiod: 26, signalperiod: 9 });
```

### 4. Implementation Methods

Add these methods to the DataProvider class:

```javascript
// Alpha Vantage API methods
async getAlphaVantageQuote(symbol) {
    try {
        const params = new URLSearchParams({
            function: 'GLOBAL_QUOTE',
            symbol: symbol,
            apikey: this.apiKeys.alphaVantage
        });

        const response = await fetch(`${this.baseUrls.alphaVantage}?${params}`);
        const data = await response.json();
        
        if (data['Global Quote']) {
            return {
                symbol: symbol,
                price: parseFloat(data['Global Quote']['05. price']),
                change: parseFloat(data['Global Quote']['09. change']),
                changePercent: data['Global Quote']['10. change percent'],
                volume: parseInt(data['Global Quote']['06. volume'])
            };
        }
        return null;
    } catch (error) {
        console.error('Alpha Vantage API error:', error);
        return null;
    }
}

async getAlphaVantageHistorical(symbol, functionName = 'TIME_SERIES_DAILY') {
    try {
        const params = new URLSearchParams({
            function: functionName,
            symbol: symbol,
            apikey: this.apiKeys.alphaVantage
        });

        const response = await fetch(`${this.baseUrls.alphaVantage}?${params}`);
        const data = await response.json();
        
        // Process and return historical data
        const timeSeriesKey = Object.keys(data).find(key => key.includes('Time Series'));
        if (timeSeriesKey && data[timeSeriesKey]) {
            return data[timeSeriesKey];
        }
        return null;
    } catch (error) {
        console.error('Alpha Vantage historical data error:', error);
        return null;
    }
}

async getAlphaVantageFundamentals(symbol) {
    try {
        const params = new URLSearchParams({
            function: 'OVERVIEW',
            symbol: symbol,
            apikey: this.apiKeys.alphaVantage
        });

        const response = await fetch(`${this.baseUrls.alphaVantage}?${params}`);
        const data = await response.json();
        
        return {
            peRatio: parseFloat(data.PERatio) || 0,
            priceToBook: parseFloat(data.PriceToBookRatio) || 0,
            roe: parseFloat(data.ReturnOnEquityTTM) || 0,
            profitMargin: parseFloat(data.ProfitMargin) || 0,
            marketCap: parseFloat(data.MarketCapitalization) || 0
        };
    } catch (error) {
        console.error('Alpha Vantage fundamentals error:', error);
        return null;
    }
}
```

## ⚙️ Configuration File Setup

### Environment Variables (Recommended for Production)
Create a `.env` file in your project root:

```bash
# API Keys
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
NEWSDATA_API_KEY=your_newdata_key_here

# Optional: Other configurations
REFRESH_INTERVAL=30000
ALERT_THRESHOLD=70
```

### Alternative: Direct Configuration
If you prefer not to use environment variables, edit the `main.js` file directly:

```javascript
// Option 1: Hardcode the keys (not recommended for production)
this.apiKeys = {
    alphaVantage: 'YOUR_ACTUAL_ALPHA_VANTAGE_KEY',
    newsData: 'YOUR_ACTUAL_NEWSDATA_KEY'
};

// Option 2: Load from a separate config file
import { apiKeys } from './config.js';
this.apiKeys = apiKeys;
```

## 🧪 Testing Your Configuration

### Test NewsData.io Integration
```javascript
// In browser console after loading the dashboard
const dataProvider = new DataProvider();
dataProvider.setApiKey('newsData', 'your_newdata_api_key');

// Test news fetching
dataProvider.getNewsDataFromNewsData('NVIDIA AI stock market')
    .then(data => console.log('News data:', data))
    .catch(error => console.error('Error:', error));
```

### Test Alpha Vantage Integration
```javascript
// Test Alpha Vantage
dataProvider.setApiKey('alphaVantage', 'your_alpha_vantage_key');

// Test stock data fetching
dataProvider.getAlphaVantageQuote('NVDA')
    .then(data => console.log('Stock quote:', data))
    .catch(error => console.error('Error:', error));
```

## 🔒 Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** in production
3. **Rotate API keys** periodically
4. **Monitor API usage** to prevent abuse
5. **Implement rate limiting** for user-facing features

## 📋 API Rate Limits

### Alpha Vantage (Free Tier)
- 5 API calls per minute
- 500 API calls per day
- Real-time data available

### NewsData.io (Free Tier)
- 200 requests per day
- 1 request per second
- Real-time news updates

### Recommended Usage Strategy
1. **Cache responses** to minimize API calls
2. **Batch requests** when possible
3. **Implement retry logic** for failed requests
4. **Use mock data** for development/testing
5. **Monitor usage** to avoid hitting limits

## 🚨 Troubleshooting

### Common Issues
1. **"Invalid API key"** - Check key spelling and account status
2. **"Rate limit exceeded"** - Implement caching and reduce call frequency
3. **"Network error"** - Check internet connection and CORS settings
4. **"No data returned"** - Verify symbol names and parameters

### Debug Mode
Enable debug logging:
```javascript
// Add to main.js
const DEBUG = true;
if (DEBUG) {
    console.log('API Keys configured:', Object.keys(this.apiKeys));
    console.log('Making API call to:', url);
}
```

## 🎯 Next Steps

1. **Get your API keys** from both services
2. **Configure the dashboard** with your keys
3. **Test the integration** using the provided test code
4. **Deploy to production** with proper environment variables
5. **Monitor usage** and adjust as needed

The dashboard is now ready to use with live data! 🚀