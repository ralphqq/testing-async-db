# async-scraping-and-storage
A collection of scrapers that uses Async IO, AIOHTTP, and AIOPG to asynchronously retrieve and save data.

## Sites to scrape
1. Hacker News front page: https://news.ycombinator.com
2. Google News top stories: https://news.google.com/topstories?hl=en-PH&gl=PH&ceid=PH:en

## Schema

Table name: `scraper_details`
Fields:
- `id`
- `name`

Table name: `scraped_items`
Fields:
- `id`
- `title`
- `url`
- `source_id`
- `scraped_ts`

Table name: `sources`
Fields:
- `id`
- `name`
- `url`

## To-do
1. Create base scraper class
2. Define item pipeline
3. Create a scraper for each of the above websites
4. Make a runner script
