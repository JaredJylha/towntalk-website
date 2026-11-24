/* Insulation rebate calculator demo (Technology page).
   Jared's contractor tool, restyled for the Town Talk site. Estimates rebates under Ontario's
   Home Renovation Savings program (Enbridge / Save on Energy). The demo never sends anything:
   on submit it shows the lead a contractor's sales team would receive.
   Check every amount against homerenovationsavings.ca before a client launch; lines marked
   VERIFY could not be confirmed from public sources. */
(function () {
  var root = document.getElementById('rebate-finder');
  if (!root) return;

  var P = {
    deadline: 'March 31, 2027',
    checked: 'November 2026',
    standaloneAttic: { r12: 1250, r25: 1000, r35: 800, cathedral: 750, pctOfCost: 0.5 },
    bundleAttic: { r12: 1500, r25: 1200, r35: 900, cathedral: 780 },
    walls: { low: 1200, mid: 2100, high: 3600 },
    basement: { mid: 750 /* VERIFY */, high: 1500 },
    crawl: { wallMid: 600, wallHigh: 1200, ceiling: 600 /* VERIFY */ },
    header: 300, slab: 500, window: 100, air: 200,
    thirdBonus: 500, assessment: 600,
    caps: { gas: 5000, other: 10000 } /* VERIFY whether cap includes bonus/assessment */
  };
  var LABEL = { attic: 'Attic insulation', walls: 'Exterior walls', basement: 'Basement walls', crawl: 'Crawl space',
    header: 'Rim joists / header', slab: 'Basement slab', windows: 'Windows and doors', air: 'Air sealing' };
  var HOME = { detached: 'Detached', semi: 'Semi-detached', row: 'Row or townhouse', mobile: 'Mobile home on foundation', stacked: 'Stacked townhouse or condo' };
  var HEAT = { gas: 'Natural gas (Enbridge)', 'gas-other': 'Natural gas (other utility)', electric: 'Electricity', oil: 'Oil', propane: 'Propane', wood: 'Wood' };
  // Foundation items count as one upgrade toward the 2- and 3-upgrade thresholds (conservative).
  var GROUP = { basement: 'foundation', crawl: 'foundation', header: 'foundation', slab: 'foundation' };

  function $(s) { return root.querySelector(s); }
  function $$(s) { return Array.prototype.slice.call(root.querySelectorAll(s)); }
  function val(n) { var i = root.querySelector('input[name="rb-' + n + '"]:checked'); return i ? i.value : undefined; }
  function money(n) { return '$' + Math.round(n).toLocaleString('en-CA'); }
  function esc(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
  function selected() { return $$('.rb-upg-head input:checked').map(function (i) { return i.value; }); }
  function hasFoundationWall(sel) { return sel.indexOf('basement') > -1 || sel.indexOf('crawl') > -1; }
  function has(sel, k) { return sel.indexOf(k) > -1; }

  $('#rb-fine').textContent = 'Estimate only, based on published program amounts as of ' + P.checked +
    '. Final rebates are confirmed by the program after your Energy Advisor’s follow-up assessment. The program runs to ' +
    P.deadline + ' and can end early. Work must not start before your first assessment.';

  var estimate = { total: 0, lines: [], path: '' };

  function calc() {
    var sel = selected(), notes = [], lines = [], total = 0, path = '';
    var postal = $('#rb-postal').value.trim().toUpperCase();
    if (postal && !/^[KLMNP]/.test(postal)) return stop('This program is for Ontario homes. Check your postal code.');
    if (val('own') === 'renter') return stop('Rebates go to the property owner. Ask your landlord, who can apply for a rental home.');
    if (val('htype') === 'stacked') return stop('Stacked townhouses and condo units aren’t eligible for this program.');
    if (val('heat') === 'gas-other') return stop('Gas-heated homes need to be Enbridge Gas customers to qualify.');
    if (!sel.length) return render(0, [], 'Choose an upgrade to see your estimate.', []);

    var gas = val('heat') === 'gas';
    var atticNow = val('atticNow'), atticType = val('atticType');
    var units = {};
    sel.forEach(function (s) { if (!(s === 'header' && !hasFoundationWall(sel))) units[GROUP[s] || s] = 1; });
    if (has(sel, 'header') && !hasFoundationWall(sel)) notes.push('Rim joist insulation only qualifies alongside basement or crawl space wall work.');
    if (has(sel, 'attic') && atticType === 'standard' && atticNow === 'full') notes.push('Attics already above R-35 don’t qualify for the attic rebate.');
    var atticOk = has(sel, 'attic') && !(atticType === 'standard' && atticNow === 'full');
    if (!atticOk) delete units.attic;
    var count = Object.keys(units).length;

    // Path A: attic on its own, no assessment needed
    if (count === 1 && units.attic) {
      var amt = atticType === 'cathedral' ? P.standaloneAttic.cathedral : P.standaloneAttic[atticNow];
      var cost = parseFloat($('#rb-atticCost').value);
      if (cost > 0 && cost * P.standaloneAttic.pctOfCost < amt) {
        amt = cost * P.standaloneAttic.pctOfCost;
        notes.push('The attic-only rebate covers up to half the project cost.');
      }
      lines.push(['Attic insulation', amt]);
      var bundleAmt = (atticType === 'cathedral' ? P.bundleAttic.cathedral : P.bundleAttic[atticNow]) + P.assessment;
      notes.push('Adding a second upgrade with an energy assessment would raise the attic portion to about ' + money(bundleAmt) + ' including the assessment rebate.');
      return render(amt, lines, 'Attic-only path: no energy assessment needed.', notes);
    }

    if (count < 2) {
      notes.push('Add one more upgrade, such as attic insulation, to unlock these rebates.');
      return render(0, [], 'Most insulation rebates need two or more upgrades.', notes);
    }

    // Path B: bundle with energy assessment
    var measures = 0;
    function add(k, a) { lines.push([LABEL[k], a]); measures += a; }
    if (atticOk) add('attic', atticType === 'cathedral' ? P.bundleAttic.cathedral : P.bundleAttic[atticNow]);
    if (has(sel, 'walls')) add('walls', P.walls[val('walls')]);
    if (has(sel, 'basement')) add('basement', P.basement[val('basement')]);
    if (has(sel, 'crawl')) add('crawl', P.crawl[val('crawl')]);
    if (has(sel, 'header') && hasFoundationWall(sel)) add('header', P.header);
    if (has(sel, 'slab')) add('slab', P.slab);
    if (has(sel, 'windows')) {
      var n = Math.max(0, parseInt($('#rb-windowCount').value, 10) || 0);
      if (n < 3) notes.push('Windows need at least three openings, or one door or skylight.');
      add('windows', n * P.window);
    }
    if (has(sel, 'air')) { add('air', P.air); notes.push('Air sealing is paid only if the target is met, so it’s safest as a third upgrade.'); }
    var cap = gas ? P.caps.gas : P.caps.other;
    if (measures > cap) { lines.push(['Program maximum applied', cap - measures]); measures = cap; }
    if (count >= 3) lines.push(['Bonus for three upgrades', P.thirdBonus]);
    lines.push(['Energy assessments', P.assessment]);
    total = measures + (count >= 3 ? P.thirdBonus : 0) + P.assessment;
    path = 'Bundle path: ' + count + ' upgrades with a before-and-after energy assessment.';
    if (count === 2) notes.push('A third upgrade adds a ' + money(P.thirdBonus) + ' bonus.');
    return render(total, lines, path, notes);
  }

  function stop(msg) { render(0, [], 'Not eligible as entered.', [msg], true); }

  function render(total, lines, path, notes, blocked) {
    $('#rb-total').textContent = money(total);
    $('#rb-path').textContent = path;
    $('#rb-lines').innerHTML = lines.map(function (l) {
      return '<li><span>' + l[0] + '</span><span>' + (l[1] < 0 ? '−' + money(-l[1]) : money(l[1])) + '</span></li>';
    }).join('');
    $('#rb-notes').innerHTML = notes.map(function (n) { return '<p class="rb-note' + (blocked ? ' rb-stop' : '') + '">' + n + '</p>'; }).join('');
    $('#rb-quoteBtn').disabled = total <= 0;
    var sel = blocked ? [] : selected();
    $$('.rb-zone').forEach(function (z) {
      var k = z.getAttribute('data-z');
      var on = has(sel, k) || (k === 'basement' && has(sel, 'crawl') && val('crawl') !== 'ceiling') ||
        (k === 'header' && has(sel, 'crawl') && val('crawl') === 'ceiling');
      z.classList.toggle('on', on);
    });
    estimate = { total: total, lines: lines, path: path };
  }

  $$('.rb-upg-head input').forEach(function (cb) {
    cb.addEventListener('change', function () { cb.closest('.rb-upg').classList.toggle('open', cb.checked); });
  });
  root.addEventListener('change', function (e) {
    if (e.target.name === 'rb-atticType') $('#rb-atticLevelQ').style.display = val('atticType') === 'cathedral' ? 'none' : '';
  });
  var main = $('.rb-main');
  main.addEventListener('input', calc);
  main.addEventListener('change', calc);

  $('#rb-quoteBtn').addEventListener('click', function () {
    $('#rb-lead').hidden = false; $('#rb-quoteBtn').hidden = true; $('#rb-lname').focus();
  });

  $('#rb-lead').addEventListener('submit', function (e) {
    e.preventDefault();
    var err = $('#rb-leadErr');
    var name = $('#rb-lname').value.trim(), email = $('#rb-lemail').value.trim();
    if (!name || !/^\S+@\S+\.\S+$/.test(email)) { err.textContent = 'Enter your name and a valid email.'; err.hidden = false; return; }
    if (!$('#rb-lconsent').checked) { err.textContent = 'Check the consent box so we can contact you.'; err.hidden = false; return; }
    err.hidden = true;
    var rows = [
      ['Name', name], ['Email', email], ['Phone', $('#rb-lphone').value.trim() || '—'],
      ['Postal code', $('#rb-postal').value.trim().toUpperCase() || '—'],
      ['Home', HOME[val('htype')]], ['Heating', HEAT[val('heat')]],
      ['Upgrades', selected().map(function (k) { return LABEL[k]; }).join(', ')],
      ['Estimated rebate', money(estimate.total)], ['Path', estimate.path]
    ];
    var lead = root.querySelector('.rf-lead');
    lead.querySelector('tbody').innerHTML = rows.map(function (r) { return '<tr><th scope="row">' + r[0] + '</th><td>' + esc(r[1]) + '</td></tr>'; }).join('');
    $('#rb-lead').hidden = true; $('#rb-sent').hidden = false; lead.hidden = false;
    lead.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  });

  calc();
})();
