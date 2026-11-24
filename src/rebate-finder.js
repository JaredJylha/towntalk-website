/* Rebate finder demo (Technology page).
   A sample of the widget Town Talk builds for home improvement websites. Amounts are
   illustrative demo figures; a client's version uses the current programs for their area.
   The demo never sends the visitor's details anywhere: it shows the lead the business would receive. */
(function () {
  var root = document.getElementById('rebate-finder');
  if (!root) return;
  var qs = root.querySelector('.rf-questions');
  var out = root.querySelector('.rf-result');
  var gate = root.querySelector('.rf-gate');
  var lead = root.querySelector('.rf-lead');

  var UPGRADES = {
    attic: { label: 'Attic insulation', prov: 1000, insul: true },
    wall: { label: 'Wall insulation', prov: 2000, insul: true },
    basement: { label: 'Basement insulation', prov: 1200, insul: true },
    air: { label: 'Air sealing', prov: 300 },
    windows: { label: 'Windows and doors', prov: 500 },
    heatpump: { label: 'Heat pump', prov: 5000 }
  };
  var HOME = { detached: 'Detached house', attached: 'Semi or townhouse', mobile: 'Mobile or modular home' };
  var HEAT = { gas: 'Natural gas', electric: 'Electric', oil: 'Oil or propane', heatpump: 'Heat pump' };

  function money(n) { return '$' + Math.round(n).toLocaleString('en-CA'); }
  function picked(name) {
    return Array.prototype.map.call(qs.querySelectorAll('input[name="' + name + '"]:checked'), function (i) { return i.value; });
  }
  function esc(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

  var state = null;

  function calc() {
    var home = picked('rf-home')[0], heat = picked('rf-heat')[0], ups = picked('rf-up');
    if (!home || !heat || !ups.length) return null;
    var programs = [];
    var prov = 0;
    ups.forEach(function (k) {
      var v = UPGRADES[k].prov;
      if (k === 'heatpump') v = heat === 'heatpump' ? 0 : heat === 'gas' ? 2000 : 5000;
      if (k === 'wall' && home !== 'detached') v = 1400;
      prov += v;
    });
    if (prov) programs.push({ name: 'Provincial home renovation rebate', note: 'For the upgrades you picked', amount: prov });
    var insul = ups.filter(function (k) { return UPGRADES[k].insul; }).length;
    if (heat === 'gas' && insul) programs.push({ name: 'Gas utility insulation bonus', note: 'Because you heat with natural gas', amount: Math.min(750, 250 * insul) });
    if (ups.length >= 2 || ups.indexOf('air') > -1) programs.push({ name: 'Energy assessment rebate', note: 'Covers most of your before-and-after assessment', amount: 600 });
    var total = programs.reduce(function (s, p) { return s + p.amount; }, 0);
    if (total) programs.push({ name: 'Interest-free retrofit financing', note: 'Spread the rest over up to 10 years', text: 'Up to $40,000' });
    return { home: home, heat: heat, ups: ups, programs: programs, total: total };
  }

  function render(unlocked) {
    if (!state || !state.total) {
      out.innerHTML = '<p class="tool-empty">' + (state ? 'Those upgrades don’t match a rebate in this demo. Try adding insulation or air sealing.' : 'Answer the three questions to see what you may qualify for.') + '</p>';
      gate.hidden = true;
      return;
    }
    var rows = state.programs.map(function (p) {
      var val = p.text ? p.text : unlocked ? money(p.amount) : '<span class="locked" aria-label="Hidden until you request your report">$0,000</span>';
      return '<li><div><strong>' + p.name + '</strong><span>' + p.note + '</span></div><b>' + val + '</b></li>';
    }).join('');
    out.innerHTML =
      '<p class="tool-kicker">You may qualify for up to</p>' +
      '<p class="tool-big">' + money(state.total) + '</p>' +
      '<p class="tool-sub">across ' + (state.programs.length - 1) + ' rebate program' + (state.programs.length - 1 === 1 ? '' : 's') + ', plus financing</p>' +
      '<ul class="rf-programs">' + rows + '</ul>';
    gate.hidden = unlocked;
  }

  qs.addEventListener('change', function () {
    state = calc();
    lead.hidden = true;
    render(false);
  });

  gate.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = gate.elements;
    var msg = gate.querySelector('.form-status');
    if (!f['rf-name'].value.trim() || !f['rf-email'].value.trim() || !f['rf-email'].checkValidity()) {
      msg.textContent = 'Please add your name and a valid email address.';
      msg.hidden = false;
      return;
    }
    msg.hidden = true;
    render(true);
    var rows = [
      ['Name', f['rf-name'].value.trim()],
      ['Email', f['rf-email'].value.trim()],
      ['Phone', f['rf-phone'].value.trim() || '—'],
      ['Postal code', f['rf-postal'].value.trim().toUpperCase() || '—'],
      ['Home', HOME[state.home]],
      ['Heating', HEAT[state.heat]],
      ['Interested in', state.ups.map(function (k) { return UPGRADES[k].label; }).join(', ')],
      ['Rebates shown', money(state.total)],
      ['Wants an assessment', f['rf-book'].checked ? 'Yes, please call to book' : 'Not yet']
    ];
    lead.querySelector('tbody').innerHTML = rows.map(function (r) {
      return '<tr><th scope="row">' + r[0] + '</th><td>' + esc(r[1]) + '</td></tr>';
    }).join('');
    lead.hidden = false;
    lead.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  });

  render(false);
})();
