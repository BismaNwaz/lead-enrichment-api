# Lead Enrichment API
![CI](https://github.com/BismaNwaz/lead-enrichment-api/actions/workflows/deploy.yml/badge.svg)

An AI-powered backend service that turns a company website URL into structured, sales-ready lead data — industry classification, a summary, products/services, likely decision-maker titles, and contact info — using LLM-based extraction.

**Live demo:** https://bisma225-lead-enrichment-api.hf.space/docs
**Source:** https://github.com/BismaNwaz/lead-enrichment-api

## Why I built this

Lead enrichment is normally done manually or through expensive third-party data providers. This project automates the process end-to-end: scrape a company's public website, send the content to an LLM with a structured extraction prompt, and return clean, structured JSON ready to feed into a CRM or outreach workflow — the same kind of problem I've solved in production automation work, rebuilt here as an original, fully self-contained project.

## How it works

1. **Scrape** — `requests` + `BeautifulSoup` fetch and clean the target website's visible text content.
2. **Enrich** — the cleaned text is sent to Claude (Anthropic API) with a structured prompt, which extracts company name, industry, summary, products/services, likely decision-maker titles, contact email, and location as JSON.
3. **Cache** — results are stored in SQLite, keyed by URL, so repeat lookups don't re-scrape or re-call the LLM.
4. **Serve** — a FastAPI REST endpoint (`POST /enrich`) exposes the pipeline, with a `/health` check for monitoring.

```
Client → FastAPI → Scraper (BeautifulSoup) → Claude API → SQLite cache → JSON response
```

## Tech stack

- **Backend:** Python, FastAPI
- **Scraping:** Requests, BeautifulSoup4
- **AI:** Anthropic Claude API (structured JSON extraction)
- **Storage:** SQLite + SQLAlchemy
- **Deployment:** Docker, Hugging Face Spaces
- **Version control:** Git/GitHub

## API

### `GET /health`
Returns `{"status": "ok"}` — used for uptime/monitoring checks.

### `POST /enrich`
Request body:
```json
{ "url": "https://stripe.com" }
```

Response:
```json
{
  "company_name": "Stripe",
  "industry": "Financial Technology (FinTech) / Payment Processing",
  "summary": "...",
  "products_or_services": ["..."],
  "likely_decision_maker_titles": ["..."],
  "contact_email": null,
  "location": null
}
```

## Running locally

```bash
git clone https://github.com/BismaNwaz/lead-enrichment-api.git
cd lead-enrichment-api
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```
ANTHROPIC_API_KEY=your_key_here
```

Run it:
```bash
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

### Running with Docker

```bash
docker build -t lead-enrichment-api .
docker run -p 8000:8000 --env-file .env lead-enrichment-api
```

## Known limitations & future improvements

- **JS-heavy sites:** the scraper reads server-rendered HTML only. Sites that load their content dynamically via JavaScript (e.g. heavy React/Vue SPAs) may return incomplete text. A future version could add Playwright for headless-browser rendering on sites where static scraping comes up short.
- **Single-page scraping:** only the given URL is scraped. Adding a lightweight crawl of `/about` or `/contact` pages would likely improve contact/location field accuracy.
- **No batch endpoint yet:** currently one URL per request; a batch endpoint (`POST /enrich/batch`) would be a natural next step for higher-throughput use cases.
- **CI/CD:** deployment currently auto-builds on push via Hugging Face Spaces. A GitHub Actions workflow to run tests before deploy is a planned addition.

## Author

Built by Bisma Nawaz — Backend Developer & Automation Specialist. [LinkedIn](#)
