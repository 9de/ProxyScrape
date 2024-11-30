# 🌐 ProxyScraperPlus

A high-performance, asynchronous proxy scraper with multi-source support and advanced verification capabilities.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-2.0-red.svg)

## ✨ Features

- 🚀 Asynchronous multi-source proxy scraping
- ✅ Built-in proxy verification system
- 📊 Detailed proxy information (country, speed, anonymity)
- 📁 Export to both TXT and Excel formats
- 🌍 Support for HTTP, SOCKS4, and SOCKS5 proxies
- 🛡️ Error handling and timeout management
- 🎯 Multiple proxy sources for increased reliability

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/9de/ProxyScraper.git
cd ProxyScraper
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

Run the script:
```bash
python proxy_scraper.py
```

Follow the interactive menu to:
1. Select proxy type (HTTP, SOCKS4, SOCKS5)
2. Set timeout value
3. Wait for the scraping and verification process
4. Find your proxies in the 'proxies' directory

## 📂 Output

The script creates two types of files in the 'proxies' directory:
- `{proxy_type}_proxies_{timestamp}.txt` - Simple list of proxies
- `{proxy_type}_proxies_{timestamp}.xlsx` - Detailed Excel file with additional information

## 🔍 Proxy Sources

- ProxyScrape API
- ProxyScan.io
- Proxy-List.download
- Additional sources can be easily added

## ⚙️ Configuration

Timeout values:
- Minimum: 5 seconds
- Maximum: 60 seconds
- Default: 10 seconds

## 🛠️ Technical Details

- Async/await implementation for concurrent operations
- Automatic proxy verification
- Country and speed detection
- Anonymity level checking
- Duplicate removal
- Comprehensive error handling

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!
