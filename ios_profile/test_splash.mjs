// Deterministic navigation/session tests; does not pretend to be an iOS browser.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const html = readFileSync(process.argv[2] || new URL("./index.html", import.meta.url), "utf8");
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const key = "trumsublike.ios.splash.v1";
function launch({ storage = new Map(), blocked = false, reduced = false, search = "" } = {}) {
  let now = 0, nextId = 0;
  const pending = new Map(), events = {}, classes = new Set(), redirects = [];
  const link = { hidden: true };
  vm.runInNewContext(script, {
    URLSearchParams,
    location: { search, replace(url) { redirects.push({ url, at: now }); } },
    sessionStorage: {
      getItem(k) { if (blocked) throw new Error("blocked"); return storage.get(k) ?? null; },
      setItem(k, v) { if (blocked) throw new Error("blocked"); storage.set(k, v); },
    },
    document: {
      getElementById: () => link,
      body: { classList: { add(...names) { names.forEach(n => classes.add(n)); },
        remove(...names) { names.forEach(n => classes.delete(n)); } } },
    },
    window: { matchMedia: () => ({ matches: reduced }),
      addEventListener(name, callback) { events[name] = callback; } },
    setTimeout(callback, delay) { pending.set(++nextId, { callback, at: now + delay }); return nextId; },
    clearTimeout(id) { pending.delete(id); },
  });
  return { redirects, events, classes, storage, link,
    advance(to) {
      for (;;) {
        const task = [...pending].filter(([, t]) => t.at <= to).sort((a, b) => a[1].at - b[1].at)[0];
        if (!task) break;
        pending.delete(task[0]); now = task[1].at; task[1].callback();
      }
      now = to;
    } };
}

const first = launch();
assert.equal(first.storage.get(key), "seen");
first.advance(1480);
assert(first.classes.has("leaving"));
assert.equal(first.redirects.length, 0);
first.advance(1800);
assert.deepEqual(first.redirects, [{ url: "https://trumsublike.com", at: 1800 }]);
const repeat = launch({ storage: first.storage });
assert.equal(repeat.redirects[0].at, 0);
assert(repeat.classes.has("skip"));
const restricted = launch({ blocked: true });
restricted.advance(1800);
assert.equal(restricted.redirects.length, 1);
const reduced = launch({ reduced: true });
reduced.advance(180);
assert.equal(reduced.redirects[0].at, 180);
const preview = launch({ search: "?preview=1" });
preview.advance(10000);
assert.equal(preview.redirects.length, 0);
assert.equal(preview.storage.size, 0);
assert.equal(preview.link.hidden, false);
const restored = launch();
restored.events.pagehide();
restored.advance(2000);
assert.equal(restored.redirects.length, 0);
restored.events.pageshow({ persisted: true });
assert.equal(restored.redirects.length, 1);
console.log("PASS: 6 navigation/session cases (fresh, repeat, storage denied, reduced motion, preview, restored).");
