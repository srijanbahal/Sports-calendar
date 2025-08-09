from .base_scraper import BaseScraper
from ..utils.llm_extractor import LLMExtractor
import os

class CricketScraper(BaseScraper):
    def __init__(self):
        super().__init__("cricket")
        # Initialize LLM (you'll need OpenAI API key)
        api_key = os.getenv('OPENAI_API_KEY', 'your-api-key-here')
        self.llm = LLMExtractor(api_key)
        
        # Cricket tournament sources
        self.sources = {
            'international': [
                'https://www.espncricinfo.com/series',
                'https://www.icc-cricket.com/fixtures-results',
                'https://www.cricketworldcup.com/fixtures'
            ],
            'national': [
                'https://www.bcci.tv/domestic',
                'https://www.espncricinfo.com/ci/engine/series/index.html?view=league'
            ],
            'local': [
                'https://www.cricketworldcup.com/league',
                # Add more local cricket websites
            ]
        }
    
    def scrape_international(self):
        """Scrape international cricket tournaments"""
        print("Scraping international cricket tournaments...")
        
        for url in self.sources['international']:
            try:
                soup = self.get_page(url)
                if soup:
                    html_content = str(soup)
                    tournaments = self.llm.extract_tournaments_from_html(
                        html_content, "cricket", url
                    )
                    
                    for tournament in tournaments:
                        if tournament.get('level') in ['International']:
                            self.save_tournament(tournament)
                            
            except Exception as e:
                print(f"Error scraping {url}: {e}")
    
    def scrape_national(self):
        """Scrape national cricket tournaments"""
        print("Scraping national cricket tournaments...")
        
        for url in self.sources['national']:
            try:
                soup = self.get_page(url)
                if soup:
                    html_content = str(soup)
                    tournaments = self.llm.extract_tournaments_from_html(
                        html_content, "cricket", url
                    )
                    
                    for tournament in tournaments:
                        if tournament.get('level') in ['National', 'State']:
                            self.save_tournament(tournament)
                            
            except Exception as e:
                print(f"Error scraping {url}: {e}")
    
    def scrape_local(self):
        """Scrape local cricket tournaments"""
        print("Scraping local cricket tournaments...")
        
        # Add specific logic for local tournaments
        # University websites, local cricket associations, etc.
        local_urls = [
            'https://example-university.edu/sports/cricket',
            # Add more local sources
        ]
        
        for url in local_urls:
            try:
                soup = self.get_page(url)
                if soup:
                    html_content = str(soup)
                    tournaments = self.llm.extract_tournaments_from_html(
                        html_content, "cricket", url
                    )
                    
                    for tournament in tournaments:
                        if tournament.get('level') in ['College', 'School', 'Club', 'Corporate']:
                            self.save_tournament(tournament)
                            
            except Exception as e:
                print(f"Error scraping {url}: {e}")
    
    def scrape_specific_tournament(self, tournament_url):
        """Scrape a specific tournament page for detailed info"""
        soup = self.get_page(tournament_url)
        if soup:
            html_content = str(soup)
            tournaments = self.llm.extract_tournaments_from_html(
                html_content, "cricket", tournament_url
            )
            return tournaments
        return []

# Usage example
if __name__ == "__main__":
    scraper = CricketScraper()
    scraper.scrape_all()