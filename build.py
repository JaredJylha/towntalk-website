#!/usr/bin/env python3
"""Builds the Town Talk site.

  dist/      a plain multi-page static site (deploy this folder as-is, e.g. Cloudflare Pages
             or Workers static assets; no build step needed on the host).
  preview/   a single-file version used for the claude.ai preview link (pages switch by #hash).

Run: python3 build.py
"""
import pathlib, re, shutil

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
CSS = (SRC / "styles.css").read_text()

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Archivo:wght@400;500;600;700;800&display=swap">'

PAGES = [
    ("home", "index.html", "Home"),
    ("services", "services.html", "Services"),
    ("about", "about.html", "About"),
    ("contact", "contact.html", "Contact"),
]
DESC = "Town Talk Marketing Solutions is an independent marketing consultancy helping small and mid-sized businesses make smarter marketing decisions and see what their marketing dollars achieve."


def header(cur):
    links = "".join(
        f'<a href="{{{{{k}}}}}"{" aria-current=\"page\"" if k == cur else ""}>{label}</a>'
        for k, _, label in PAGES[1:]
    )
    return f'''<header class="site-header"><div class="wrap">
  <a class="brand" href="{{{{home}}}}" aria-label="Town Talk Marketing Solutions, home">
    <img src="assets/emblem-light.png" alt="" width="256" height="224">
    <span>Town Talk<small>Marketing Solutions</small></span>
  </a>
  <nav class="nav" aria-label="Main">{links}<a class="nav-cta" href="{{{{contact}}}}">Book a call</a></nav>
</div></header>'''


FOOTER = '''<footer class="site-footer"><div class="wrap">
  <div>
    <img src="assets/logo-light.png" alt="Town Talk Marketing Solutions" width="290" height="163">
    <p>Independent marketing advice for small and mid-sized businesses. Clear plans, plain answers, and a straight account of where the money goes.</p>
  </div>
  <div><h4>Site</h4><ul><li><a href="{{home}}">Home</a></li><li><a href="{{services}}">Services</a></li><li><a href="{{about}}">About</a></li><li><a href="{{contact}}">Contact</a></li></ul></div>
  <div><h4>Get in touch</h4><ul><li><a href="{{contact}}">Book a free consult</a></li><li><a href="mailto:jared@towntalk.ca">jared@towntalk.ca</a></li><li><a href="tel:+12893384051">(289) 338-4051</a></li><li>Muskoka and Brock, Ontario</li></ul></div>
  <div class="legal"><span>&copy; 2026 Town Talk Marketing Solutions</span><span>Independent marketing consultancy</span></div>
</div></footer>'''

CTA = '''<section class="cta"><div class="wrap on-paper" style="background:transparent">
  <div>
    <h2>Find out what your marketing is really doing.</h2>
    <p>Start with a free 30-minute conversation. Bring your last few invoices and we will tell you what we see.</p>
  </div>
  <div class="btn-row"><a class="btn btn-solid" href="{{contact}}">Book a free consult</a></div>
</div></section>'''

HOME = '''<section class="hero">
  <img class="hero-img" src="assets/hero.jpg" srcset="assets/hero-sm.jpg 836w, assets/hero.jpg 1672w" sizes="100vw" alt="" width="1672" height="941">
  <div class="wrap">
    <div class="eyebrow">Marketing Solutions</div>
    <h1>Smarter marketing for local business.</h1>
    <p class="lede">Town Talk is an independent consultancy for small and mid-sized businesses. We help you decide where to spend, cut what isn't working, and see what every dollar is doing.</p>
    <div class="btn-row"><a class="btn btn-solid" href="{{contact}}">Book a free consult</a><a class="btn btn-ghost" href="{{services}}">See services</a></div>
  </div>
</section>

<section class="band on-paper"><div class="wrap">
  <div class="section-head">
    <div class="eyebrow">Sound familiar?</div>
    <h2>Most owners we meet are asking the same questions.</h2>
  </div>
  <ul class="questions">
    <li>&ldquo;Is any of this advertising working?&rdquo;</li>
    <li>&ldquo;Every vendor says their channel is the one.&rdquo;</li>
    <li>&ldquo;I don't have time to manage five suppliers.&rdquo;</li>
    <li>&ldquo;Where should next year's budget go?&rdquo;</li>
  </ul>
</div></section>

<section class="band band-dark"><div class="wrap split">
  <div class="copy">
    <div class="eyebrow">Where the money goes</div>
    <h2>We start by reading your marketing like a ledger.</h2>
    <p>Before we recommend anything, we line up every marketing cost against what it produced. Most businesses find at least one line nobody can explain.</p>
    <p>From there the plan is simple: keep what earns, fix what could, and stop paying for what doesn't.</p>
    <div class="btn-row"><a class="btn btn-ghost" href="{{services}}">How a review works</a></div>
  </div>
  <div class="ledger" role="figure" aria-label="Example monthly marketing spend review">
    <div class="ledger-head"><span>Monthly spend review</span><span class="tag">Example</span></div>
    <div class="ledger-scroll"><table>
      <thead><tr><th>Channel</th><th class="num">Spend / mo</th><th class="num">Result</th><th class="num">Cost each</th></tr></thead>
      <tbody>
        <tr><td>Search ads</td><td class="num">$900</td><td class="num">61 calls</td><td class="num">$14.75</td></tr>
        <tr><td>Social ads</td><td class="num">$1,600</td><td class="num">38 leads</td><td class="num">$42.10</td></tr>
        <tr class="flag"><td>Print directory</td><td class="num">$1,100</td><td class="num"><span class="unknown">Not tracked</span></td><td class="num">?</td></tr>
        <tr class="flag"><td>Local radio</td><td class="num">$600</td><td class="num"><span class="unknown">Not tracked</span></td><td class="num">?</td></tr>
      </tbody>
      <tfoot><tr><td>Total</td><td class="num">$4,200</td><td class="num"></td><td class="num">40% unaccounted</td></tr></tfoot>
    </table></div>
    <div class="ledger-note">Illustrative figures for a local retailer. In a real review these come from your own invoices and reports.</div>
  </div>
</div></section>

<section class="band on-paper"><div class="wrap">
  <div class="section-head">
    <div class="eyebrow">What we do</div>
    <h2>Six ways we help.</h2>
    <p>Use us for one piece or the whole picture. You only pay for the help you need.</p>
  </div>
  <div class="services">
    <div class="service"><h3>Strategic advice</h3><p>A clear plan for where to spend and why, built around your goals and budget.</p></div>
    <div class="service"><h3>Marketing solutions</h3><p>Practical fixes for specific problems, from slow seasons to a new location launch.</p></div>
    <div class="service"><h3>Campaign development</h3><p>Campaigns planned from the offer to the message to how results get measured.</p></div>
    <div class="service"><h3>Advertising guidance</h3><p>Independent advice on media buys, so you can judge proposals with confidence.</p></div>
    <div class="service"><h3>Technology support</h3><p>Websites, tracking, CRM and tools set up so they work together and report properly.</p></div>
    <div class="service"><h3>Project coordination</h3><p>One point of contact managing designers, printers, developers and media reps.</p></div>
  </div>
  <div class="btn-row" style="margin-top:2.5rem"><a class="btn btn-solid" href="{{services}}">Explore services</a></div>
</div></section>

<section class="band band-night"><div class="wrap">
  <div class="section-head">
    <div class="eyebrow">Not an agency</div>
    <h2>Independent advice, with no media to sell you.</h2>
    <p>Agencies earn more when you spend more. We earn our fee by helping you spend well. That keeps the advice honest.</p>
  </div>
  <div class="values">
    <div><h3>Plain answers</h3><p>No jargon and no fifty-slide decks. You get a short list of what to do next and why.</p></div>
    <div><h3>Clear numbers</h3><p>Every recommendation ties back to cost and results you can check yourself.</p></div>
    <div><h3>Hands on</h3><p>We don't hand over a plan and leave. We help get it done and coordinate the people doing it.</p></div>
  </div>
</div></section>
''' + CTA

SERVICES = '''<section class="page-hero">
  <img class="ghost-mark" src="assets/emblem-light.png" alt="" width="256" height="224">
  <div class="wrap">
    <div class="eyebrow">Services</div>
    <h1>Marketing help, sized to your business.</h1>
    <p>Six services, one goal: marketing you understand and can measure. Start with one or bring us in for the whole picture.</p>
  </div>
</section>

<section class="band on-paper"><div class="wrap">
  <div class="services">
    <div class="service"><h3>Strategic advice</h3><p>A clear marketing plan built around your goals, customers and budget.</p>
      <ul><li>Marketing and spend review</li><li>Annual plan and budget split</li><li>Customer and competitor snapshot</li><li>Quarterly check-ins</li></ul></div>
    <div class="service"><h3>Marketing solutions</h3><p>Focused fixes for a specific business problem.</p>
      <ul><li>Slow-season and off-peak plans</li><li>New location or product launches</li><li>Lead follow-up and conversion</li><li>Brand and message clean-up</li></ul></div>
    <div class="service"><h3>Campaign development</h3><p>Campaigns planned end to end, with results measured from day one.</p>
      <ul><li>Offer and message development</li><li>Channel mix and schedule</li><li>Creative brief for designers</li><li>Tracking set up before launch</li></ul></div>
    <div class="service"><h3>Advertising guidance</h3><p>A second opinion from someone with nothing to sell you.</p>
      <ul><li>Review of media proposals and rates</li><li>Search, social, print, radio and outdoor</li><li>Negotiation support</li><li>Monthly performance read-outs</li></ul></div>
    <div class="service"><h3>Technology support</h3><p>The tools behind your marketing, set up to work together.</p>
      <ul><li>Website updates and landing pages</li><li>Analytics and call tracking</li><li>CRM and email platform set-up</li><li>Google Business Profile and listings</li></ul></div>
    <div class="service"><h3>Project coordination</h3><p>One contact who manages the suppliers so you don't have to.</p>
      <ul><li>Designers, printers and developers</li><li>Media reps and agencies</li><li>Timelines and approvals</li><li>Budget tracking against plan</li></ul></div>
  </div>
</div></section>

<section class="band band-dark"><div class="wrap">
  <div class="section-head">
    <div class="eyebrow">How it works</div>
    <h2>From first call to clear results.</h2>
  </div>
  <ol class="steps">
    <li><h3>Listen</h3><p>A free conversation about your business, your goals and what you are spending today.</p></li>
    <li><h3>Review</h3><p>We line up every marketing cost against what it produced and show you what we find.</p></li>
    <li><h3>Plan</h3><p>A short, practical plan: what to keep, what to change, and what to stop.</p></li>
    <li><h3>Coordinate</h3><p>We help put the plan in place and manage the people and suppliers involved.</p></li>
    <li><h3>Report</h3><p>Regular plain-language updates on spend and results, so you always know where you stand.</p></li>
  </ol>
</div></section>

<section class="band band-night"><div class="wrap">
  <div class="section-head">
    <div class="eyebrow">Who we work with</div>
    <h2>Built for owner-run businesses.</h2>
    <p>Typically businesses with no in-house marketing team, or a small one that needs a senior voice.</p>
  </div>
  <ul class="chips">
    <li>Retail and showrooms</li><li>Trades and home services</li><li>Restaurants and hospitality</li><li>Professional services</li><li>Health and wellness</li><li>Automotive</li><li>Multi-location businesses</li>
  </ul>
</div></section>
''' + CTA

ABOUT = '''<section class="page-hero">
  <img class="ghost-mark" src="assets/emblem-light.png" alt="" width="256" height="224">
  <div class="wrap">
    <div class="eyebrow">About Town Talk</div>
    <h1>Marketing, made simple again.</h1>
    <p>Town Talk Marketing Solutions is an independent consultancy that helps small and mid-sized businesses make smarter marketing decisions and get more from what they spend.</p>
  </div>
</section>

<section class="band on-paper"><div class="wrap split">
  <div class="copy" style="gap:1.25rem">
    <div class="eyebrow">Why we exist</div>
    <h2>Owners deserve a straight answer.</h2>
  </div>
  <div style="display:grid;gap:1.25rem;font-size:1.1rem">
    <p>Most business owners are pitched by a dozen media reps, platforms and agencies, each sure their channel is the answer. Few of them can say what the last campaign actually returned.</p>
    <p>Town Talk sits on your side of the table. We help you find growth opportunities, sort good proposals from bad ones, and understand where your marketing dollars are going and what they achieve.</p>
    <p>When something needs doing, we roll up our sleeves and coordinate it, so you get one accountable contact instead of five suppliers.</p>
  </div>
</div></section>

<section class="band band-dark" id="founder"><div class="wrap founder">
  <figure class="founder-photo">
    <img src="assets/founder-portrait.jpg" alt="Jared Jylha, Founder and CEO of Town Talk Marketing Solutions" width="640" height="800" loading="lazy">
  </figure>
  <div class="founder-copy">
    <div class="eyebrow">Meet the founder</div>
    <div>
      <h2>Jared Jylha</h2>
      <p class="founder-role">Founder and CEO</p>
    </div>
    <p>Jared Jylha is the Founder and CEO of Town Talk Marketing, a marketing consultancy built on the belief that good marketing starts with understanding the business behind it.</p>
    <p>With more than six years of experience in marketing and advertising, Jared has worked with businesses across a range of industries, helping them navigate digital advertising, marketing strategy, media planning, and customer acquisition. His experience managing client relationships, overseeing advertising budgets, and translating performance data into actionable insights has shaped his practical approach to marketing.</p>
    <p>Jared founded Town Talk Marketing to make marketing and business decision-making simpler, more accessible, and more strategic. Having worked closely with businesses and their marketing teams, he recognized the need for clear advice, practical thinking, and a better understanding of where marketing efforts and budgets are best invested. His goal is to help business owners cut through the noise, understand their options, and make confident decisions about what comes next.</p>
    <p>As a Chartered Marketer (CM), Jared combines hands-on industry experience with a commitment to continued learning. He believes effective marketing isn't about doing more for the sake of doing more. It's about asking better questions, understanding what matters, and making smarter decisions that move a business forward.</p>
    <div class="credential">
      <img src="assets/cm-badge.png" alt="Chartered Marketer (CM) designation badge" width="240" height="240" loading="lazy">
      <div><strong>Chartered Marketer (CM)</strong><span>Professional marketing designation</span></div>
    </div>
  </div>
</div></section>

<section class="band on-paper"><div class="wrap">
  <div class="compare">
    <div class="yes"><h3>What Town Talk is</h3><ul>
      <li>An independent advisor on your side</li>
      <li>A strategist who explains the numbers</li>
      <li>A hands-on coordinator for the work</li>
      <li>Flexible, so you pay only for what you use</li>
    </ul></div>
    <div class="no"><h3>What we are not</h3><ul>
      <li>A full-service ad agency</li>
      <li>Paid by commission on your media spend</li>
      <li>Locked into long retainers</li>
      <li>A reseller of any one platform</li>
    </ul></div>
  </div>
</div></section>

<section class="band band-dark"><div class="wrap">
  <div class="section-head">
    <div class="eyebrow">How we work</div>
    <h2>Three promises to every client.</h2>
  </div>
  <div class="values">
    <div><h3>Simplify</h3><p>We cut marketing down to the few things that matter for your business and say them plainly.</p></div>
    <div><h3>Solve</h3><p>We start from the business problem, not the channel, and recommend only what fixes it.</p></div>
    <div><h3>Show the results</h3><p>You will always know what you spent, what it produced, and what we suggest next.</p></div>
  </div>
</div></section>
''' + CTA

CONTACT = '''<section class="page-hero">
  <img class="ghost-mark" src="assets/emblem-light.png" alt="" width="256" height="224">
  <div class="wrap">
    <div class="eyebrow">Contact</div>
    <h1>Let's talk about your marketing.</h1>
    <p>Tell us a little about your business and we will set up a free 30-minute call. No pitch and no obligation.</p>
  </div>
</section>

<section class="band on-paper"><div class="wrap contact-grid">
  <div class="contact-info">
    <div class="eyebrow">Reach us</div>
    <dl>
      <div><dt>Email</dt><dd><a href="mailto:jared@towntalk.ca">jared@towntalk.ca</a></dd></div>
      <div><dt>Phone</dt><dd><a href="tel:+12893384051">(289) 338-4051</a></dd></div>
      <div><dt>Service area</dt><dd>Clients across Canada</dd></div>
      <div><dt>Offices</dt><dd>Muskoka and Brock, Ontario</dd></div>
    </dl>
    <div>
      <div class="eyebrow" style="margin-bottom:0.75rem">What to bring</div>
      <p style="color:var(--muted-light)">If you can, bring your last three months of marketing invoices or reports. It makes the first call far more useful.</p>
    </div>
  </div>
  <form class="form" id="contact-form" novalidate>
    <input type="checkbox" name="botcheck" id="cf-botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
    <h2>Book a free consult</h2>
    <div class="field-row">
      <div class="field"><label for="cf-name">Your name</label><input id="cf-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="cf-business">Business</label><input id="cf-business" name="business" autocomplete="organization"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="cf-email">Email</label><input id="cf-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="cf-phone">Phone</label><input id="cf-phone" name="phone" type="tel" autocomplete="tel"></div>
    </div>
    <div class="field"><label for="cf-spend">Monthly marketing spend</label>
      <select id="cf-spend" name="spend"><option value="">Choose a range</option><option>Under $1,000</option><option>$1,000 to $5,000</option><option>$5,000 to $15,000</option><option>Over $15,000</option><option>Not sure</option></select></div>
    <div class="field"><label for="cf-msg">What would you like help with?</label><textarea id="cf-msg" name="message"></textarea></div>
    <div class="btn-row"><button class="btn btn-solid" type="submit">Send request</button></div>
    <p class="form-status" id="cf-status" hidden></p>
  </form>
</div></section>
'''

BODIES = {"home": HOME, "services": SERVICES, "about": ABOUT, "contact": CONTACT}

# Contact form delivery: Web3Forms (https://web3forms.com) emails each submission to the
# address the access key was created for (jared@towntalk.ca). The key is public by design.
WEB3FORMS_KEY = "fa269272-cd0e-4498-98c7-e3fd4660d626"

FORM_JS_TEMPLATE = '''<script>
(function(){
  var KEY="__WEB3FORMS_KEY__";
  var f=document.getElementById('contact-form'); if(!f) return;
  var s=document.getElementById('cf-status'), btn=f.querySelector('button[type=submit]');
  function say(t){s.textContent=t;s.hidden=false;}
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var n=f.querySelector('#cf-name'), m=f.querySelector('#cf-email');
    if(!n.value.trim()||!m.value.trim()||!m.checkValidity()){say('Please add your name and a valid email address.');return;}
    if(f.querySelector('#cf-botcheck').checked) return;
    if(!KEY){say('The form is not connected yet. Please email jared@towntalk.ca or call (289) 338-4051.');return;}
    var data=Object.fromEntries(new FormData(f).entries());
    delete data.botcheck;
    data.access_key=KEY;
    data.subject='Website enquiry from '+n.value.trim()+(data.business?' ('+data.business+')':'');
    data.from_name='Town Talk website';
    data.replyto=m.value.trim();
    btn.disabled=true; say('Sending...');
    fetch('https://api.web3forms.com/submit',{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(data)})
      .then(function(r){return r.json();})
      .then(function(j){
        if(j.success){var first=n.value.trim().split(' ')[0];f.reset();say('Thanks, '+first+'. Your message is on its way, and Jared will be in touch soon.');}
        else{say('Your message did not send. Please try again, or email jared@towntalk.ca.');}
      })
      .catch(function(){say('Your message did not send. Check your connection and try again, or email jared@towntalk.ca.');})
      .finally(function(){btn.disabled=false;});
  });
})();
</script>'''
FORM_JS = FORM_JS_TEMPLATE.replace("__WEB3FORMS_KEY__", WEB3FORMS_KEY)
PREVIEW_FORM_JS = FORM_JS_TEMPLATE.replace("__WEB3FORMS_KEY__", "")  # preview can't reach outside hosts


def fill(html, mode):
    for k, file, _ in PAGES:
        html = html.replace("{{" + k + "}}", file if mode == "dist" else "#" + k)
    return html


def build_dist():
    out = ROOT / "dist"
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(SRC / "assets", out / "assets")
    (out / "styles.css").write_text(CSS)
    for k, file, label in PAGES:
        title = "Town Talk Marketing Solutions" if k == "home" else f"{label} | Town Talk Marketing Solutions"
        doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="assets/hero.jpg">
<link rel="icon" type="image/png" href="assets/emblem-dark.png">
{FONTS}
<link rel="stylesheet" href="styles.css">
</head>
<body>
{header(k)}
<main>
{BODIES[k]}
</main>
{FOOTER}
{FORM_JS if k == "contact" else ""}
</body>
</html>
'''
        (out / file).write_text(fill(doc, "dist"))


def build_preview():
    out = ROOT / "preview"
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(SRC / "assets", out / "assets")
    sections = []
    for k, _, _ in PAGES:
        # Each page gets its own header so the active nav state is right.
        sections.append(f'<div data-page="{k}"{" hidden" if k != "home" else ""}>{header(k)}<main>{BODIES[k]}</main></div>')
    router = '''<script>
(function(){
  var pages=['home','services','about','contact'];
  function show(){
    var h=(location.hash||'').slice(1); if(pages.indexOf(h)<0) h='home';
    document.querySelectorAll('[data-page]').forEach(function(el){el.hidden=el.getAttribute('data-page')!==h;});
    window.scrollTo(0,0);
  }
  window.addEventListener('hashchange',show); show();
})();
</script>'''
    doc = f'''<title>Town Talk Website</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}
<style>
{CSS}
</style>
{"".join(sections)}
{FOOTER}
{PREVIEW_FORM_JS}
{router}
'''
    (out / "index.html").write_text(fill(doc, "preview"))


if __name__ == "__main__":
    build_dist()
    build_preview()
    print("built dist/ and preview/")
