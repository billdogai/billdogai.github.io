"""Generate the billdogai.github.io index.html from the codelab metadata."""
import html, json, sys

src, out = sys.argv[1], sys.argv[2]
labs = json.load(open(src))
V = "1.1.1-beta.5"
SITE = "https://billdog.io"
UTM = "?utm_source=github_pages&utm_medium=referral&utm_campaign=codelabs"

PLATFORM = {"ios": "iOS", "android": "Android", "flutter": "Flutter", "react-native": "React Native", "web": "Web", "any": "Any platform"}
ICON = {"Get started": "🚀", "Testing": "🧪", "Experiments": "⚗️", "AI agents": "🤖"}

def e(s): return html.escape(s, quote=True)

cards = []
for c in labs:
    url = f"{SITE}/codelabs/{c['slug']}{UTM}"
    cards.append(f"""      <a class="card" href="{e(url)}" data-platform="{e(c['platform'])}">
        <div class="card-top"><span class="tag">{ICON[c['category']]} {e(c['category'])}</span><span class="plat">{e(PLATFORM[c['platform']])}</span></div>
        <h3>{e(c['title'])}</h3>
        <p>{e(c['summary'])}</p>
        <div class="card-foot"><span>⏱ {c['minutes']} min · {e(c['level'])}</span><span class="go">Start codelab →</span></div>
      </a>""")

INSTALL = [
    ("ios", "iOS", "Swift Package Manager", f'.package(url: "https://github.com/billdogai/billdog-ios-spm.git", from: "{V}")', "/docs/ios"),
    ("android", "Android", "app/build.gradle.kts", f'implementation("io.billdog:billdog-compose:{V}")\nimplementation("io.billdog:billdog-paywall:{V}") // Google Play Billing', "/docs/android"),
    ("flutter", "Flutter", "Terminal", f"flutter pub add billdog_flutter:^{V}", "/docs/flutter"),
    ("rn", "React Native", "Terminal", f"npm install @billdog.io/react-native@^{V} \\\n  @react-native-async-storage/async-storage@^1.19.0 \\\n  react-native-fs@^2.20.0 react-native-svg@^13.0.0 react-native-webview@^13.0.0", "/docs/react-native"),
    ("web", "Web", "Terminal", f"npm install @billdog.io/web@^{V}", "/docs/web"),
]
tabs = "".join(f'<button role="tab" aria-selected="{"true" if i == 0 else "false"}" aria-controls="ins-{k}" id="tab-{k}" data-tab="{k}">{e(n)}</button>' for i, (k, n, *_ ) in enumerate(INSTALL))
panels = "".join(
    f"""<div role="tabpanel" id="ins-{k}" aria-labelledby="tab-{k}"{'' if i == 0 else ' hidden'}>
          <div class="code"><div class="code-bar"><span>{e(label)}</span><button class="copy" type="button">Copy</button></div><pre><code>{e(code)}</code></pre></div>
          <p class="small">Full guide: <a href="{SITE}{doc}{UTM}">billdog.io{doc}</a></p>
        </div>"""
    for i, (k, n, label, code, doc) in enumerate(INSTALL))

REPOS = [
    ("billdog-mcp", "MCP server: set up paywalls, subscriptions, A/B tests and analytics from Claude Code, Cursor and other AI coding agents."),
    ("billdog-ios-spm", "iOS SDK (Swift Package Manager): paywalls, in-app subscriptions, analytics and A/B tests for iOS apps."),
    ("billdog-ios-superwall", "Superwall PurchaseController that runs every Superwall paywall purchase and restore through BillDog."),
    ("billdog-android-full", "BillDog Full SDK for Android: compiled AAR artifacts (paywalls, subscriptions, analytics)."),
    ("billdog-android-eng", "BillDog Eng SDK for Android: compiled AAR artifacts."),
    ("billdogeng-go", "Server SDK for Go: analytics, feature flags, surveys, messaging and LLM observability."),
    ("billdogeng-php", "Server SDK for PHP: analytics, feature flags, surveys, messaging and LLM observability."),
]
repos = "\n".join(f"""      <a class="repo" href="https://github.com/billdogai/{r}"><span class="repo-name">billdogai/{e(r)}</span><span>{e(d)}</span></a>""" for r, d in REPOS)

ld = json.dumps({
    "@context": "https://schema.org", "@type": "ItemList", "name": "BillDog codelabs",
    "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": c["title"], "url": f"{SITE}/codelabs/{c['slug']}"} for i, c in enumerate(labs)],
}, ensure_ascii=False)

filters = "".join(f'<button type="button" class="chip{" on" if k == "all" else ""}" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n}</button>'
                  for k, n in [("all", "All"), ("ios", "iOS"), ("android", "Android"), ("flutter", "Flutter"), ("react-native", "React Native"), ("web", "Web")])

page = open(sys.argv[3]).read()
page = page.replace("{{CARDS}}", "\n".join(cards)).replace("{{TABS}}", tabs).replace("{{PANELS}}", panels) \
           .replace("{{REPOS}}", repos).replace("{{LD}}", ld).replace("{{FILTERS}}", filters) \
           .replace("{{COUNT}}", str(len(labs))).replace("{{UTM}}", UTM)
open(out, "w").write(page)
print("wrote", out)
