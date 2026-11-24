# Town Talk Marketing Solutions website

Static site: Home, Technology, Advertising, About, Contact.

- Technology page has a rebate finder demo (`src/rebate-finder.js`, demo figures, sends nothing).
- Advertising page has an ad budget estimator (`src/ad-estimator.js`) that emails each lead to Jared through Web3Forms.
- `dist/_redirects` sends the old `/services` URL to `/advertising`.

- `src/styles.css` and `src/assets/`: styles and brand images
- `build.py`: page content and templates; run `python3 build.py` to regenerate `dist/`
- `dist/`: the finished site, plain HTML/CSS, deployed as-is

## Cloudflare Pages settings

- Framework preset: None
- Build command: (leave empty)
- Build output directory: `dist`

## Cloudflare Workers

`wrangler.jsonc` tells Workers Builds to serve `dist/` as static assets. Deploy command: `npx wrangler deploy` (no build command).

## Contact form

The form sends through [Web3Forms](https://web3forms.com), which emails each submission to jared@towntalk.ca.
The access key is set in `WEB3FORMS_KEY` in `build.py`; run `python3 build.py` after changing it.
