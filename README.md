# Town Talk Marketing Solutions website

Static site: Home, Services, About, Contact.

- `src/styles.css` and `src/assets/`: styles and brand images
- `build.py`: page content and templates; run `python3 build.py` to regenerate `dist/`
- `dist/`: the finished site, plain HTML/CSS, deployed as-is

## Cloudflare Pages settings

- Framework preset: None
- Build command: (leave empty)
- Build output directory: `dist`

## Contact form

The form sends through [Web3Forms](https://web3forms.com), which emails each submission to jared@towntalk.ca.
The access key is set in `WEB3FORMS_KEY` in `build.py`; run `python3 build.py` after changing it.
