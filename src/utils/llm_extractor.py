import requests
import json
import re
from datetime import datetime
import time

class GroqExtractor:
    def __init__(self, api_key, model="llama3-70b-8192"):
        """
        Initialize Groq extractor
        
        Args:
            api_key: Your Groq API key from console.groq.com
            model: Model to use (llama3-70b-8192, llama3-8b-8192, mixtral-8x7b-32768)
        """
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Rate limiting (adjust based on your free tier limits)
        self.last_request_time = 0
        self.min_request_interval = 1  # 1 second between requests
        
    def extract_tournaments_from_html(self, html_content, sport, source_url):
        """Extract tournament data from HTML using Groq API"""
        
        
        # testing connextion
        test = self.test_connection()
        if test is False:
            raise ConnectionError("❌ Could not connect to Groq API")
            return []
        
        # Clean HTML for better processing
        cleaned_html = self.clean_html(html_content)
        
        # Create extraction prompt
        prompt = self.create_extraction_prompt(cleaned_html, sport, source_url)
        
        try:
            # Rate limiting
            self.rate_limit()
            
            response = self.query_groq(prompt)
            tournaments = self.parse_llm_response(response)
            
            print(f"✅ Extracted {len(tournaments)} tournaments from {source_url}")
            return tournaments
            
        except Exception as e:
            print(f"❌ Groq extraction error for {source_url}: {e}")
            return []
    
    def query_groq(self, prompt):
        """Send query to Groq API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a sports tournament data extraction expert. Extract only real, upcoming tournaments from the provided content. Return valid JSON only."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "model": self.model,
            "temperature": 0.1,
            "max_tokens": 2000,
            "top_p": 1,
            "stream": False
        }
        
        response = requests.post(self.base_url, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        return content
    
    def clean_html(self, html_content):
        """Clean HTML content for better processing"""
        # Remove scripts, styles, comments
        html_content = re.sub(r'<script.*?</script>', '', html_content, flags=re.DOTALL)
        html_content = re.sub(r'<style.*?</style>', '', html_content, flags=re.DOTALL)
        html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
        
        # Remove excessive whitespace
        html_content = re.sub(r'\s+', ' ', html_content)
        
        # Limit size for API token limits
        if len(html_content) > 6000:
            html_content = html_content[:6000] + "..."
        
        return html_content.strip()
    
    def create_extraction_prompt(self, html_content, sport, source_url):
        """Create extraction prompt for Groq"""
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        prompt = f"""
EXTRACT UPCOMING {sport.upper()} TOURNAMENTS from this HTML content.

STRICT RULES:
1. Only extract tournaments starting AFTER {current_date}
2. Classify level precisely: International, National, State, Regional, College, School, Club, Corporate, District
3. Return ONLY valid JSON array
4. If no tournaments found, return []

HTML CONTENT:
{html_content}

REQUIRED JSON FORMAT:
[
  {{
    "name": "Tournament Name",
    "level": "International",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD", 
    "official_url": "{source_url}",
    "streaming_links": "Platform1, Platform2",
    "image_url": "",
    "summary": "Brief description max 50 words",
    "location": "City, Country"
  }}
]

EXTRACT JSON ARRAY:"""
        
        return prompt
    
    def parse_llm_response(self, response_text):
        """Parse LLM JSON response"""
        try:
            # Clean response - remove any text before/after JSON
            response_text = response_text.strip()
            
            # Find JSON array
            json_match = re.search(r'\[.*?\]', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                tournaments = json.loads(json_str)
                
                # Validate tournaments
                valid_tournaments = []
                for tournament in tournaments:
                    if self.validate_tournament(tournament):
                        valid_tournaments.append(tournament)
                
                return valid_tournaments
            else:
                print("⚠️ No JSON array found in response")
                return []
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"Response was: {response_text[:200]}...")
            return []
        except Exception as e:
            print(f"❌ Response parsing error: {e}")
            return []
    
    def validate_tournament(self, tournament):
        """Validate tournament data"""
        if not isinstance(tournament, dict):
            return False
        
        # Check required fields
        required_fields = ['name', 'level', 'start_date']
        for field in required_fields:
            if not tournament.get(field):
                return False
        
        # Validate name length
        if len(tournament['name']) < 5 or len(tournament['name']) > 200:
            return False
        
        # Validate level
        valid_levels = ['International', 'National', 'State', 'Regional', 'College', 'School', 'Club', 'Corporate', 'District']
        if tournament['level'] not in valid_levels:
            tournament['level'] = 'Club'  # Default
        
        # Validate dates
        try:
            start_date = datetime.strptime(tournament['start_date'], '%Y-%m-%d')
            if start_date < datetime.now():
                return False  # Skip past tournaments
        except:
            return False
        
        return True
    
    def rate_limit(self):
        """Simple rate limiting to respect free tier limits"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            print(f"⏳ Rate limiting: sleeping {sleep_time:.1f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def test_connection(self):
        """Test Groq API connection"""
        try:
            response = self.query_groq("Hello, are you working? Reply with just 'Yes'")
            if 'yes' in response.lower():
                print(f"✅ Groq API working with model {self.model}")
                return True
            else:
                print("⚠️ Groq API responded but unexpectedly")
                return False
        except Exception as e:
            print(f"❌ Groq API test failed: {e}")
            print("💡 Check your API key and internet connection")
            return False