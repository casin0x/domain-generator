# Domain Generator — Workspace Map

## What This Is
Casino/iGaming domain name search dashboard. Single-file static HTML app with 2,070+ compound names and 700+ short invented names, all WHOIS-verified across 4 TLDs (.com, .io, .bet, .game). Includes login system, per-user selection lists, filtering by category, sorting, export/copy.

**Repo:** `casin0x/domain-generator` | **Deploy:** Vercel (`prj_YhczDTsloYzkfmtqIoSmwzXDDOFb`, team `team_hMUhTpvxbNK0NsNtNh1mVHYV`)
**Live:** https://domain-generator-casin0x.vercel.app

## Architecture
```
index.html          # Entire app — HTML + CSS + JS + inline data (~313KB)
vercel.json         # Static deploy config (no build step)
```

This is a **single-file static app**. All domain data is embedded inline in the HTML as JavaScript arrays/objects. No backend, no database, no API calls. Login is client-side with hardcoded users (localStorage persistence).

## Key Features
- **Search & filter:** text search, category filters (compound, invented, short, animal, dark, action)
- **TLD columns:** .com, .io, .bet, .game — shows Available/Taken/price
- **Selection lists:** click rows to add to per-user list, export as text, copy to clipboard
- **Login system:** client-side auth with localStorage, per-user saved lists
- **Stats bar:** total names, available .com count, taken count, list count
- **Sorting:** click column headers to sort by name, type, taken count, TLD status

## Related Files (outside repo)
- **WHOIS checker:** `~/Documents/Domain-hunting/check_domains.py` (Python, GoDaddy API)
- **Raw data:** `~/Documents/casino-domain-search.csv`, `~/Documents/casino-invented-names-to-check.txt`
- **Batch results:** `~/tmp/batch8_names.json`, `~/tmp/batch8_results.json` (latest generation run)

## Development
```bash
# Local server (any static server works)
npx serve . -p 3001

# Deploy
vercel --prod
```

## Adding New Names
New domain names are generated in batch runs (see batch files in ~/tmp/) using compound word pools, then WHOIS-checked with the Domain-hunting script. Results get merged into the inline data arrays in index.html.

## Hard Rules
- **casin0x account only.** Never push to or reference Astos-ai.
- **All data is inline.** No external API calls or database. Domain data lives in the HTML file itself.
- **Dark theme only.** Background #0a0a0f, accent #6c5ce7.
