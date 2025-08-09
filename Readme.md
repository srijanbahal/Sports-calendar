# Sports Tournament Calendar

A GenAI-powered solution to generate an up-to-date calendar of sports tournaments across multiple sports and competition levels.

## Sports Covered
- Cricket
- Football  
- Basketball
- Badminton
- Chess

## Competition Levels
- Corporate
- School
- College/University
- Club/Academy
- District
- State
- Zonal/Regional
- National
- International

## Project Structure
```
sports-tournament-calendar/
├── src/
│   ├── scrapers/          # Web scrapers for different sports
│   ├── database/          # Database initialization and utilities
│   ├── api/              # Flask API application
│   └── utils/            # Utility functions
├── data/                 # SQLite database and raw data
├── ui/                   # Frontend mockup
├── output/              # Generated CSV/JSON files
├── requirements.txt     # Python dependencies
├── run.py              # Main application runner
└── README.md           # This file
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python run.py setup
```

### 3. Collect Tournament Data
```bash
python run.py scrape
```

### 4. Start API Server
```bash
python run.py api
```

### 5. Export Data
```bash
python run.py export
```

## API Endpoints

### GET /tournaments
Get tournaments with optional filters:
- `sport`: Filter by sport (cricket, football, etc.)
- `level`: Filter by competition level
- `start_date`: Filter tournaments starting after this date
- `end_date`: Filter tournaments ending before this date
- `limit`: Maximum number of results (default: 100)

Example: `GET /tournaments?sport=cricket&level=International&limit=10`

### GET /sports
Get list of available sports

### GET /levels  
Get list of available competition levels

### GET /health
Health check endpoint

## Data Output Format

Each tournament entry contains:
- **Tournament Name**: Official tournament name
- **Level**: Competition level (International, National, etc.)
- **Start Date**: Tournament start date
- **End Date**: Tournament end date  
- **Tournament Official URL**: Official website
- **Streaming Partners/Links**: Where to watch
- **Tournament Image**: Official tournament image URL
- **Summary**: Brief description (max 50 words)
- **Location**: Tournament location

## Sample Output

```json
{
  "tournaments": [
    {
      "id": 1,
      "name": "ICC Cricket World Cup 2024",
      "sport": "cricket",
      "level": "International",
      "start_date": "2024-10-05",
      "end_date": "2024-11-19",
      "official_url": "https://www.icc-cricket.com/cricket-world-cup",
      "streaming_links": "Disney+ Hotstar, Star Sports",
      "image_url": "https://example.com/cwc2024.jpg",
      "summary": "The premier international cricket tournament featuring the world's best teams.",
      "location": "India"
    }
  ],
  "count": 1
}
```

## Technology Stack
- **Backend**: Python, Flask
- **Database**: SQLite
- **Web Scraping**: BeautifulSoup, Requests, Selenium
- **AI/LLM**: OpenAI GPT for data extraction and summarization
- **Frontend**: HTML, JavaScript, CSS

## Development Status
- [x] Project setup and structure
- [ ] Web scrapers implementation
- [ ] LLM integration for data processing
- [x] Database schema and API
- [ ] Frontend UI mockup
- [ ] Data export functionality

## Future Improvements
- Add more sports and tournament levels
- Implement real-time data updates
- Add tournament notifications
- Improve UI/UX design
- Add data validation and error handling