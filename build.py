#!/usr/bin/env python3
"""Builds the Town Talk site.

  dist/      a plain multi-page static site (deploy this folder as-is, e.g. Cloudflare Pages
             or Workers static assets; no build step needed on the host).
  preview/   a single-file version used for the claude.ai preview link (pages switch by #hash).

Run: python3 build.py
"""
import pathlib, shutil

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
CSS = (SRC / "styles.css").read_text()
SCRIPTS = ["rebate-finder.js", "ad-estimator.js"]

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Archivo:wght@400;500;600;700;800&display=swap">'

PAGES = [
    ("home", "index.html", "Home"),
    ("technology", "technology.html", "Technology"),
    ("advertising", "advertising.html", "Advertising"),
    ("about", "about.html", "About"),
    ("contact", "contact.html", "Contact"),
]
DESC = "Town Talk Marketing Solutions builds lead-generation tools for home improvement websites and gives independent advice on advertising: contract reviews, media plans and digital campaigns."

# Contact form and estimator delivery: Web3Forms (https://web3forms.com) emails each submission to
# the address the access key was created for (jared@towntalk.ca). The key is public by design.
WEB3FORMS_KEY = "fa269272-cd0e-4498-98c7-e3fd4660d626"


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
    <p>Lead-generation tools and independent advertising advice for home improvement businesses. Plain answers and a straight account of where the money goes.</p>
  </div>
  <div><h4>Site</h4><ul><li><a href="{{home}}">Home</a></li><li><a href="{{technology}}">Technology</a></li><li><a href="{{advertising}}">Advertising</a></li><li><a href="{{about}}">About</a></li><li><a href="{{contact}}">Contact</a></li></ul></div>
  <div><h4>Get in touch</h4><ul><li><a href="{{contact}}">Book a free call</a></li><li><a href="mailto:jared@towntalk.ca">jared@towntalk.ca</a></li><li><a href="tel:+12893384051">(289) 338-4051</a></li><li>Muskoka and Brock, Ontario</li></ul></div>
  <div class="legal"><span>&copy; 2026 Town Talk Marketing Solutions</span><span>Independent marketing consultancy</span></div>
</div></footer>'''


def cta(title, text, button="Book a free call"):
    return f'''<section class="cta"><div class="wrap on-paper" style="background:transparent">
  <div>
    <h2>{title}</h2>
    <p>{text}</p>
  </div>
  <div class="btn-row"><a class="btn btn-solid" href="{{{{contact}}}}">{button}</a></div>
</div></section>'''


CTA = cta("Find out what your marketing is really doing.",
          "Start with a free 30-minute call. Bring your last few ad invoices, or tell us the question your customers ask most.")

HOME = '''<section class="hero">
  <img class="hero-img" src="assets/hero.jpg" srcset="assets/hero-sm.jpg 836w, assets/hero.jpg 1672w" sizes="100vw" alt="" width="1672" height="941">
  <div class="wrap">
    <div class="eyebrow">Marketing Solutions</div>
    <h1>Smarter marketing for local business.</h1>
    <p class="lede">Town Talk is an independent consultancy for small and mid-sized businesses. We help you decide where to spend, cut what isn't working, and see what every dollar is doing.</p>
    <div class="hero-special">
      <div class="eyebrow">What we specialize in</div>
      <p>Town Talk builds simple lead-generation tools for your website, then makes sure the advertising that sends people to them is worth what you pay.</p>
    </div>
    <div class="btn-row"><a class="btn btn-solid" href="{{technology}}#demo">Try the rebate finder</a><a class="btn btn-ghost" href="{{advertising}}#estimator">Estimate your ad budget</a></div>
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
    <li>&ldquo;Is our agency worth what we pay?&rdquo;</li>
    <li>&ldquo;Our site gets visits but few quote requests.&rdquo;</li>
  </ul>
</div></section>

<section class="band band-dark"><div class="wrap split">
  <div class="copy">
    <div class="eyebrow">Where the money goes</div>
    <h2>We start by reading your marketing like a ledger.</h2>
    <p>Before we recommend anything, we line up every marketing cost against what it produced. Most businesses find at least one line nobody can explain.</p>
    <p>From there the plan is simple: keep what earns, fix what could, and stop paying for what doesn't.</p>
    <div class="btn-row"><a class="btn btn-ghost" href="{{advertising}}">How a review works</a></div>
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

<section class="band band-night"><div class="wrap">
  <div class="section-head">
    <div class="eyebrow">What we specialize in</div>
    <h2>Two ways we help.</h2>
    <p>Start with either one. Most clients end up using both, because one feeds the other.</p>
  </div>
  <div class="pillars">
    <a class="pillar" href="{{technology}}">
      <span class="pillar-num">01</span>
      <h3>Technology</h3>
      <p class="pillar-lede">Lead-generation tools for your website.</p>
      <p>Rebate finders, cost estimators and booking tools that answer a customer's question on the spot and hand your sales team a lead with a name, email and project details. One-time fee, no long contract.</p>
      <span class="pillar-link">See the tools and try a demo</span>
    </a>
    <a class="pillar" href="{{advertising}}">
      <span class="pillar-num">02</span>
      <h3>Advertising</h3>
      <p class="pillar-lede">Bring your invoices.</p>
      <p>An independent review of your ad contracts and agency agreements, a media plan built around your budget, digital campaigns that send the right homeowners to your site, and training if you'd rather run ads yourself.</p>
      <span class="pillar-link">See advertising services</span>
    </a>
  </div>
</div></section>

<section class="band on-paper"><div class="wrap">
  <div class="section-head">
    <div class="eyebrow">Who we work with</div>
    <h2>Built for home improvement.</h2>
    <p>Owner-run trades and contractors with no time to manage five marketing vendors.</p>
  </div>
  <ul class="chips chips-paper">
    <li>Carpenters</li><li>Electricians</li><li>Plumbers</li><li>HVAC technicians</li><li>Roofers</li><li>Insulation installers</li><li>Window and door installers</li><li>Painters</li><li>Flooring installers</li><li>Masons and concrete</li><li>Landscapers</li><li>General contractors</li>
  </ul>
</div></section>

<section class="band band-dark"><div class="wrap">
  <div class="section-head">
    <div class="eyebrow">Not an agency</div>
    <h2>Independent advice, on your side of the table.</h2>
    <p>Agencies earn more when you spend more. We earn our fee by helping you spend well. That keeps the advice honest.</p>
  </div>
  <div class="values">
    <div><h3>Plain answers</h3><p>No jargon and no fifty-slide decks. You get a short list of what to do next and why.</p></div>
    <div><h3>Clear numbers</h3><p>Every recommendation ties back to cost and results you can check yourself.</p></div>
    <div><h3>Hands on</h3><p>We don't hand over a plan and leave. We help get it done and coordinate the people doing it.</p></div>
  </div>
</div></section>
''' + CTA

TECHNOLOGY = '''<section class="page-hero">
  <img class="ghost-mark" src="assets/emblem-light.png" alt="" width="256" height="224">
  <div class="wrap">
    <div class="eyebrow">Technology</div>
    <h1>Website tools that turn visitors into leads.</h1>
    <p>Small, fast widgets for home improvement websites. They answer a customer's question on the spot and hand your sales team a qualified lead: name, email and exactly what they're interested in.</p>
    <div class="btn-row"><a class="btn btn-solid" href="#demo">Try the demo</a><a class="btn btn-ghost" href="{{contact}}">Book a call</a></div>
  </div>
</section>

<section class="band band-dark" id="demo"><div class="wrap">
  <div class="section-head">
    <div class="eyebrow">Try it</div>
    <h2>Rebate finder demo.</h2>
    <p>Set up for an example insulation company. Homeowners answer three quick questions, see the rebates they may qualify for, and request their full breakdown and an assessment.</p>
  </div>
  <div class="tool" id="rebate-finder">
    <div class="tool-head"><span>Home energy rebate finder</span><span class="tag">Demo</span></div>
    <div class="tool-grid">
      <form class="tool-questions rf-questions" onsubmit="return false">
        <fieldset><legend>1. What kind of home?</legend><div class="opts">
          <label class="opt"><input type="radio" name="rf-home" value="detached"><span>Detached house</span></label>
          <label class="opt"><input type="radio" name="rf-home" value="attached"><span>Semi or townhouse</span></label>
          <label class="opt"><input type="radio" name="rf-home" value="mobile"><span>Mobile or modular</span></label>
        </div></fieldset>
        <fieldset><legend>2. How is it heated?</legend><div class="opts">
          <label class="opt"><input type="radio" name="rf-heat" value="gas"><span>Natural gas</span></label>
          <label class="opt"><input type="radio" name="rf-heat" value="electric"><span>Electric</span></label>
          <label class="opt"><input type="radio" name="rf-heat" value="oil"><span>Oil or propane</span></label>
          <label class="opt"><input type="radio" name="rf-heat" value="heatpump"><span>Heat pump</span></label>
        </div></fieldset>
        <fieldset><legend>3. What are you thinking of upgrading? <small>Pick any</small></legend><div class="opts">
          <label class="opt"><input type="checkbox" name="rf-up" value="attic"><span>Attic insulation</span></label>
          <label class="opt"><input type="checkbox" name="rf-up" value="wall"><span>Wall insulation</span></label>
          <label class="opt"><input type="checkbox" name="rf-up" value="basement"><span>Basement insulation</span></label>
          <label class="opt"><input type="checkbox" name="rf-up" value="air"><span>Air sealing</span></label>
          <label class="opt"><input type="checkbox" name="rf-up" value="windows"><span>Windows and doors</span></label>
          <label class="opt"><input type="checkbox" name="rf-up" value="heatpump"><span>Heat pump</span></label>
        </div></fieldset>
      </form>
      <div class="tool-out">
        <div class="rf-result" aria-live="polite"></div>
        <form class="form tool-gate rf-gate" novalidate hidden>
          <h3>Get your full rebate breakdown</h3>
          <p>We'll email the amounts for each program and call to book a free home assessment.</p>
          <div class="field-row">
            <div class="field"><label for="rf-name">Name</label><input id="rf-name" name="rf-name" autocomplete="name"></div>
            <div class="field"><label for="rf-email">Email</label><input id="rf-email" name="rf-email" type="email" autocomplete="email"></div>
          </div>
          <div class="field-row">
            <div class="field"><label for="rf-phone">Phone</label><input id="rf-phone" name="rf-phone" type="tel" autocomplete="tel"></div>
            <div class="field"><label for="rf-postal">Postal code</label><input id="rf-postal" name="rf-postal" autocomplete="postal-code"></div>
          </div>
          <label class="check"><input type="checkbox" name="rf-book" checked><span>Yes, book my free on-site assessment</span></label>
          <div class="btn-row"><button class="btn btn-solid" type="submit">Show my rebates</button></div>
          <p class="form-status" hidden></p>
        </form>
      </div>
    </div>
    <div class="rf-lead" hidden>
      <div class="lead-head"><span>What the business receives</span><span class="tag">New lead</span></div>
      <table><tbody></tbody></table>
      <p class="ledger-note">In a live version this lands in the company's inbox or CRM within seconds, and nothing is sent from this demo. Rebate amounts here are example figures; your version is built on the current programs in your area.</p>
    </div>
  </div>
</div></section>

<section class="band band-night"><div class="wrap">
  <div class="section-head">
    <div class="eyebrow">How it fits together</div>
    <h2>From first click to booked visit.</h2>
  </div>
  <ol class="steps">
    <li><h3>Add a tool</h3><p>A widget on your site answers the question customers ask most: what rebates can I get, or what will this cost?</p></li>
    <li><h3>Capture the lead</h3><p>To see their full result, visitors leave their email and project details. It goes straight to your sales team.</p></li>
    <li><h3>Book the visit</h3><p>Your team follows up with a quote or an on-site assessment, already knowing what the customer wants.</p></li>
    <li><h3>Drive traffic</h3><p>Digital ads send the right homeowners to the tool, and you see the cost of every lead in plain numbers.</p></li>
  </ol>
</div></section>

<section class="band on-paper"><div class="wrap">
  <div class="section-head">
    <div class="eyebrow">What we build</div>
    <h2>Tools your customers will actually use.</h2>
    <p>Each one is built for your business, matches your brand, and works on any website. One-time build fee.</p>
  </div>
  <div class="services">
    <div class="service"><h3>Rebate finders</h3><p>Show homeowners the rebates and financing they may qualify for, then collect their details for a quote or assessment.</p></div>
    <div class="service"><h3>Cost estimators</h3><p>A ballpark price for a roof, deck or window package in a minute, so serious buyers raise their hand.</p></div>
    <div class="service"><h3>Product match quizzes</h3><p>A few questions that point customers to the right product line, with the answers passed to your sales team.</p></div>
    <div class="service"><h3>Assessment booking</h3><p>Let customers request an on-site visit or consultation without phone tag, with the job details already filled in.</p></div>
    <div class="service"><h3>Financing calculators</h3><p>Turn a big number into a monthly payment, which keeps more people in the conversation.</p></div>
    <div class="service"><h3>AI assistants</h3><p>Coming next: website helpers that answer common questions any time of day and hand hot leads to your team.</p></div>
  </div>
</div></section>

<section class="band band-night"><div class="wrap">
  <div class="section-head">
    <div class="eyebrow">How it works</div>
    <h2>Live on your site in weeks, not months.</h2>
  </div>
  <ol class="steps">
    <li><h3>Talk</h3><p>A short call about the question your customers ask most and how your team follows up.</p></li>
    <li><h3>Build</h3><p>We build the tool around your products, service area and brand.</p></li>
    <li><h3>Install</h3><p>A small snippet added to your site. It works with WordPress, Wix, Squarespace and the rest.</p></li>
    <li><h3>Collect leads</h3><p>Every submission goes to your inbox or CRM with the customer's answers attached.</p></li>
    <li><h3>Add traffic</h3><p>Pair it with a digital ad campaign that sends the right homeowners straight to the tool.</p></li>
  </ol>
  <div class="btn-row" style="margin-top:2.5rem"><a class="btn btn-ghost" href="{{advertising}}">See advertising services</a></div>
</div></section>
''' + cta("Want a tool like this on your site?",
          "Tell us the question your customers ask most. We'll show you what a tool for it could look like on a free 30-minute call.")

ADVERTISING = '''<section class="page-hero">
  <img class="ghost-mark" src="assets/emblem-light.png" alt="" width="256" height="224">
  <div class="wrap">
    <div class="eyebrow">Advertising</div>
    <h1>Bring your invoices.</h1>
    <p>Think of us as the angel on your shoulder. We review your ad contracts and agency agreements, build a media plan that fits your budget, run digital campaigns that send customers to your website, or teach your team to run them.</p>
    <div class="btn-row"><a class="btn btn-solid" href="#estimator">Estimate your budget</a><a class="btn btn-ghost" href="{{contact}}">Book a review call</a></div>
  </div>
</section>

<section class="band band-dark" id="estimator"><div class="wrap">
  <div class="section-head">
    <div class="eyebrow">Free tool</div>
    <h2>How much should you spend on advertising?</h2>
    <p>Answer five questions for a recommended monthly budget. Leave your email to see how it should split across channels.</p>
  </div>
  <div class="tool" id="ad-estimator" data-key="{{web3forms_key}}" data-contact="{{contact}}">
    <div class="tool-head"><span>Ad budget estimator</span><span class="tag">Home improvement</span></div>
    <div class="tool-grid">
      <form class="tool-questions ae-questions" onsubmit="return false">
        <fieldset><legend><label for="ae-type">1. What do you sell?</label></legend>
          <select class="select" id="ae-type" name="ae-type">
            <option value="">Choose your business</option>
            <option value="insulation">Insulation and energy upgrades</option>
            <option value="windows">Windows and doors</option>
            <option value="hvac">HVAC and heat pumps</option>
            <option value="roofing">Roofing and siding</option>
            <option value="reno">Kitchens, baths and renovation</option>
            <option value="outdoor">Decks, fences and outdoor living</option>
            <option value="other">Other home services</option>
          </select>
        </fieldset>
        <fieldset><legend>2. Annual revenue</legend><div class="opts">
          <label class="opt"><input type="radio" name="ae-rev" value="r1"><span>Under $500K</span></label>
          <label class="opt"><input type="radio" name="ae-rev" value="r2"><span>$500K&ndash;1M</span></label>
          <label class="opt"><input type="radio" name="ae-rev" value="r3"><span>$1&ndash;3M</span></label>
          <label class="opt"><input type="radio" name="ae-rev" value="r4"><span>$3&ndash;10M</span></label>
          <label class="opt"><input type="radio" name="ae-rev" value="r5"><span>Over $10M</span></label>
        </div></fieldset>
        <fieldset><legend>3. Your goal for next year</legend><div class="opts">
          <label class="opt"><input type="radio" name="ae-goal" value="hold"><span>Hold steady</span></label>
          <label class="opt"><input type="radio" name="ae-goal" value="grow"><span>Grow steadily</span></label>
          <label class="opt"><input type="radio" name="ae-goal" value="fast"><span>Grow fast</span></label>
        </div></fieldset>
        <fieldset><legend>4. Where you work</legend><div class="opts">
          <label class="opt"><input type="radio" name="ae-market" value="town"><span>One town</span></label>
          <label class="opt"><input type="radio" name="ae-market" value="region"><span>A region</span></label>
          <label class="opt"><input type="radio" name="ae-market" value="multi"><span>Several markets</span></label>
        </div></fieldset>
        <fieldset><legend>5. Average job size</legend><div class="opts">
          <label class="opt"><input type="radio" name="ae-ticket" value="low"><span>Under $2K</span></label>
          <label class="opt"><input type="radio" name="ae-ticket" value="mid"><span>$2&ndash;10K</span></label>
          <label class="opt"><input type="radio" name="ae-ticket" value="high"><span>$10&ndash;30K</span></label>
          <label class="opt"><input type="radio" name="ae-ticket" value="top"><span>Over $30K</span></label>
        </div></fieldset>
      </form>
      <div class="tool-out">
        <div class="ae-result" aria-live="polite"></div>
        <form class="form tool-gate ae-gate" novalidate hidden>
          <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
          <h3>See your channel mix</h3>
          <p>Where the budget should go, by channel. Free, and Jared will follow up personally, not a mailing list.</p>
          <div class="field-row">
            <div class="field"><label for="ae-name">Name</label><input id="ae-name" name="ae-name" autocomplete="name"></div>
            <div class="field"><label for="ae-email">Email</label><input id="ae-email" name="ae-email" type="email" autocomplete="email"></div>
          </div>
          <div class="field"><label for="ae-business">Business name</label><input id="ae-business" name="ae-business" autocomplete="organization"></div>
          <div class="btn-row"><button class="btn btn-solid" type="submit">Show my channel mix</button></div>
          <p class="form-status" hidden></p>
        </form>
      </div>
    </div>
    <p class="ledger-note">A rule-of-thumb starting point for owner-run home improvement businesses, based on revenue, growth goals and market size. It isn't a media plan.</p>
  </div>
</div></section>

<section class="band on-paper"><div class="wrap">
  <div class="section-head">
    <div class="eyebrow">What we do</div>
    <h2>Four ways to get more from your ad spend.</h2>
  </div>
  <div class="services services-2">
    <div class="service"><h3>Contract and agency review</h3><p>Bring your invoices. We read every contract and bill so you know what you're paying for and whether you're getting it.</p>
      <ul><li>Media and agency invoices, line by line</li><li>Contract terms, auto-renewals and exit clauses</li><li>Management fees and markups</li><li>A plain report: keep, renegotiate or cut</li></ul></div>
    <div class="service"><h3>Media plans</h3><p>A budget and channel plan built around your revenue, season and goals.</p>
      <ul><li>Budget set from revenue and growth goals</li><li>Channel mix and seasonal schedule</li><li>Cost-per-lead targets for each channel</li><li>A plan you can take to any vendor</li></ul></div>
    <div class="service"><h3>Digital ad campaigns</h3><p>Search and social campaigns that send homeowners to your website tools and quote forms.</p>
      <ul><li>Google search and Meta (Facebook and Instagram)</li><li>Built around your rebate finder or estimator</li><li>Call and form tracking from day one</li><li>Monthly report in plain numbers</li></ul></div>
    <div class="service"><h3>Digital ad training</h3><p>Rather run your own ads? We'll teach you or your team to do it well, one-on-one or in a group.</p>
      <ul><li>Google Ads and Meta ads, step by step</li><li>Setting budgets and reading the results</li><li>Campaign strategy and optimization</li><li>Hands-on, using your own accounts</li></ul></div>
  </div>
</div></section>

<section class="band band-night"><div class="wrap split">
  <div class="copy">
    <div class="eyebrow">Where the money goes</div>
    <h2>We read your marketing like a ledger.</h2>
    <p>Before we recommend anything, we line up every advertising cost against what it produced. Most businesses find at least one line nobody can explain.</p>
    <p>From there the plan is simple: keep what earns, fix what could, and stop paying for what doesn't.</p>
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
    <div class="ledger-note">Illustrative figures for a local window and door company. In a real review these come from your own invoices and reports.</div>
  </div>
</div></section>

<section class="band band-dark"><div class="wrap">
  <div class="section-head">
    <div class="eyebrow">How a review works</div>
    <h2>From a pile of invoices to a clear plan.</h2>
  </div>
  <ol class="steps">
    <li><h3>Send</h3><p>Email your last three to six months of ad invoices, contracts and any reports you get.</p></li>
    <li><h3>Review</h3><p>We line up each cost against what it produced and check the terms you signed.</p></li>
    <li><h3>Report</h3><p>A short, plain-language read-out: what to keep, renegotiate and stop.</p></li>
    <li><h3>Plan</h3><p>A media plan for the budget you have, aimed at cost per lead.</p></li>
    <li><h3>Launch</h3><p>We run the digital campaigns, or hand the plan to your team and train them to run it.</p></li>
  </ol>
</div></section>
''' + cta("Bring your invoices.",
          "Book a free 30-minute call. Send your last few ad invoices beforehand and we'll tell you what we see.",
          "Book a review call")

ABOUT = '''<section class="page-hero">
  <img class="ghost-mark" src="assets/emblem-light.png" alt="" width="256" height="224">
  <div class="wrap">
    <div class="eyebrow">About Town Talk</div>
    <h1>Marketing, made simple again.</h1>
    <p>Town Talk Marketing Solutions is an independent consultancy that helps home improvement businesses win more leads from their websites and get more from what they spend on advertising.</p>
  </div>
</section>

<section class="band on-paper"><div class="wrap split">
  <div class="copy" style="gap:1.25rem">
    <div class="eyebrow">Why we exist</div>
    <h2>Owners deserve a straight answer.</h2>
  </div>
  <div style="display:grid;gap:1.25rem;font-size:1.1rem">
    <p>Most business owners are pitched by a dozen media reps, platforms and agencies, each sure their channel is the answer. Few of them can say what the last campaign actually returned.</p>
    <p>Town Talk sits on your side of the table. We build simple tools that turn website visitors into leads, review the advertising contracts you already have, and help you understand where your marketing dollars are going and what they achieve.</p>
    <p>We start small and prove it: one tool, one review, one campaign. If it works, we grow from there together.</p>
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
      <li>A builder of simple tools that bring in leads</li>
      <li>A strategist who explains the numbers</li>
      <li>Flexible, so you pay only for what you use</li>
    </ul></div>
    <div class="no"><h3>What we are not</h3><ul>
      <li>A full-service ad agency</li>
      <li>Locked into long retainers</li>
      <li>A reseller of any one platform</li>
      <li>Fifty-slide decks and jargon</li>
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
      <p style="color:var(--muted-light)">For an advertising review, bring your last three months of ad invoices, contracts or reports. For a website tool, think about the question your customers ask most.</p>
    </div>
  </div>
  <form class="form" id="contact-form" novalidate>
    <input type="checkbox" name="botcheck" id="cf-botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
    <h2>Book a free call</h2>
    <div class="field-row">
      <div class="field"><label for="cf-name">Your name</label><input id="cf-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="cf-business">Business</label><input id="cf-business" name="business" autocomplete="organization"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="cf-email">Email</label><input id="cf-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="cf-phone">Phone</label><input id="cf-phone" name="phone" type="tel" autocomplete="tel"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="cf-interest">Interested in</label>
        <select id="cf-interest" name="interest"><option value="">Choose one</option><option>A lead tool for my website</option><option>Ad contract or agency review</option><option>A media plan</option><option>Digital ad campaigns</option><option>Google or Meta ads training</option><option>Not sure yet</option></select></div>
      <div class="field"><label for="cf-spend">Monthly ad spend</label>
        <select id="cf-spend" name="spend"><option value="">Choose a range</option><option>Under $1,000</option><option>$1,000 to $5,000</option><option>$5,000 to $15,000</option><option>Over $15,000</option><option>Not sure</option></select></div>
    </div>
    <div class="field"><label for="cf-msg">What would you like help with?</label><textarea id="cf-msg" name="message"></textarea></div>
    <div class="btn-row"><button class="btn btn-solid" type="submit">Send request</button></div>
    <p class="form-status" id="cf-status" hidden></p>
  </form>
</div></section>
'''

BODIES = {"home": HOME, "technology": TECHNOLOGY, "advertising": ADVERTISING, "about": ABOUT, "contact": CONTACT}

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

PAGE_SCRIPTS = {"technology": ["rebate-finder.js"], "advertising": ["ad-estimator.js"]}

# Old URLs (the Services page was replaced by Technology and Advertising).
REDIRECTS = """/services /advertising 301
/services.html /advertising 301
"""


def fill(html, mode):
    for k, file, _ in PAGES:
        html = html.replace("{{" + k + "}}", file if mode == "dist" else "#" + k)
    return html.replace("{{web3forms_key}}", WEB3FORMS_KEY if mode == "dist" else "")


def build_dist():
    out = ROOT / "dist"
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(SRC / "assets", out / "assets")
    (out / "styles.css").write_text(CSS)
    for js in SCRIPTS:
        shutil.copy(SRC / js, out / js)
    (out / "_redirects").write_text(REDIRECTS)
    for k, file, label in PAGES:
        title = "Town Talk Marketing Solutions" if k == "home" else f"{label} | Town Talk Marketing Solutions"
        scripts = "".join(f'<script src="{js}" defer></script>' for js in PAGE_SCRIPTS.get(k, []))
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
{scripts}
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
    keys = ",".join(f"'{k}'" for k, _, _ in PAGES)
    router = '''<script>
(function(){
  var pages=[__KEYS__];
  function show(){
    var raw=(location.hash||'').slice(1), h=raw, anchor=null;
    if(pages.indexOf(h)<0){
      var el=raw&&document.getElementById(raw), host=el&&el.closest('[data-page]');
      h=host?host.getAttribute('data-page'):'home'; anchor=el;
    }
    document.querySelectorAll('[data-page]').forEach(function(el){el.hidden=el.getAttribute('data-page')!==h;});
    if(anchor) anchor.scrollIntoView(); else window.scrollTo(0,0);
  }
  window.addEventListener('hashchange',show); show();
})();
</script>'''.replace("__KEYS__", keys)
    widget_js = "".join(f"<script>\n{(SRC / js).read_text()}</script>\n" for js in SCRIPTS)
    doc = f'''<title>Town Talk Website</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}
<style>
{CSS}
</style>
{"".join(sections)}
{FOOTER}
{PREVIEW_FORM_JS}
{widget_js}
{router}
'''
    # In the single-file preview, in-page links like "#demo" stay as they are; page links become "#page".
    doc = fill(doc, "preview").replace('href="#technology#demo"', 'href="#demo"').replace('href="#advertising#estimator"', 'href="#estimator"')
    (out / "index.html").write_text(doc)


if __name__ == "__main__":
    build_dist()
    build_preview()
    print("built dist/ and preview/")
