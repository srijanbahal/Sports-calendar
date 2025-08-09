from base_scraper import BaseScraper
from ..utils.llm_extractor import GroqExtractor
import os

class CricketScraper(BaseScraper):
    def __init__(self, groq_api_key=None):
        super().__init__("cricket")
        
        # Initialize Groq LLM
        if not groq_api_key:
            groq_api_key = os.getenv('GROQ_API_KEY')
        
        if not groq_api_key:
            raise ValueError("❌ GROQ_API_KEY not found! Get one from: https://console.groq.com/")
        
        # Use llama3-70b-8192 for best accuracy (you can change to llama3-8b-8192 for speed)
        self.llm = GroqExtractor(groq_api_key, model="llama3-70b-8192")
        
        # Test connection
        if not self.llm.test_connection():
            raise ConnectionError("❌ Could not connect to Groq API")
        
        # Cricket tournament sources - REAL websites with tournament info
        self.sources = {
            'international': [
                'https://www.espncricinfo.com/series',
                'https://www.icc-cricket.com/fixtures-results',
                'https://www.bcci.tv/fixtures-results',
                'https://www.cricketworldcup.com/fixtures'
            ],
            'national': [
                'https://www.bcci.tv/domestic',
                'https://www.espncricinfo.com/ci/engine/series/index.html?view=league',
                'https://www.cricketworldcup.com/league'
            ],
            'local': [
                'https://www.universitycricket.com/tournaments',
                'https://www.cricketacademy.com/upcoming-tournaments',
                # Add more local sources as you find them
            ]
        }
    
    def scrape_international(self):
        """Scrape international cricket tournaments"""
        print("🏏 Scraping international cricket tournaments...")
        
        tournaments_found = 0
        
        for url in self.sources['international']:
            try:
                print(f"📡 Fetching: {url}")
                soup = self.get_page(url)
                
                if soup:
                    html_content = str(soup)
                    tournaments = self.llm.extract_tournaments_from_html(
                        html_content, "cricket", url
                    )
                    
                    # Filter for international tournaments
                    for tournament in tournaments:
                        if tournament.get('level') in ['International']:
                            self.save_tournament(tournament)
                            tournaments_found += 1
                            
                else:
                    print(f"⚠️ Could not fetch {url}")
                    
            except Exception as e:
                print(f"❌ Error scraping {url}: {e}")
        
        print(f"✅ Found {tournaments_found} international cricket tournaments")
    
    def scrape_national(self):
        """Scrape national cricket tournaments"""
        print("🏏 Scraping national cricket tournaments...")
        
        tournaments_found = 0
        
        for url in self.sources['national']:
            try:
                print(f"📡 Fetching: {url}")
                soup = self.get_page(url)
                
                if soup:
                    html_content = str(soup)
                    tournaments = self.llm.extract_tournaments_from_html(
                        html_content, "cricket", url
                    )
                    
                    # Filter for national/state tournaments
                    for tournament in tournaments:
                        if tournament.get('level') in ['National', 'State', 'Regional']:
                            self.save_tournament(tournament)
                            tournaments_found += 1
                            
            except Exception as e:
                print(f"❌ Error scraping {url}: {e}")
        
        print(f"✅ Found {tournaments_found} national cricket tournaments")
    
    def scrape_local(self):
        """Scrape local cricket tournaments"""
        print("🏏 Scraping local cricket tournaments...")
        
        tournaments_found = 0
        
        # Local cricket sources (you can add more)
        local_sources = [
            'https://www.cricketacademy.com/tournaments',
            'https://www.universitysports.com/cricket',
            # Add university websites, local cricket clubs, etc.
        ]
        
        for url in local_sources:
            try:
                print(f"📡 Fetching: {url}")
                soup = self.get_page(url)
                
                if soup:
                    html_content = str(soup)
                    tournaments = self.llm.extract_tournaments_from_html(
                        html_content, "cricket", url
                    )
                    
                    # Filter for local tournaments
                    for tournament in tournaments:
                        if tournament.get('level') in ['College', 'School', 'Club', 'Corporate', 'District']:
                            self.save_tournament(tournament)
                            tournaments_found += 1
                            
            except Exception as e:
                print(f"❌ Error scraping {url}: {e}")
        
        print(f"✅ Found {tournaments_found} local cricket tournaments")
    
    def quick_test(self):
        """Quick test with one URL"""
        test_url = "https://www.espncricinfo.com/series"
        print(f"🧪 Testing cricket scraper with: {test_url}")
        
        try:
            soup = self.get_page(test_url)
            if soup:
                html_content = str(soup)
                tournaments = self.llm.extract_tournaments_from_html(
                    html_content, "cricket", test_url
                )
                
                print(f"📊 Test result: Found {len(tournaments)} tournaments")
                for t in tournaments[:3]:  # Show first 3
                    print(f"  🏆 {t.get('name')} ({t.get('level')})")
                
                return tournaments
            else:
                print("❌ Could not fetch test URL")
                return []
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return []

# Usage examples
if __name__ == "__main__":
    # Make sure to set your API key first:
    # export GROQ_API_KEY="your_key_here"
    
    try:
        scraper = CricketScraper()
        
        # Quick test first
        scraper.quick_test()
        
        # Full scraping
        # scraper.scrape_all()
        
    except Exception as e:
        print(f"❌ Scraper setup failed: {e}")
        print("💡 Make sure to:")
        print("   1. Get API key from: https://console.groq.com/")
        print("   2. Set: export GROQ_API_KEY='your_key_here'")