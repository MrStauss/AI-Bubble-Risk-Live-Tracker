# AI Bubble Health Dashboard - Project Outline

## File Structure

### Core HTML Pages
- **index.html** - Executive Summary Dashboard (Main Landing)
- **fundamentals.html** - Fundamentals vs Market Analysis
- **options.html** - Options & Crash Risk Analysis
- **exposure.html** - Sector & ETF Exposure Map
- **sentiment.html** - News & Narrative Analysis

### JavaScript Files
- **main.js** - Core dashboard functionality and data management
- **risk-calculator.js** - Bubble risk scoring algorithms
- **data-providers.js** - API integration and data fetching
- **visualizations.js** - Chart rendering and animations

### Resource Assets
- **resources/** - Images, icons, and media files
  - **hero-bg.jpg** - Dashboard background image
  - **risk-icons/** - Various risk level indicators
  - **company-logos/** - Ticker symbols and logos

## Page-by-Page Breakdown

### 1. Executive Summary (index.html)
**Purpose**: Primary dashboard with bubble risk overview
**Key Sections**:
- **Hero Area**: Large bubble risk score dial (0-100)
- **Regime Status**: Current market phase with trend indicators
- **Top 5 Drivers**: Expandable cards showing score influencers
- **7-Day Trend**: Interactive risk score timeline
- **Alert Panel**: Real-time notifications and threshold warnings
- **Watchlist Heatmap**: Live ticker risk visualization

**Interactive Elements**:
- Animated risk gauge with real-time updates
- Hover tooltips for detailed metric breakdowns
- Clickable driver cards revealing calculation logic
- Alert configuration modal

### 2. Fundamentals vs Market (fundamentals.html)
**Purpose**: Deep dive into fundamental analysis vs price action
**Key Sections**:
- **Ticker Analysis Grid**: Individual stock fundamental panels
- **FCF vs Price Charts**: Cash flow trend visualization
- **Divergence Alerts**: Automated warning system
- **Quality Scores**: Color-coded health indicators
- **Monetization Analysis**: Revenue vs cash flow correlation

**Interactive Elements**:
- Ticker selection dropdown with search
- Time period filters (1Y/3Y/5Y)
- Expandable company detail cards
- Sortable metrics table

### 3. Options & Crash Risk (options.html)
**Purpose**: Options market analysis and crash indicators
**Key Sections**:
- **IV Surface**: 3D implied volatility visualization
- **Skew Analysis**: Put/call imbalance indicators
- **Term Structure**: Front vs back month comparison
- **Put/Call Ratios**: Market sentiment through options flow
- **Crash Premium**: Dedicated hedging demand gauge

**Interactive Elements**:
- 3D chart rotation and zoom
- Expiration date selector
- Strike price range slider
- Historical volatility comparison

### 4. Sector & ETF Exposure Map (exposure.html)
**Purpose**: Portfolio and sector exposure analysis
**Key Sections**:
- **Exposure Spider Chart**: Multi-dimensional risk mapping
- **ETF Performance**: SOXL/SOXX/SOXS/TECL/XLK/TECS analysis
- **Beta Correlation**: AI stocks vs market relationship
- **Concentration Warnings**: Portfolio overlap detection
- **Leverage Indicators**: Froth measurement tools

**Interactive Elements**:
- Draggable spider chart nodes
- ETF comparison selector
- Correlation matrix heatmap
- Risk exposure calculator

### 5. News & Narrative Analysis (sentiment.html)
**Purpose**: Sentiment tracking and narrative detection
**Key Sections**:
- **Sentiment Timeline**: Historical sentiment tracking
- **Topic Clustering**: AI bubble, GPU shortage themes
- **Source Analysis**: Credibility-weighted news impact
- **Language Detection**: "Mania language" identification
- **Narrative Intensity**: Volume and repetition metrics

**Interactive Elements**:
- Sentiment filter controls
- Topic search and highlighting
- Source credibility toggle
- Time range selection

## Technical Implementation

### Data Integration Strategy
- **Primary**: Yahoo Finance API (yfinance) for real-time stock data
- **Secondary**: Alpha Vantage for technical indicators and fundamentals
- **Options**: CME Options Analytics for volatility data
- **News**: NewsAPI.org for sentiment analysis
- **Fallback**: Mock data for demonstration and testing

### Risk Scoring Algorithm
- **Fundamental Divergence (30%)**: Price vs cash flow analysis
- **Valuation Stretch (25%)**: P/E and market cap metrics
- **Leverage & Liquidity (20%)**: Credit spreads and breadth
- **Options Euphoria (15%)**: IV levels and skew analysis
- **Sentiment Crowding (10%)**: News and social sentiment

### Real-time Features
- **WebSocket Connections**: Live price updates
- **Server-Sent Events**: Risk score recalculation
- **Background Refresh**: Automated data updates
- **Alert System**: Threshold-based notifications

### Performance Optimization
- **Lazy Loading**: Progressive content loading
- **Data Caching**: Efficient storage and retrieval
- **Responsive Design**: Mobile-first approach
- **Error Handling**: Graceful degradation

## Development Tasks

### Phase 1: Core Dashboard
1. Create HTML structure and navigation
2. Implement basic risk scoring algorithm
3. Integrate Yahoo Finance API for stock data
4. Build executive summary dashboard
5. Add basic visualizations and animations

### Phase 2: Advanced Analytics
1. Develop options analysis page
2. Implement sentiment analysis integration
3. Create exposure mapping tools
4. Add historical data analysis
5. Build alert and notification system

### Phase 3: Polish & Optimization
1. Refine visual design and animations
2. Optimize performance and loading times
3. Add comprehensive error handling
4. Implement user customization features
5. Test across devices and browsers

This outline provides a comprehensive roadmap for building a sophisticated AI Bubble Health Dashboard that combines real-time data analysis with intuitive visual design.