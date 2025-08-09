import requests
from bs4 import BeautifulSoup
import sqlite3
import json
from datetime import datetime
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    """Base class for all sport scrapers"""
    
    def __init__(self, sport_name):
        self.sport_name = sport_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_page(self, url):
        """Get webpage content"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def save_tournament(self, tournament_data):
        """Save tournament to database"""
        conn = sqlite3.connect('data/tournaments.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tournaments 
            (name, sport, level, start_date, end_date, official_url, 
             streaming_links, image_url, summary, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            tournament_data.get('name'),
            self.sport_name,
            tournament_data.get('level'),
            tournament_data.get('start_date'),
            tournament_data.get('end_date'),
            tournament_data.get('official_url'),
            tournament_data.get('streaming_links'),
            tournament_data.get('image_url'),
            tournament_data.get('summary'),
            tournament_data.get('location')
        ))
        
        conn.commit()
        conn.close()
        print(f"Saved: {tournament_data.get('name')}")
    
    def use_llm_to_extract(self, html_content, prompt_context=""):
        """Use LLM to extract tournament data from HTML"""
        # Placeholder - implement with OpenAI API
        # This would send HTML to GPT and get structured tournament data back
        pass
    
    @abstractmethod
    def scrape_international(self):
        """Scrape international tournaments"""
        pass
    
    @abstractmethod
    def scrape_national(self):
        """Scrape national tournaments"""
        pass
    
    @abstractmethod
    def scrape_local(self):
        """Scrape local tournaments"""
        pass
    
    def scrape_all(self):
        """Scrape all tournament levels"""
        print(f"Starting {self.sport_name} scraper...")
        
        try:
            self.scrape_international()
            self.scrape_national()
            self.scrape_local()
            print(f"{self.sport_name} scraping complete!")
        except Exception as e:
            print(f"Error in {self.sport_name} scraper: {e}")