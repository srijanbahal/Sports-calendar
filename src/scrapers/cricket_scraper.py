from .base_scraper import BaseScraper
from ..utils.groq_extractor import GroqExtractor
import os

class CricketScraper(BaseScraper):
    def __init__(self, groq_api_key=None):
        super().__init__("cricket")
        
        # Initialize Groq LLM
        if not groq_api_key:
            groq_api_key = os.getenv('GROQ_API_KEY')
        
        if not groq_api_key:
            raise ValueError("❌ GROQ_API_KEY not found! Get one from: https://console.groq.com/")
        
        self.llm = GroqExtractor(groq_api_key, model="llama3-70b-8192")
        
        # Test connection
        if not self.llm.test_connection():
            raise ConnectionError("❌ Could not connect to Groq API")
        
        # ALL cricket sources in one list - let LLM decide the level!
        self.all_sources = [
            # Major cricket sites (mix of all levels)
            'https://www.espncricinfo.com/series',
            'https://www.icc-cricket.com/fixtures-results',
            'https://www.bcci.tv/fixtures-results',
            'https://www.cricketworldcup.com/fixtures',
            'https://www.bcci.tv/domestic',
            
            # Regional/Local sources
            'https://www.universitycricket.com/tournaments',
            'https://www.cricketacademy.com/upcoming-tournaments',
            
            # You can add more sources here - LLM will classify each tournament properly
        ]
    
    def scrape_all_tournaments(self):
        """Scrape ALL cricket tournaments from all sources - let LLM classify levels"""
        print("🏏 Starting comprehensive cricket tournament scraping...")
        
        total_tournaments_found = 0
        processed_sources = 0
        
        for url in self.all_sources:
            try:
                print(f"📡 Fetching: {url}")
                soup = self.get_page(url)
                
                if soup:
                    html_content = str(soup)
                    tournaments = self.llm.extract_tournaments_from_html(
                        html_content, "cricket", url
                    )
                    
                    # Save ALL tournaments - LLM already classified them correctly!
                    for tournament in tournaments:
                        if self.validate_tournament_data(tournament):
                            self.save_tournament(tournament)
                            total_tournaments_found += 1
                            print(f"  ✅ Saved: {tournament['name']} ({tournament['level']})")
                    
                    processed_sources += 1
                    print(f"  📊 Found {len(tournaments)} tournaments from this source")
                    
                else:
                    print(f"  ⚠️ Could not fetch {url}")
                    
            except Exception as e:
                print(f"  ❌ Error scraping {url}: {e}")
        
        print(f"\n🎉 SCRAPING COMPLETE!")
        print(f"📈 Processed {processed_sources} sources")
        print(f"🏆 Found {total_tournaments_found} cricket tournaments total")
        
        # Show breakdown by level
        self.show_tournament_breakdown()
    
    def validate_tournament_data(self, tournament):
        """Basic validation - but trust LLM classification"""
        
        # Check essential fields exist
        if not tournament.get('name') or len(tournament.get('name', '')) < 3:
            print(f"  ⚠️ Skipping tournament with invalid name: {tournament}")
            return False
        
        # Check if level is reasonable (but don't override LLM decision)
        valid_levels = ['International', 'National', 'State', 'Regional', 'College', 'School', 'Club', 'Corporate', 'District']
        if tournament.get('level') not in valid_levels:
            print(f"  ⚠️ Unusual level '{tournament.get('level')}' for: {tournament.get('name')}")
            # Don't reject - just log it
        
        return True
    
    def show_tournament_breakdown(self):
        """Show breakdown of tournaments by level"""
        import sqlite3
        
        conn = sqlite3.connect('data/tournaments.db')
        cursor = conn.cursor()
        
        print(f"\n📊 CRICKET TOURNAMENTS BY LEVEL:")
        
        breakdown = cursor.execute('''
            SELECT level, COUNT(*) as count 
            FROM tournaments 
            WHERE sport = 'cricket' 
            GROUP BY level 
            ORDER BY count DESC
        ''').fetchall()
        
        for level, count in breakdown:
            print(f"  🎯 {level}: {count} tournaments")
        
        conn.close()
    
    # Override the old methods to use the new approach
    def scrape_international(self):
        """Legacy method - redirects to comprehensive scraping"""
        print("🔄 Redirecting to comprehensive scraping...")
        self.scrape_all_tournaments()
    
    def scrape_national(self):
        """Legacy method - redirects to comprehensive scraping"""
        print("🔄 Using comprehensive scraping (no need for separate national scraping)")
        pass
    
    def scrape_local(self):
        """Legacy method - redirects to comprehensive scraping"""  
        print("🔄 Using comprehensive scraping (no need for separate local scraping)")
        pass
    
    def scrape_all(self):
        """Main scraping method"""
        self.scrape_all_tournaments()
    
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
                
                print(f"\n📊 TEST RESULTS:")
                print(f"🏆 Found {len(tournaments)} tournaments")
                
                # Show breakdown by level
                level_counts = {}
                for t in tournaments:
                    level = t.get('level', 'Unknown')
                    level_counts[level] = level_counts.get(level, 0) + 1
                
                for level, count in level_counts.items():
                    print(f"  {level}: {count} tournaments")
                
                print(f"\n📝 Sample tournaments:")
                for i, t in enumerate(tournaments[:3]):
                    print(f"  {i+1}. {t.get('name')} ({t.get('level')}) - {t.get('start_date')}")
                
                return tournaments
            else:
                print("❌ Could not fetch test URL")
                return []
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return []

# Usage
if __name__ == "__main__":
    try:
        scraper = CricketScraper()
        
        # Test first
        scraper.quick_test()
        
        # Full scraping - ONE method does it all!
        # scraper.scrape_all_tournaments()
        
    except Exception as e:
        print(f"❌ Scraper setup failed: {e}")