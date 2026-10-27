"""Frontend hardening: HTML escaping, URL allow-listing, CSP, and cache busting."""
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "site" / "app.js"
HTML = ROOT / "site" / "index.html"


class FrontendHardeningTests(unittest.TestCase):
    def test_resource_markup_escapes_text_and_blocks_non_http_urls(self):
        result = subprocess.run(["node", "-e", r'''
const fs=require("fs"), vm=require("vm"), assert=require("assert");
const source=fs.readFileSync("site/app.js","utf8");
const helpers=source.slice(source.indexOf("const ESCAPES"),source.indexOf("\n",source.indexOf("const safeUrl")));
const markup=source.slice(source.indexOf("function resourceMarkup"),source.indexOf("\n",source.indexOf("function resourceMarkup")));
const context={t:k=>k}; vm.createContext(context); vm.runInContext(helpers+"\n"+markup+"\nthis.esc=esc;this.safeUrl=safeUrl;this.resourceMarkup=resourceMarkup;",context);
assert.equal(context.esc(`<a href="x">'&`),"&lt;a href=&quot;x&quot;&gt;&#39;&amp;");
assert.equal(context.esc(null),"");
assert.equal(context.safeUrl("https://example.org/a?b=1&c=2"),"https://example.org/a?b=1&c=2");
assert.equal(context.safeUrl("http://example.org"),"http://example.org");
for(const bad of ["javascript:alert(1)"," JavaScript:alert(1)","data:text/html,x","//evil.example","#",undefined]) assert.equal(context.safeUrl(bad),"#");
const html=context.resourceMarkup([{url:"javascript:alert(1)",title:"<img src=x onerror=alert(1)>",publisher:"A & B"},{url:"https://ok.example/?a=1&b=\"2\"",title:"Fine",authority:"x"}]);
assert(!html.includes("<img"),html); assert(!html.includes("javascript:"),html);
assert(html.includes('href="#"'),html); assert(html.includes("A &amp; B"),html);
assert(html.includes('href="https://ok.example/?a=1&amp;b=&quot;2&quot;"'),html);
'''], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_index_html_declares_csp_canonical_and_accessible_buttons(self):
        html = HTML.read_text(encoding="utf-8")
        csp = re.search(r'<meta http-equiv="Content-Security-Policy" content="([^"]+)">', html)
        self.assertIsNotNone(csp)
        policy = csp.group(1)
        for directive in ("default-src 'self'", "script-src 'self'", "style-src 'self'", "connect-src 'self'", "object-src 'none'"):
            self.assertIn(directive, policy)
        self.assertNotIn("unsafe-inline", policy)
        self.assertNotIn("<script>", html)
        self.assertNotIn(" style=", html)
        self.assertIn('<link rel="canonical" href="https://yuema137.github.io/ble/">', html)
        for button_id in ("lang-en", "lang-zh", "theme-light", "theme-dark"):
            tag = re.search(rf'<button id="{button_id}"[^>]*>', html).group(0)
            self.assertIn('type="button"', tag)
        for button_id in ("theme-light", "theme-dark"):
            self.assertIn("aria-label=", re.search(rf'<button id="{button_id}"[^>]*>', html).group(0))

    def test_source_uses_dev_cache_tokens_only(self):
        html = HTML.read_text(encoding="utf-8")
        app = APP.read_text(encoding="utf-8")
        self.assertIn("styles.css?v=dev", html)
        self.assertIn("app.js?v=dev", html)
        self.assertIn('const DATA_VERSION = "dev";', app)
        self.assertNotRegex(app, r"\?v=\d{8}")
        self.assertNotRegex(html, r"\?v=\d{8}")

    def test_pages_snapshot_derives_cache_versions_from_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            outputs = []
            for name in ("a", "b"):
                output = Path(tmp) / name
                subprocess.run(["python3", "scripts/build_pages_snapshot.py", "--output", str(output), "--source-sha", "test"],
                               cwd=ROOT, check=True, capture_output=True)
                outputs.append(output)
            manifests = [json.loads((output / "manifest.json").read_text()) for output in outputs]
            self.assertEqual(manifests[0]["asset_versions"], manifests[1]["asset_versions"])
            versions = manifests[0]["asset_versions"]
            html = (outputs[0] / "index.html").read_text()
            app = (outputs[0] / "app.js").read_text()
            self.assertIn(f"styles.css?v={versions['styles']}", html)
            self.assertIn(f"app.js?v={versions['app']}", html)
            self.assertIn(f'const DATA_VERSION = "{versions["data"]}";', app)
            self.assertNotIn("?v=dev", html)
            self.assertTrue(all(re.fullmatch(r"[0-9a-f]{12}", value) for value in versions.values()))


if __name__ == "__main__":
    unittest.main()
