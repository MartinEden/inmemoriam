A small Python script to scrape memorial data off an ongoing D&D campaign's wiki
and lay it out semi-randomly as tombstones.

Uses mustache (via chevron) for templating and requests + beautifulsoup for 
scraping.

# Run
To output the HTML to stdout, just run `./inmemoriam.py`. To build a complete
web page, with dependencies (CSS, fonts, etc.), run `./build.sh`.

# Publish
To publish to `surge.sh` free hosting, run `./publish.sh`, but you will first
have to update `CNAME` to point at a domain that is free, as the default one is
owned by my surge account.
