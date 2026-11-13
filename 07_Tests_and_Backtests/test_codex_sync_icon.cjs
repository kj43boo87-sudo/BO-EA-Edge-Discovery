const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
for (const name of ['ChatGPT_Scout_Champ_Codex_v5.1.user.js', 'Gemini_Spark_Codex_v5.1.user.js']) {
  const source = fs.readFileSync(path.join(__dirname, '../06_Tampermonkey_UI', name), 'utf8');
  const start = source.indexOf('    // Codex Desktop uses');
  const end = source.indexOf("    const toggleBtn =", start);
  assert.ok(start >= 0 && end > start);
  for (const returnedWindow of [null, {opener: {}}]) {
    const calls = [];
    const button = {style: {}, setAttribute(k, v) {this[k] = v;}, addEventListener(event, callback) {assert.equal(event, 'click'); this.click = callback;}};
    const badge = {};
    vm.runInNewContext(source.slice(start, end), {
      document: {createElement(tag) {assert.equal(tag, 'button'); return button;}},
      toolbar: {appendChild(value) {assert.equal(value, button);}},
      statusBadge: badge,
      window: {open(...args) {calls.push(args); return returnedWindow;}}
    });
    assert.equal(calls.length, 0, 'Must not open or share on page load');
    assert.equal(button['aria-label'], button.title);
    button.click();
    assert.deepEqual(calls, [['http://127.0.0.1:5001/', '_blank', 'noopener,noreferrer']]);
    assert.ok(badge.textContent.includes('対象チャット'));
    if (returnedWindow) assert.equal(returnedWindow.opener, null);
  }
  console.log(name + ': click, accessible label, isolated tab, null return passed');
}
