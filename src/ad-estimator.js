/* Ad budget estimator (Advertising page).
   Shows a recommended monthly ad budget range straight away, and the channel mix once the
   visitor leaves an email. The email, answers and results go to Jared through Web3Forms.
   The figures are rules of thumb for owner-run home improvement businesses, not a media plan. */
(function () {
  var root = document.getElementById('ad-estimator');
  if (!root) return;
  var qs = root.querySelector('.ae-questions');
  var out = root.querySelector('.ae-result');
  var gate = root.querySelector('.ae-gate');
  var KEY = root.getAttribute('data-key') || '';

  var TYPES = {
    insulation: 'Insulation and energy upgrades', windows: 'Windows and doors', hvac: 'HVAC and heat pumps',
    roofing: 'Roofing and siding', reno: 'Kitchens, baths and renovation', outdoor: 'Decks, fences and outdoor living',
    other: 'Other home services'
  };
  var REVENUE = { r1: [350000, 'Under $500K'], r2: [750000, '$500K to $1M'], r3: [2000000, '$1M to $3M'], r4: [5000000, '$3M to $10M'], r5: [12000000, 'Over $10M'] };
  var GOAL = { hold: [0.03, 0.05, 'Hold steady'], grow: [0.05, 0.08, 'Grow steadily'], fast: [0.08, 0.12, 'Grow fast'] };
  var MARKET = { town: [0.9, 'One town'], region: [1, 'A region'], multi: [1.15, 'Several markets'] };
  var TICKET = { low: 'Under $2K', mid: '$2K to $10K', high: '$10K to $30K', top: 'Over $30K' };
  var CHANNELS = [
    ['search', 'Search ads', 'Google and Bing, for people already looking'],
    ['social', 'Social ads', 'Facebook and Instagram, to build demand'],
    ['retarget', 'Retargeting and video', 'Bring back visitors who didn’t call'],
    ['local', 'Local media', 'Radio, print, flyers and outdoor'],
    ['shows', 'Home shows and events', 'Face-to-face trust for bigger jobs']
  ];
  var TYPE_SHIFT = {
    insulation: { search: 10, local: -5, shows: -5 }, hvac: { search: 10, local: -5, shows: -5 },
    roofing: { search: 10, social: -5, shows: -5 }, windows: { shows: 5, social: -5 },
    reno: { social: 10, search: -5, local: -5 }, outdoor: { social: 10, search: -5, shows: 5, local: -10 }, other: {}
  };

  function money(n) {
    var step = n < 2000 ? 50 : n < 20000 ? 100 : 1000;
    return '$' + (Math.round(n / step) * step).toLocaleString('en-CA');
  }
  function val(name) { var i = qs.querySelector('[name="' + name + '"]:checked, select[name="' + name + '"]'); return i ? i.value : ''; }

  var state = null, unlocked = false;

  function calc() {
    var a = { type: val('ae-type'), rev: val('ae-rev'), goal: val('ae-goal'), market: val('ae-market'), ticket: val('ae-ticket') };
    if (!a.type || !a.rev || !a.goal || !a.market || !a.ticket) return null;
    var rev = REVENUE[a.rev][0], g = GOAL[a.goal], m = MARKET[a.market][0];
    var low = rev * g[0] / 12 * m, high = rev * g[1] / 12 * m;
    var mix = { search: 35, social: 25, retarget: 10, local: 20, shows: 10 };
    function shift(s) { for (var k in s) mix[k] += s[k]; }
    shift(TYPE_SHIFT[a.type]);
    if (a.market === 'town') shift({ local: 5, search: -5 });
    if (a.market === 'multi') shift({ search: 5, local: -5 });
    if (a.ticket === 'high' || a.ticket === 'top') shift({ retarget: 5, shows: 5, search: -5, social: -5 });
    if (a.ticket === 'low') shift({ search: 5, shows: -5 });
    if ((low + high) / 2 < 3000) { mix.search += mix.shows; mix.shows = 0; }
    var total = 0;
    for (var k in mix) { mix[k] = Math.max(0, mix[k]); total += mix[k]; }
    var sum = 0, top = 'search';
    for (k in mix) { mix[k] = Math.round(mix[k] / total * 20) * 5; sum += mix[k]; if (mix[k] > mix[top]) top = k; }
    mix[top] += 100 - sum;
    return { a: a, low: low, high: high, mix: mix };
  }

  function render() {
    if (!state) {
      out.innerHTML = '<p class="tool-empty">Answer the five questions to see your recommended monthly budget.</p>';
      gate.hidden = true;
      return;
    }
    var bars = CHANNELS.map(function (c, i) {
      var pct = state.mix[c[0]];
      if (unlocked && !pct) return '';
      var w = unlocked ? pct : [70, 55, 40, 30, 20][i];
      return '<li class="' + (unlocked ? '' : 'is-locked') + '"><div class="mix-label"><strong>' + (unlocked ? c[1] : 'Channel ' + (i + 1)) + '</strong>' +
        (unlocked ? '<span>' + c[2] + '</span>' : '') + '</div><div class="mix-bar"><i style="width:' + w + '%"></i></div><b>' +
        (unlocked ? pct + '%' : '??%') + '</b></li>';
    }).join('');
    var spread = unlocked
      ? '<p class="tool-note">On ' + money((state.low + state.high) / 2) + ' a month, search alone would be about ' + money((state.low + state.high) / 2 * state.mix.search / 100) + '. A full media plan sets the schedule, targets and cost per lead for each line.</p>' +
        '<div class="btn-row"><a class="btn btn-solid" href="' + (root.getAttribute('data-contact') || 'contact.html') + '">Get a full media plan</a></div>'
      : '';
    out.innerHTML =
      '<p class="tool-kicker">Recommended advertising budget</p>' +
      '<p class="tool-big">' + money(state.low) + '<span> to </span>' + money(state.high) + '</p>' +
      '<p class="tool-sub">per month, or ' + money(state.low * 12) + ' to ' + money(state.high * 12) + ' a year</p>' +
      '<div class="mix"><p class="tool-kicker">' + (unlocked ? 'Suggested channel mix' : 'Your channel mix is ready') + '</p><ul>' + bars + '</ul></div>' + spread;
    gate.hidden = unlocked;
  }

  qs.addEventListener('change', function () { state = calc(); render(); });

  gate.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = gate.elements, msg = gate.querySelector('.form-status'), btn = gate.querySelector('button');
    function say(t) { msg.textContent = t; msg.hidden = !t; }
    if (!f['ae-name'].value.trim() || !f['ae-email'].value.trim() || !f['ae-email'].checkValidity()) { say('Please add your name and a valid email address.'); return; }
    if (f.botcheck.checked) return;
    unlocked = true;
    render();
    out.querySelector('.mix').scrollIntoView({ behavior: 'smooth', block: 'center' });
    if (!KEY) { say(''); return; }
    var a = state.a, mixText = CHANNELS.map(function (c) { return c[1] + ': ' + state.mix[c[0]] + '%'; }).join(', ');
    var data = {
      access_key: KEY,
      subject: 'Ad budget estimator lead: ' + f['ae-name'].value.trim() + (f['ae-business'].value.trim() ? ' (' + f['ae-business'].value.trim() + ')' : ''),
      from_name: 'Town Talk website',
      replyto: f['ae-email'].value.trim(),
      name: f['ae-name'].value.trim(),
      email: f['ae-email'].value.trim(),
      business: f['ae-business'].value.trim(),
      business_type: TYPES[a.type], annual_revenue: REVENUE[a.rev][1], goal: GOAL[a.goal][2],
      market: MARKET[a.market][1], average_job: TICKET[a.ticket],
      budget_shown: money(state.low) + ' to ' + money(state.high) + ' per month',
      channel_mix_shown: mixText,
      email_updates: f['ae-updates'].checked ? 'Yes' : 'No',
      source: 'Ad budget estimator, Advertising page'
    };
    btn.disabled = true;
    (window.ttCaptcha ? window.ttCaptcha() : Promise.resolve(''))
      .then(function (t) {
        if (t) data.recaptcha_response = t;
        return fetch('https://api.web3forms.com/submit', { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data) });
      })
      .then(function (r) { return r.json(); })
      .then(function (j) { if (!j.success) throw 0; })
      .catch(function () { /* the visitor still gets their result */ })
      .finally(function () { btn.disabled = false; });
  });

  render();
})();
