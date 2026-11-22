# Brazil Pizza

Authentic Brazilian-style pizza, savory and sweet, plus rodízio Thursday to Sunday.
279 Powers Ferry Rd SE, Ste B, Marietta, GA 30067 · (404) 421-1426

Plain HTML/CSS/JS, hosted on GitHub Pages from the repo root. GSAP and Lenis load from a CDN for motion; the page still works without them.

- To change a price or dish: edit `MENU` in `tools/build.py`, then run `python3 tools/build.py` from this folder. It rebuilds `index.html`.
- Hours live in two places in `tools/template.html`: the hours table and the `HOURS` list in the first script. Update both.
- All "Order" buttons go to the restaurant's own Square ordering page.
- The site is unlisted (`noindex`). Remove that meta tag in `tools/template.html` when the owner approves and the domain is connected.
- Photos are the restaurant's own, from the "By owner" photos on its Google listing.
