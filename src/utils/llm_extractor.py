import openai
import json
import re
from datetime import datetime, timedelta

class LLMExtractor:
    def __init__(self, api_key):
        openai.api_key = api_key
        
    def extract_tournaments_from_html(self, html_content, sport, source_url):
        """Extract tournament data from HTML using LLM"""
        
        # Clean HTML (remove scripts, styles, etc.)
        cleaned_html = self.clean_html(html_content)
        
        prompt = self.create_extraction_prompt(cleaned_html, sport, source_url)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sports tournament data extraction expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            result = response.choices[0].message.content
            tournaments = self.parse_llm_response(result)
            return tournaments
            
        except Exception as e:
            print(f"LLM extraction error: {e}")
            return []
    
    def clean_html(self, html_content):
        """Clean HTML content for better LLM processing"""
        # Remove scripts, styles, comments
        html_content = re.sub(r'<script.*?</script>', '', html_content, flags=re.DOTALL)
        html_content = re.sub(r'<style.*?</style>', '', html_content, flags=re.DOTALL)
        html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
        
        # Limit size (LLM token limits)
        if len(html_content) > 8000:
            html_content = html_content[:8000] + "..."
        
        return html_content
    
    def create_extraction_prompt(self, html_content, sport, source_url):
        """Create prompt for tournament extraction"""
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        prompt = f"""
Extract upcoming {sport} tournament information from this HTML content.

IMPORTANT RULES:
1. Only extract UPCOMING tournaments (starting after {current_date})
2. Focus on tournaments, competitions, matches, series
3. Ignore news articles, player info, or irrelevant content
4. Classify each tournament level as: International, National, State, Regional, College, School, Club, Corporate, District

HTML Content:
{html_content}

Return a JSON array with this exact format:
[
  {{
    "name": "Tournament Name",
    "level": "International|National|State|Regional|College|School|Club|Corporate|District",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "official_url": "{source_url}",
    "streaming_links": "Platform1, Platform2",
    "image_url": "image_url_if_found",
    "summary": "Brief description max 50 words",
    "location": "City, Country"
  }}
]

If no tournaments found, return empty array: []
"""
        return prompt
    
    def parse_llm_response(self, response_text):
        """Parse LLM JSON response"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                tournaments = json.loads(json_str)
                return tournaments
            else:
                print("No JSON found in LLM response")
                return []
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return []
    
    def summarize_tournament(self, tournament_text):
        """Generate tournament summary using LLM"""
        prompt = f"""
Summarize this tournament information in exactly 50 words or less:

{tournament_text}

Focus on: what type of tournament, who participates, when it happens, significance.
"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=100
            )
            return response.choices[0].message.content.strip()
        except:
            return "Tournament summary not available."