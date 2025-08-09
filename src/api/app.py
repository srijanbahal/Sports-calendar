#!/usr/bin/env python3
"""
Main runner for Sports Tournament Calendar System
"""

import os
import sys
import argparse
from src.database.initDB import create_database
from src.api.app import app

def setup_project():
    """Initial project setup"""
    print("Setting up Sports Tournament Calendar...")
    create_database()
    print("Project setup complete!")

def run_scrapers():
    """Run all tournament scrapers"""
    print("Starting tournament data collection...")
    # Import and run scrapers
    from src.scrapers.cricket_scraper import CricketScraper
    # from src.scrapers.football_scraper import FootballScraper
    
    # Add scraper execution logic here
    print("Data collection complete!")

def start_api():
    """Start the Flask API server"""
    print("Starting API server...")
    app.run(debug=True, host='0.0.0.0', port=5000)

def export_data():
    """Export data to CSV/JSON"""
    print("Exporting tournament data...")
    # Import and run export functions
    print("Data export complete!")

def main():
    parser = argparse.ArgumentParser(description='Sports Tournament Calendar System')
    parser.add_argument('command', choices=['setup', 'scrape', 'api', 'export'], 
                        help='Command to run')
    
    args = parser.parse_args()
    
    if args.command == 'setup':
        setup_project()
    elif args.command == 'scrape':
        run_scrapers()
    elif args.command == 'api':
        start_api()
    elif args.command == 'export':
        export_data()

if __name__ == "__main__":
    main()