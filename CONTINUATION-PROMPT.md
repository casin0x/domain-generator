# GoLuna Project — Continuation Prompt

Copy and paste this into a new Claude session to resume exactly where we left off:

---

## Prompt:

I'm continuing work on the GoLuna casino platform project. Read the project memory file first:

```
Read /Users/tradeaspire/.claude/projects/-Users-tradeaspire/memory/goluna-project.md
```

Then read the project CLAUDE.md:

```
Read ~/Documents/domain-generator/CLAUDE.md
```

**Quick context:** GoLuna is a casino/sports/PVP platform using a white-label template (same as Betplay.io). We've built:

1. **Casino demo** — 7 pages (homepage, casino, sports, VIP, deposit, profile, promotions) at `/goluna-demo/` with real game images extracted from the Figma template
2. **10 brand directions** — each with its own color scheme, all using CSS variables. Clickable screenshots on the brand page link to themed homepage variants
3. **Domain dashboard** — 6,377+ casino domain names with availability checking

**Working directory:** `~/Documents/domain-generator/`
**Live:** https://domain-generator-neon.vercel.app/goluna-demo/
**Brand page:** https://domain-generator-neon.vercel.app/goluna-brand.html
**GitHub:** `casin0x/domain-generator` (ALWAYS use casin0x, NEVER Astos-ai)
**Deploy:** `cd ~/Documents/domain-generator && npx vercel --prod --yes`

**Current state / what was last done:**
- Fixed all hardcoded blue colors across 16 HTML files — nav, ticker, hero, modal backgrounds now use CSS variables
- All 9 themed homepage variants regenerated with proper accent colors for glows, borders, shadows
- Brand page has clickable screenshots for all 10 directions
- The brand page screenshots are OUTDATED (taken before the color fixes) — need to be retaken with Playwright

**Key files:**
- `/goluna-demo/index.html` — Main homepage (Moonlit Luxe, 1500+ lines)
- `/goluna-demo/theme-*.html` — 9 themed variants (generated from index.html with CSS variable swaps)
- `/goluna-brand.html` — Brand exploration page (10 directions, screenshots, VIP tiers, voice)
- `/goluna-demo/assets/` — 32 game images + 10 homepage screenshots

**CSS architecture:** Everything uses `:root` CSS variables. To create a themed variant, swap variable values and regenerate. No hardcoded colors allowed outside `:root`.

**White-label constraint:** Layout structure is locked. We can only change colors, fonts, icons, text. Cannot change component layout.

**What needs doing next:** [describe your task here]

---

## Common tasks and how to do them:

### Retake brand page screenshots
```bash
# Start local server
cd ~/Documents/domain-generator/goluna-demo && python3 -m http.server 3940 &

# Use Playwright to screenshot each theme
# Navigate to http://localhost:3940/index.html (and temp variants)
# Screenshot with fullPage: true
# Save to /goluna-demo/assets/homepage-screenshot.png (dir1)
# and /goluna-demo/assets/homepage-dir{2-10}.png
```

### Create a new themed variant
```python
# Read index.html, regex-replace CSS variable values, write to theme-{name}.html
import re
with open('index.html') as f: base = f.read()
for var, val in colors.items():
    base = re.sub(re.escape(var) + r':\s*[^;]+;', f'{var}: {val};', base)
```

### Add a new demo page
1. Copy index.html CSS architecture (variables, nav, sidebar, footer, modal)
2. Keep same Google Fonts link
3. Replace main content area only
4. Update active states in sidebar/nav
5. Add links in other pages' nav

### Check for hardcoded colors
```bash
grep -rn 'rgba(10,15,46\|rgba(14,18,56\|rgba(212,160,23\|#0e1650\|#1a1060' goluna-demo/*.html | grep -v '\-\-'
```

### Deploy
```bash
gh auth switch --user casin0x  # ALWAYS check this first
cd ~/Documents/domain-generator && git add -A && git commit -m "message" && git push origin main && npx vercel --prod --yes
```
