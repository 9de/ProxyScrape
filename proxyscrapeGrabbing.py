import asyncio
import aiohttp
import colorama
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

# Initialize colorama
colorama.init(autoreset=True)

@dataclass
class ProxySource:
    name: str
    url: str
    type: str

class ProxyScraperPlus:
    def __init__(self):
        self.proxy_sources = {
            'http': [
                ProxySource('proxyscrape', 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout={timeout}&country=all&ssl=all&anonymity=all', 'http'),
                ProxySource('proxyscan', 'https://www.proxyscan.io/download?type=http&timeout={timeout}', 'http'),
                ProxySource('proxylist', 'https://www.proxy-list.download/api/v1/get?type=http&timeout={timeout}', 'http')
            ],
            'socks4': [
                ProxySource('proxyscrape', 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout={timeout}&country=all', 'socks4'),
                ProxySource('proxyscan', 'https://www.proxyscan.io/download?type=socks4&timeout={timeout}', 'socks4')
            ],
            'socks5': [
                ProxySource('proxyscrape', 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout={timeout}&country=all', 'socks5'),
                ProxySource('proxyscan', 'https://www.proxyscan.io/download?type=socks5&timeout={timeout}', 'socks5')
            ]
        }
        self.output_dir = Path('proxies')
        self.output_dir.mkdir(exist_ok=True)

    async def fetch_proxies(self, session: aiohttp.ClientSession, source: ProxySource, timeout: int) -> List[str]:
        """Fetch proxies from a single source"""
        try:
            url = source.url.format(timeout=timeout)
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    content = await response.text()
                    proxies = [p.strip() for p in content.split('\n') if p.strip()]
                    print(colorama.Fore.GREEN + f"Successfully fetched {len(proxies)} proxies from {source.name}")
                    return proxies
                else:
                    print(colorama.Fore.YELLOW + f"Failed to fetch from {source.name}: HTTP {response.status}")
                    return []
        except Exception as e:
            print(colorama.Fore.RED + f"Error fetching from {source.name}: {str(e)}")
            return []

    async def verify_proxy(self, session: aiohttp.ClientSession, proxy: str, proxy_type: str) -> Optional[Dict]:
        """Verify if a proxy is working"""
        try:
            proxy_url = f"{proxy_type}://{proxy}"
            async with session.get('http://ip-api.com/json', proxy=proxy_url, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'proxy': proxy,
                        'country': data.get('country', 'Unknown'),
                        'speed': response.elapsed.total_seconds(),
                        'anonymity': 'Elite' if 'proxy' not in str(data) else 'Anonymous'
                    }
        except:
            return None

    async def process_proxy_type(self, proxy_type: str, timeout: int):
        """Process all sources for a specific proxy type"""
        async with aiohttp.ClientSession() as session:
            sources = self.proxy_sources[proxy_type]
            tasks = [self.fetch_proxies(session, source, timeout) for source in sources]
            proxy_lists = await asyncio.gather(*tasks)
            
            # Combine and deduplicate proxies
            all_proxies = list(set([p for sublist in proxy_lists for p in sublist if p]))
            
            # Verify proxies concurrently
            verify_tasks = [self.verify_proxy(session, proxy, proxy_type) for proxy in all_proxies]
            results = await asyncio.gather(*verify_tasks)
            valid_proxies = [r for r in results if r is not None]
            
            # Save results
            self.save_proxies(valid_proxies, proxy_type)
            return valid_proxies

    def save_proxies(self, proxies: List[Dict], proxy_type: str):
        """Save proxies to both text and Excel formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save to text file
        txt_path = self.output_dir / f'{proxy_type}_proxies_{timestamp}.txt'
        with open(txt_path, 'w') as f:
            for proxy in proxies:
                f.write(f"{proxy['proxy']}\n")
                
        # Save to Excel with additional information
        if proxies:
            df = pd.DataFrame(proxies)
            excel_path = self.output_dir / f'{proxy_type}_proxies_{timestamp}.xlsx'
            df.to_excel(excel_path, index=False)
            
        print(colorama.Fore.GREEN + f"Saved {len(proxies)} valid {proxy_type} proxies")

    @staticmethod
    def display_banner():
        banner = """
        ╔══════════════════════════════════════════════╗
        ║             Enhanced Proxy Scraper           ║
        ║                                             ║
        ║  Features:                                  ║
        ║  - Multi-source proxy scraping              ║
        ║  - Proxy verification                       ║
        ║  - Excel export with details                ║
        ║  - Async processing                         ║
        ╚══════════════════════════════════════════════╝
        """
        print(colorama.Fore.CYAN + banner)

async def main():
    scraper = ProxyScraperPlus()
    scraper.display_banner()
    
    while True:
        try:
            print(colorama.Fore.YELLOW + "\nSelect proxy type:")
            print("[1] HTTP")
            print("[2] SOCKS4")
            print("[3] SOCKS5")
            print("[4] Exit")
            
            choice = input(colorama.Fore.WHITE + "Enter your choice (1-4): ")
            
            if choice == '4':
                break
                
            if choice not in ['1', '2', '3']:
                print(colorama.Fore.RED + "Invalid choice!")
                continue
                
            proxy_type = {
                '1': 'http',
                '2': 'socks4',
                '3': 'socks5'
            }[choice]
            
            timeout = input(colorama.Fore.YELLOW + "Enter timeout in seconds (5-60): ")
            try:
                timeout = int(timeout)
                if not 5 <= timeout <= 60:
                    raise ValueError
            except ValueError:
                print(colorama.Fore.RED + "Invalid timeout! Using default of 10 seconds")
                timeout = 10
            
            print(colorama.Fore.CYAN + "\nFetching and verifying proxies...")
            valid_proxies = await scraper.process_proxy_type(proxy_type, timeout)
            
            print(colorama.Fore.GREEN + f"\nFound {len(valid_proxies)} valid {proxy_type} proxies!")
            input(colorama.Fore.YELLOW + "\nPress Enter to continue...")
            
        except Exception as e:
            print(colorama.Fore.RED + f"An error occurred: {str(e)}")
            input("Press Enter to continue...")

if __name__ == '__main__':
    asyncio.run(main())
