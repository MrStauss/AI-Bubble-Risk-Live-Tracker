            const data = await response.json();
            
            return this.processNewsData(data);
        } catch (error) {
            console.error('Error fetching news from NewsData.io:', error);
            return this.getMockNewsData(query);
        }
    }

    processNewsData(data) {
        if (!data.results || data.results.length === 0) {
            return { sentiment: 0, intensity: 0, articleCount: 0, articles: [] };
        }

        let totalSentiment = 0;
        let articles = [];

        data.results.forEach(article => {
            // Simple sentiment analysis based on keywords
            const sentiment = this.analyzeSentiment(article.title + ' ' + (article.description || ''));
            totalSentiment += sentiment;
            
            articles.push({
                title: article.title,
                description: article.description,
                sentiment: sentiment,
                source: article.source_id,
                publishedAt: article.pubDate,
                url: article.link
            });
        });

        return {
            sentiment: totalSentiment / articles.length,
            intensity: articles.length / 50, // Normalize to 0-1
            articleCount: articles.length,
            articles: articles
        };
    }

    analyzeSentiment(text) {
        const positiveWords = ['growth', 'surge', 'boom', 'strong', 'excellent', 'outstanding', 'revolutionary', 'breakthrough', 'dominance'];
        const negativeWords = ['concern', 'warning', 'bubble', 'risk', 'decline', 'fall', 'crash', 'scarcity', 'shortage'];
        
        const words = text.toLowerCase().split(/\s+/);
        let score = 0;
        
        words.forEach(word => {
            if (positiveWords.some(pw => word.includes(pw))) score += 0.1;
            if (negativeWords.some(nw => word.includes(nw))) score -= 0.1;
        });
        
        return Math.max(-1, Math.min(1, score));
    }

    getMockNewsData(query) {
        // Mock data for demonstration when API keys are not available
        return {
            sentiment: Math.random() * 2 - 1,
            intensity: Math.random(),
            articleCount: Math.floor(Math.random() * 100),
            articles: [
                {
                    title: `AI Market Shows Strong Growth Potential`,
                    description: `Latest analysis indicates continued expansion in AI sector driven by increased demand.`,
                    sentiment: 0.7,
                    source: 'Financial Times',
                    publishedAt: new Date().toISOString(),
                    url: '#'
                },
                {
                    title: `Analysts Express Concern Over AI Valuations`,
                    description: `Some market experts warn that current AI stock prices may not be sustainable long-term.`,
                    sentiment: -0.3,
                    source: 'Wall Street Journal',
                    publishedAt: new Date().toISOString(),
                    url: '#'
                }
            ]
        };
    }

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
}

// Configuration Panel Management
class ConfigPanel {
    constructor() {
        this.isVisible = false;
        this.createConfigPanel();
        // Wait for DOM to be fully loaded before attaching listeners
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.attachEventListeners());
        } else {
            this.attachEventListeners();
        }
    }

    createConfigPanel() {
        // Create configuration panel HTML
        const panelHTML = `
            <div id="config-panel" class="fixed top-20 right-6 z-50 glass-card rounded-2xl p-6 w-80 transform translate-x-full transition-transform duration-300">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-bold">API Configuration</h3>
                    <button id="close-config" class="text-gray-400 hover:text-white">✕</button>
                </div>
                
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium mb-2">Alpha Vantage API Key</label>
                        <input type="password" id="alpha-vantage-key" placeholder="Enter your API key" 
                               class="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-sm text-white">
                        <div class="mt-1 text-xs text-gray-400">Get free key from alphavantage.co</div>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium mb-2">NewsData.io API Key</label>
                        <input type="password" id="newsdata-key" placeholder="Enter your API key" 
                               class="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-sm text-white">
                        <div class="mt-1 text-xs text-gray-400">Get free key from newsdata.io</div>
                    </div>
                    
                    <div class="flex space-x-2">
                        <button id="save-config" class="flex-1 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg text-sm transition-colors">
                            Save & Test
                        </button>
                        <button id="test-apis" class="flex-1 bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg text-sm transition-colors">
                            Test APIs
                        </button>
                    </div>
                    
                    <div id="config-status" class="text-xs text-center"></div>
                </div>
                
                <div class="mt-6 pt-4 border-t border-gray-700">
                    <h4 class="text-sm font-medium mb-2">Quick Links</h4>
                    <div class="space-y-1">
                        <a href="https://alphavantage.co" target="_blank" class="block text-xs text-blue-400 hover:text-blue-300">🔄 Get Alpha Vantage API Key</a>
                        <a href="https://newsdata.io" target="_blank" class="block text-xs text-blue-400 hover:text-blue-300">🔄 Get NewsData.io API Key</a>
                        <a href="API_CONFIGURATION_GUIDE.md" target="_blank" class="block text-xs text-gray-400 hover:text-gray-300">📖 View Full Guide</a>
                    </div>
                </div>
            </div>
            
            <!-- Configuration Toggle Button -->
            <button id="config-toggle" class="fixed top-24 right-6 z-50 glass-card rounded-full p-3 hover:bg-blue-600/20 transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
            </button>
        `;
        
        document.body.insertAdjacentHTML('beforeend', panelHTML);
    }

    attachEventListeners() {
        // Toggle panel visibility
        const toggleBtn = document.getElementById('config-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                this.togglePanel();
            });
        }

        // Close panel
        const closeBtn = document.getElementById('close-config');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                this.hidePanel();
            });
        }

        // Save configuration
        const saveBtn = document.getElementById('save-config');
        if (saveBtn) {
            saveBtn.addEventListener('click', () => {
                this.saveConfiguration();
            });
        }

        // Test APIs
        const testBtn = document.getElementById('test-apis');
        if (testBtn) {
            testBtn.addEventListener('click', () => {
                this.testAPIs();
            });
        }

        // Auto-save on input change
        const alphaInput = document.getElementById('alpha-vantage-key');
        if (alphaInput) {
            alphaInput.addEventListener('change', () => {
                this.saveConfiguration();
            });
        }

        const newsInput = document.getElementById('newsdata-key');
        if (newsInput) {
            newsInput.addEventListener('change', () => {
                this.saveConfiguration();
            });
        }
    }

    togglePanel() {
        const panel = document.getElementById('config-panel');
        if (!panel) return;
        
        this.isVisible = !this.isVisible;
        
        if (this.isVisible) {
            panel.classList.remove('translate-x-full');
            this.loadSavedKeys();
        } else {
            panel.classList.add('translate-x-full');
        }
    }

    hidePanel() {
        const panel = document.getElementById('config-panel');
        if (!panel) return;
        
        panel.classList.add('translate-x-full');
        this.isVisible = false;
    }

    saveConfiguration() {
        const alphaVantageKey = document.getElementById('alpha-vantage-key')?.value;
        const newsDataKey = document.getElementById('newsdata-key')?.value;

        // Save to localStorage
        if (alphaVantageKey) {
            localStorage.setItem('alphaVantageKey', alphaVantageKey);
            if (window.dataProvider) {
                window.dataProvider.setApiKey('alphaVantage', alphaVantageKey);
            }
        }

        if (newsDataKey) {
            localStorage.setItem('newsDataKey', newsDataKey);
            if (window.dataProvider) {
                window.dataProvider.setApiKey('newsData', newsDataKey);
            }
        }

        this.updateStatus('Configuration saved successfully!', 'green');
    }

    loadSavedKeys() {
        const alphaVantageKey = localStorage.getItem('alphaVantageKey');
        const newsDataKey = localStorage.getItem('newsDataKey');

        const alphaInput = document.getElementById('alpha-vantage-key');
        if (alphaInput && alphaVantageKey) {
            alphaInput.value = alphaVantageKey;
        }

        const newsInput = document.getElementById('newsdata-key');
        if (newsInput && newsDataKey) {
            newsInput.value = newsDataKey;
        }
    }

    async testAPIs() {
        this.updateStatus('Testing APIs...', 'yellow');

        try {
            // Test Alpha Vantage
            if (window.dataProvider && window.dataProvider.apiKeys.alphaVantage !== 'YOUR_ALPHA_VANTAGE_KEY') {
                const stockData = await window.dataProvider.getAlphaVantageQuote('NVDA');
                if (stockData) {
                    console.log('✅ Alpha Vantage API working:', stockData);
                } else {
                    console.warn('⚠️ Alpha Vantage API test failed');
                }
            }

            // Test NewsData.io
            if (window.dataProvider && window.dataProvider.apiKeys.newsData !== 'YOUR_NEWSDATA_API_KEY') {
                const newsData = await window.dataProvider.getNewsDataFromNewsData('NVIDIA stock');
                if (newsData && newsData.articleCount > 0) {
                    console.log('✅ NewsData.io API working:', newsData);
                } else {
                    console.warn('⚠️ NewsData.io API test failed');
                }
            }

            this.updateStatus('API tests completed! Check console for details.', 'green');
        } catch (error) {
            console.error('❌ API test error:', error);
            this.updateStatus('API test failed. Check console for details.', 'red');
        }
    }

    updateStatus(message, color) {
        const statusElement = document.getElementById('config-status');
        if (statusElement) {
            statusElement.textContent = message;
            statusElement.className = `text-xs text-center text-${color}-400`;
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new AIBubbleDashboard();
    const dataProvider = new DataProvider();
    const configPanel = new ConfigPanel();
    
    // Make dashboard globally accessible for debugging
    window.dashboard = dashboard;
    window.dataProvider = dataProvider;
    window.configPanel = configPanel;

    // Load saved API keys
    const alphaVantageKey = localStorage.getItem('alphaVantageKey');
    const newsDataKey = localStorage.getItem('newsDataKey');
    
    if (alphaVantageKey) {
        dataProvider.setApiKey('alphaVantage', alphaVantageKey);
    }
    
    if (newsDataKey) {
        dataProvider.setApiKey('newsData', newsDataKey);
    }

    // Handle window resize for charts
    window.addEventListener('resize', () => {
        if (dashboard.riskGaugeChart) {
            dashboard.riskGaugeChart.resize();
        }
        if (dashboard.trendChart) {
            dashboard.trendChart.resize();
        }
    });

    // Add click handlers for navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            if (link.getAttribute('href') !== 'index.html') {
                e.preventDefault();
                alert('Page under construction. Coming soon!');
            }
        });
    });

    // Add click handlers for ticker items
    document.querySelectorAll('.ticker-item').forEach(item => {
        item.addEventListener('click', () => {
            const symbol = item.querySelector('.text-lg').textContent;
            alert(`${symbol} detailed analysis coming soon!`);
        });
    });
});

    attachEventListeners() {
        // Toggle panel visibility
        document.getElementById('config-toggle').addEventListener('click', () => {
            this.togglePanel();
        });

        // Close panel
        document.getElementById('close-config').addEventListener('click', () => {
            this.hidePanel();
        });

        // Save configuration
        document.getElementById('save-config').addEventListener('click', () => {
            this.saveConfiguration();
        });

        // Test APIs
        document.getElementById('test-apis').addEventListener('click', () => {
            this.testAPIs();
        });

        // Auto-save on input change
        document.getElementById('alpha-vantage-key').addEventListener('change', () => {
            this.saveConfiguration();
        });

        document.getElementById('newsdata-key').addEventListener('change', () => {
            this.saveConfiguration();
        });
    }

    togglePanel() {
        const panel = document.getElementById('config-panel');
        this.isVisible = !this.isVisible;
        
        if (this.isVisible) {
            panel.classList.remove('translate-x-full');
            this.loadSavedKeys();
        } else {
            panel.classList.add('translate-x-full');
        }
    }

    hidePanel() {
        const panel = document.getElementById('config-panel');
        panel.classList.add('translate-x-full');
        this.isVisible = false;
    }

    saveConfiguration() {
        const alphaVantageKey = document.getElementById('alpha-vantage-key').value;
        const newsDataKey = document.getElementById('newsdata-key').value;

        // Save to localStorage
        if (alphaVantageKey) {
            localStorage.setItem('alphaVantageKey', alphaVantageKey);
            if (window.dataProvider) {
                window.dataProvider.setApiKey('alphaVantage', alphaVantageKey);
            }
        }

        if (newsDataKey) {
            localStorage.setItem('newsDataKey', newsDataKey);
            if (window.dataProvider) {
                window.dataProvider.setApiKey('newsData', newsDataKey);
            }
        }

        this.updateStatus('Configuration saved successfully!', 'green');
    }

    loadSavedKeys() {
        const alphaVantageKey = localStorage.getItem('alphaVantageKey');
        const newsDataKey = localStorage.getItem('newsDataKey');

        if (alphaVantageKey) {
            document.getElementById('alpha-vantage-key').value = alphaVantageKey;
        }

        if (newsDataKey) {
            document.getElementById('newsdata-key').value = newsDataKey;
        }
    }

    async testAPIs() {
        this.updateStatus('Testing APIs...', 'yellow');

        try {
            // Test Alpha Vantage
            if (window.dataProvider && window.dataProvider.apiKeys.alphaVantage !== 'YOUR_ALPHA_VANTAGE_KEY') {
                const stockData = await window.dataProvider.getAlphaVantageQuote('NVDA');
                if (stockData) {
                    console.log('✅ Alpha Vantage API working:', stockData);
                } else {
                    console.warn('⚠️ Alpha Vantage API test failed');
                }
            }

            // Test NewsData.io
            if (window.dataProvider && window.dataProvider.apiKeys.newsData !== 'YOUR_NEWSDATA_API_KEY') {
                const newsData = await window.dataProvider.getNewsDataFromNewsData('NVIDIA stock');
                if (newsData && newsData.articleCount > 0) {
                    console.log('✅ NewsData.io API working:', newsData);
                } else {
                    console.warn('⚠️ NewsData.io API test failed');
                }
            }

            this.updateStatus('API tests completed! Check console for details.', 'green');
        } catch (error) {
            console.error('❌ API test error:', error);
            this.updateStatus('API test failed. Check console for details.', 'red');
        }
    }

    updateStatus(message, color) {
        const statusElement = document.getElementById('config-status');
        statusElement.textContent = message;
        statusElement.className = `text-xs text-center text-${color}-400`;
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new AIBubbleDashboard();
    const dataProvider = new DataProvider();
    const configPanel = new ConfigPanel();
    
    // Make dashboard globally accessible for debugging
    window.dashboard = dashboard;
    window.dataProvider = dataProvider;
    window.configPanel = configPanel;

    // Load saved API keys
    const alphaVantageKey = localStorage.getItem('alphaVantageKey');
    const newsDataKey = localStorage.getItem('newsDataKey');
    
    if (alphaVantageKey) {
        dataProvider.setApiKey('alphaVantage', alphaVantageKey);
    }
    
    if (newsDataKey) {
        dataProvider.setApiKey('newsData', newsDataKey);
    }

    // Handle window resize for charts
    window.addEventListener('resize', () => {
        if (dashboard.riskGaugeChart) {
            dashboard.riskGaugeChart.resize();
        }
        if (dashboard.trendChart) {
            dashboard.trendChart.resize();
        }
    });

    // Add click handlers for navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            if (link.getAttribute('href') !== 'index.html') {
                e.preventDefault();
                alert('Page under construction. Coming soon!');
            }
        });
    });

    // Add click handlers for ticker items
    document.querySelectorAll('.ticker-item').forEach(item => {
        item.addEventListener('click', () => {
            const symbol = item.querySelector('.text-lg').textContent;
            alert(`${symbol} detailed analysis coming soon!`);
        });
    });
});