#!/usr/bin/env python3
"""Generate HomeTogether Local city pages + index + sitemap.
Rerun any time; add cities to the lists below and redeploy."""
import os, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "caregivers")
BASE = "https://tryhometogether.com"

# tier A: Southwest Missouri (served by the Caring Companions family today)
TIER_A = [
    ("springfield", "Springfield"), ("nixa", "Nixa"), ("ozark", "Ozark"),
    ("republic", "Republic"), ("bolivar", "Bolivar"), ("branson", "Branson"),
    ("marshfield", "Marshfield"), ("willard", "Willard"), ("rogersville", "Rogersville"),
    ("aurora", "Aurora"), ("monett", "Monett"), ("mount-vernon", "Mount Vernon"),
    ("buffalo", "Buffalo"), ("clever", "Clever"), ("sparta", "Sparta"), ("strafford", "Strafford"),
]
# tier B: Missouri metros
TIER_B = [
    ("kansas-city", "Kansas City"), ("st-louis", "St. Louis"), ("columbia", "Columbia"),
    ("joplin", "Joplin"), ("jefferson-city", "Jefferson City"), ("lees-summit", "Lee's Summit"),
    ("ofallon", "O'Fallon"), ("st-charles", "St. Charles"), ("independence", "Independence"),
]
# tier C: national metros (city, state abbr, state name, high_cost)
TIER_C = [
    ("new-york", "New York", "NY", "New York", True), ("los-angeles", "Los Angeles", "CA", "California", True),
    ("chicago", "Chicago", "IL", "Illinois", False), ("houston", "Houston", "TX", "Texas", False),
    ("phoenix", "Phoenix", "AZ", "Arizona", False), ("philadelphia", "Philadelphia", "PA", "Pennsylvania", False),
    ("san-antonio", "San Antonio", "TX", "Texas", False), ("san-diego", "San Diego", "CA", "California", True),
    ("dallas", "Dallas", "TX", "Texas", False), ("austin", "Austin", "TX", "Texas", False),
    ("jacksonville", "Jacksonville", "FL", "Florida", False), ("columbus", "Columbus", "OH", "Ohio", False),
    ("charlotte", "Charlotte", "NC", "North Carolina", False), ("indianapolis", "Indianapolis", "IN", "Indiana", False),
    ("seattle", "Seattle", "WA", "Washington", True), ("denver", "Denver", "CO", "Colorado", True),
    ("nashville", "Nashville", "TN", "Tennessee", False), ("boston", "Boston", "MA", "Massachusetts", True),
    ("portland", "Portland", "OR", "Oregon", True), ("las-vegas", "Las Vegas", "NV", "Nevada", False),
    ("memphis", "Memphis", "TN", "Tennessee", False), ("louisville", "Louisville", "KY", "Kentucky", False),
    ("atlanta", "Atlanta", "GA", "Georgia", False), ("miami", "Miami", "FL", "Florida", False),
    ("minneapolis", "Minneapolis", "MN", "Minnesota", False),
]

CITIES = []
for slug, name in TIER_A:
    CITIES.append(dict(slug=slug, city=name, st="MO", state="Missouri", tier="A", high=False))
for slug, name in TIER_B:
    CITIES.append(dict(slug=slug, city=name, st="MO", state="Missouri", tier="B", high=False))
for slug, name, st, state, high in TIER_C:
    CITIES.append(dict(slug=slug, city=name, st=st, state=state, tier="C", high=high))

def rate_line(c):
    if c["st"] == "MO":
        base = "Families in {c} typically pay independent in-home caregivers about $18 to $28 an hour"
        if c["slug"] == "springfield":
            base = "Posted caregiver rates in Springfield average about $18 an hour, with most families paying $18 to $28 an hour"
        return base.format(c=c["city"]) + ", often 30 to 40 percent less than agency rates, because there is no agency markup in the middle."
    if c["high"]:
        return ("Families in {c} typically pay independent in-home caregivers about $25 to $40 an hour, "
                "often well below agency rates, because there is no agency markup in the middle.").format(c=c["city"])
    return ("Families in {c} typically pay independent in-home caregivers about $20 to $32 an hour, "
            "often well below agency rates, because there is no agency markup in the middle.").format(c=c["city"])

def nearby(c):
    pool = [x for x in CITIES if x["slug"] != c["slug"] and (
        (c["tier"] in "AB" and x["tier"] in "AB") or (c["tier"] == "C" and x["tier"] == "C"))]
    i = next(idx for idx, x in enumerate(pool))
    start = [x["slug"] for x in pool].index(pool[0]["slug"])
    # deterministic: pick 4 following entries after this city's position in the master list
    idxs = [x["slug"] for x in pool]
    pos = sum(1 for x in CITIES if x["slug"] < c["slug"]) % len(pool)
    picks = [pool[(pos + k) % len(pool)] for k in range(4)]
    return picks

def faq(c):
    loc = f"{c['city']}, {c['st']}"
    qs = [
        ("How do I find an in-home caregiver in " + loc + "?",
         "Tell us what your family needs in a short five-minute form. A real person from our team reviews it and reaches out, usually the same day, to introduce caregivers near " + c["city"] + ". Talking to your matches is free, and there is no obligation to hire."),
        ("How much does in-home senior care cost in " + loc + "?",
         rate_line(c) + " You and the caregiver agree on the rate directly."),
        ("Are caregivers background-checked?",
         "Yes. Every caregiver on HomeTogether Local completes identity verification, a national criminal database search, a sex-offender registry search, and county record checks, renewed every year they are active. No check on any website can guarantee safety, which is why a real person from our team stays involved from first match to first visit."),
        ("Does it cost money to use HomeTogether Local?",
         "No subscriptions, no auto-renew, ever. Talking to your matches is always free. You pay your caregiver directly at the rate you agree on together."),
    ]
    return qs

def page(c):
    loc = f"{c['city']}, {c['st']}"
    title = f"In-Home Caregivers in {loc} | HomeTogether Local"
    desc = (f"Find a vetted, background-checked in-home caregiver in {loc}. Hand-picked matches, free to talk, "
            "no subscriptions. From the HomeTogether family, backed by real caregivers.")
    canon = f"{BASE}/caregivers/{c['slug']}"
    qs = faq(c)
    faq_html = "\n".join(
        f'<details class="q"><summary>{html.escape(q)}</summary><div class="a">{html.escape(a)}</div></details>' for q, a in qs)
    faq_ld = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]})
    near = "".join(f'<a href="/caregivers/{n["slug"]}">{html.escape(n["city"])}, {n["st"]}</a>' for n in nearby(c))
    mo_block = ""
    if c["tier"] == "A":
        mo_block = """
<section class="band">
  <h2>Backed by a real local agency</h2>
  <p>HomeTogether Local comes from the family behind <b>Caring Companions</b>, a family-owned senior-care agency that has cared for Southwest Missouri families since 2017. We are not a faraway tech company. Our own caregivers work in and around {CITY} every week, and if a marketplace match is not the right fit, our agency can often help directly. A real local person answers every request, usually the same day: <a href="/help.html#contact"><b>send us a message</b></a>.</p>
</section>""".replace("{CITY}", c["city"])
    elif c["tier"] == "B":
        mo_block = """
<section class="band">
  <h2>Missouri roots, real people</h2>
  <p>HomeTogether Local is built by the family behind <b>Caring Companions</b>, a Missouri senior-care agency caring for families since 2017. We are expanding across Missouri city by city, and every {CITY} request is reviewed by a real person, not an algorithm. Questions? <a href="/help.html#contact"><b>Send us a request</b></a> and a real person follows up.</p>
</section>""".replace("{CITY}", c["city"])
    else:
        mo_block = """
<section class="band">
  <h2>Rolling out city by city</h2>
  <p>We are adding vetted caregivers area by area, and demand tells us where to go next. Tell us what your family needs in {CITY} and a real person will follow up. If we are not fully live near you yet, you will be first in line the moment we are, and we will point you toward trustworthy options in the meantime.</p>
</section>""".replace("{CITY}", c["city"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="https://tryhometogether.com/assets/hero-family-tv.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://tryhometogether.com/assets/hero-family-tv.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Nunito+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{color-scheme:light;--navy:#0D365F;--ink:#16283A;--paper:#F8F7F3;--card:#fff;--teal:#1E7A8C;--teal-deep:#155A68;--teal-soft:#E7F2F4;--honey:#E9A23B;--good:#2E9B63;--muted:#5B6B79;--faint:#8B98A4;--line:#E9E4DB;
--serif:'Fraunces',Georgia,serif;--sans:'Nunito Sans',-apple-system,sans-serif}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16.5px;line-height:1.65}}
h1,h2{{font-family:var(--serif);color:var(--navy);letter-spacing:-.012em;text-wrap:balance;margin:0}}
a{{color:var(--teal-deep)}}
.wrap{{max-width:860px;margin:0 auto;padding:0 22px}}
header{{position:sticky;top:0;background:color-mix(in srgb,var(--paper) 90%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);z-index:20}}
header .row{{display:flex;align-items:center;gap:18px;height:62px}}
.wm{{font-family:var(--serif);font-weight:700;font-size:20px;color:var(--navy);text-decoration:none}}.wm b{{color:#C9821C}}
header .cta{{margin-left:auto;display:flex;gap:14px;align-items:center}}
header .cta a.lnk{{font-size:14px;font-weight:700;text-decoration:none;color:var(--muted)}}
.btn{{display:inline-block;background:var(--teal);color:#fff;border-radius:12px;padding:12px 22px;font-weight:800;text-decoration:none;font-size:15.5px}}
.btn:hover{{background:var(--teal-deep)}}
.hero{{padding:52px 0 34px}}
.eyebrow{{font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--teal-deep)}}
.hero h1{{font-size:clamp(30px,5.4vw,44px);line-height:1.07;margin:12px 0 0}}
.hero p.lede{{font-size:18px;color:var(--muted);margin:16px 0 22px;max-width:56ch}}
.trust{{display:flex;gap:16px;flex-wrap:wrap;margin-top:18px;font-size:13.5px;font-weight:700;color:var(--muted)}}
.trust span::before{{content:"✓ ";color:var(--good)}}
section{{padding:26px 0}}
h2{{font-size:clamp(22px,3.4vw,29px);margin:0 0 14px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px 24px;margin:14px 0;box-shadow:0 1px 2px rgba(13,54,95,.04),0 8px 26px rgba(13,54,95,.06)}}
.steps{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.step{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}}
.step b{{display:block;color:var(--navy);margin-bottom:5px}}
.step .n{{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--navy);color:#fff;font-family:var(--serif);font-weight:700;margin-bottom:9px}}
.step p{{margin:0;font-size:14px;color:var(--muted)}}
.band{{background:var(--teal-soft);border:1px solid color-mix(in srgb,var(--teal) 25%,transparent);border-radius:16px;padding:22px 26px;margin:14px 0}}
.band h2{{font-size:20px}}
.band p{{margin:8px 0 0;font-size:15.5px}}
.q{{background:var(--card);border:1px solid var(--line);border-radius:12px;margin:10px 0;padding:0 18px}}
.q summary{{cursor:pointer;font-weight:800;color:var(--navy);padding:15px 0;font-size:15.5px}}
.q .a{{padding:0 0 16px;color:var(--ink);font-size:15px}}
.near{{display:flex;flex-wrap:wrap;gap:9px}}
.near a{{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:7px 14px;font-size:13.5px;font-weight:700;text-decoration:none;color:var(--teal-deep)}}
.final{{background:linear-gradient(120deg,var(--navy),var(--teal-deep));border-radius:18px;color:#fff;text-align:center;padding:36px 26px;margin:20px 0}}
.final h2{{color:#fff}}
.final p{{color:rgba(255,255,255,.88)}}
.final .btn{{background:var(--honey);color:#3a2708;margin-top:8px}}
footer{{border-top:1px solid var(--line);margin-top:30px;padding:26px 0 40px;font-size:13px;color:var(--faint)}}
footer a{{color:var(--muted);font-weight:700;text-decoration:none;margin-right:14px}}
@media(max-width:720px){{.steps{{grid-template-columns:1fr}}header .cta a.lnk{{display:none}}}}
</style>
<script type="application/ld+json">{faq_ld}</script>
</head>
<body>
<header><div class="wrap row">
  <a class="wm" href="/local">HomeTogether <b>Local</b></a>
  <span class="cta">
    <a class="lnk" href="/">HomeTogether TV</a>
    <a class="lnk" href="/help.html#contact">Support</a>
    <a class="btn" href="/local">Find care</a>
  </span>
</div></header>

<div class="wrap">
<section class="hero">
  <span class="eyebrow">In-home senior care · {html.escape(loc)}</span>
  <h1>Find an in-home caregiver in {html.escape(c['city'])}.</h1>
  <p class="lede">Tell us what your family needs, and a real person hand-picks vetted, background-checked caregivers near {html.escape(c['city'])}. Free to talk, no subscriptions, and you hire directly at a rate you agree on together.</p>
  <a class="btn" href="/local">Get matched free →</a>
  <div class="trust"><span>Background-checked</span><span>Hand-picked by a real person</span><span>No subscription, ever</span></div>
</section>

<section>
  <h2>How it works in {html.escape(c['city'])}</h2>
  <div class="steps">
    <div class="step"><span class="n">1</span><b>Tell us what you need</b><p>A five-minute form about your loved one: the kind of help, how often, and where in the {html.escape(c['city'])} area.</p></div>
    <div class="step"><span class="n">2</span><b>Get hand-picked matches</b><p>A real person reviews your request, usually the same day, and introduces caregivers who fit.</p></div>
    <div class="step"><span class="n">3</span><b>Interview and hire directly</b><p>Talk free, meet the ones you like, and hire the person you trust. No agency markup in the middle.</p></div>
  </div>
</section>

<section>
  <h2>What in-home care costs in {html.escape(c['city'])}</h2>
  <div class="card"><p style="margin:0">{html.escape(rate_line(c))} Most families start with a few hours a week of companionship, meals, errands, or personal care, and adjust as needs change. Overnight and live-in arrangements are usually quoted as a daily rate instead.</p></div>
</section>
{mo_block}
<section>
  <h2>Common questions in {html.escape(loc)}</h2>
  {faq_html}
</section>

<section>
  <h2>Nearby areas we serve</h2>
  <div class="near">{near}<a href="/caregivers/">All cities</a></div>
</section>

<section class="band" style="background:#FBF3E3;border-color:rgba(201,130,28,.35)">
  <h2>Are you a caregiver in {html.escape(c['city'])}?</h2>
  <p>Set your own rate, choose your clients, and keep everything you earn. Joining is free. <a href="/caregiver-jobs/{c['slug']}"><b>See caregiver jobs in {html.escape(c['city'])} →</b></a></p>
</section>

<div class="final">
  <h2>Care for someone you love in {html.escape(c['city'])}?</h2>
  <p>It takes five minutes to tell us what you need. Talking to matches is always free.</p>
  <a class="btn" href="/local">Find a caregiver near you →</a>
</div>
</div>

<footer><div class="wrap">
  <div><a href="/local">HomeTogether Local</a><a href="/">HomeTogether TV</a><a href="/caregivers/">All cities</a><a href="/help.html">Help</a><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a></div>
  <div style="margin-top:10px">HomeTogether Local is a caregiver-matching service from the HomeTogether family, a Caring Companions company. Caregivers are independent providers hired directly by families, not our employees. Background checks have limits and cannot guarantee safety. Support: <a href="/help.html#contact">submit a request</a> · support@tryhometogether.com · © 2026 HomeTogether</div>
</div></footer>
</body>
</html>
"""

def cg_rate_line(c):
    if c["st"] == "MO":
        return ("Independent caregivers in {c} typically charge $18 to $28 an hour, and on HomeTogether Local "
                "you keep all of it. There is no agency taking a cut and no monthly fee eating your pay.").format(c=c["city"])
    if c["high"]:
        return ("Independent caregivers in {c} typically charge $25 to $40 an hour, and on HomeTogether Local "
                "you keep all of it. There is no agency taking a cut and no monthly fee eating your pay.").format(c=c["city"])
    return ("Independent caregivers in {c} typically charge $20 to $32 an hour, and on HomeTogether Local "
            "you keep all of it. There is no agency taking a cut and no monthly fee eating your pay.").format(c=c["city"])

def jobs_faq(c):
    loc = f"{c['city']}, {c['st']}"
    return [
        ("How much can I earn as a caregiver in " + loc + "?",
         cg_rate_line(c) + " You set your rate, and you and the family agree on it directly."),
        ("Does it cost anything to join?",
         "No. Creating your profile is free, and responding to families is free. Unlike the big caregiver sites, we never charge you a monthly fee to talk to families."),
        ("Do I need experience or certifications?",
         "Experience helps, and certifications like CNA, HHA, or CPR earn a Verified badge that families look for. But compassionate, reliable caregivers of all backgrounds are welcome to apply. Every caregiver completes identity verification and a background check before being matched."),
        ("How do I get clients in " + c["city"] + "?",
         "Families in the " + c["city"] + " area tell us what they need, and a real person introduces them to caregivers who fit. You choose which families to work with, on your schedule, in your service area."),
    ]

def jobs_page(c):
    loc = f"{c['city']}, {c['st']}"
    title = f"Caregiver Jobs in {loc} | Set Your Own Rate | HomeTogether Local"
    desc = (f"Caregiver jobs in {loc} on your terms. Set your own rate, choose your clients, keep 100 percent of what you earn. "
            "Free to join. From the HomeTogether family.")
    canon = f"{BASE}/caregiver-jobs/{c['slug']}"
    qs = jobs_faq(c)
    faq_html = "\n".join(
        f'<details class="q"><summary>{html.escape(q)}</summary><div class="a">{html.escape(a)}</div></details>' for q, a in qs)
    faq_ld = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]})
    near = "".join(f'<a href="/caregiver-jobs/{n["slug"]}">{html.escape(n["city"])}, {n["st"]}</a>' for n in nearby(c))
    if c["tier"] == "A":
        tier_block = """
<section class="band">
  <h2>Real caregiving work, right here in {CITY}</h2>
  <p>HomeTogether Local comes from the family behind <b>Caring Companions</b>, a family-owned senior-care agency serving Southwest Missouri since 2017. Families here already trust our name, and their requests come to us first. Prefer steady agency hours with a W-2 instead? Our agency hires caregivers across Southwest Missouri too. <a href="/help.html#contact"><b>Send us a request</b></a> and a real person will point you to the better fit.</p>
</section>"""
    elif c["tier"] == "B":
        tier_block = """
<section class="band">
  <h2>Get in early in {CITY}</h2>
  <p>We are expanding across Missouri city by city, backed by a real Missouri care agency, Caring Companions. Caregivers who join now are first in line as {CITY} families sign up, and early profiles build reviews fastest. A real person reviews every application.</p>
</section>"""
    else:
        tier_block = """
<section class="band">
  <h2>Be first in line in {CITY}</h2>
  <p>We are rolling out city by city, and caregiver supply tells us where to open next. Join free now and you will be at the front of the line when {CITY} families start matching, with your profile, your rate, and your service area already set.</p>
</section>"""
    tier_block = tier_block.replace("{CITY}", c["city"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="https://tryhometogether.com/assets/hero-family-tv.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://tryhometogether.com/assets/hero-family-tv.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Nunito+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{color-scheme:light;--navy:#0D365F;--ink:#16283A;--paper:#F8F7F3;--card:#fff;--teal:#1E7A8C;--teal-deep:#155A68;--teal-soft:#E7F2F4;--honey:#E9A23B;--honey-deep:#C9821C;--good:#2E9B63;--muted:#5B6B79;--faint:#8B98A4;--line:#E9E4DB;
--serif:'Fraunces',Georgia,serif;--sans:'Nunito Sans',-apple-system,sans-serif}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16.5px;line-height:1.65}}
h1,h2{{font-family:var(--serif);color:var(--navy);letter-spacing:-.012em;text-wrap:balance;margin:0}}
a{{color:var(--teal-deep)}}
.wrap{{max-width:860px;margin:0 auto;padding:0 22px}}
header{{position:sticky;top:0;background:color-mix(in srgb,var(--paper) 90%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);z-index:20}}
header .row{{display:flex;align-items:center;gap:18px;height:62px}}
.wm{{font-family:var(--serif);font-weight:700;font-size:20px;color:var(--navy);text-decoration:none}}.wm b{{color:var(--honey-deep)}}
header .cta{{margin-left:auto;display:flex;gap:14px;align-items:center}}
header .cta a.lnk{{font-size:14px;font-weight:700;text-decoration:none;color:var(--muted)}}
.btn{{display:inline-block;background:var(--honey);color:#3a2708;border-radius:12px;padding:12px 22px;font-weight:800;text-decoration:none;font-size:15.5px}}
.btn:hover{{background:var(--honey-deep)}}
.hero{{padding:52px 0 34px}}
.eyebrow{{font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--honey-deep)}}
.hero h1{{font-size:clamp(30px,5.4vw,44px);line-height:1.07;margin:12px 0 0}}
.hero p.lede{{font-size:18px;color:var(--muted);margin:16px 0 22px;max-width:56ch}}
.trust{{display:flex;gap:16px;flex-wrap:wrap;margin-top:18px;font-size:13.5px;font-weight:700;color:var(--muted)}}
.trust span::before{{content:"✓ ";color:var(--good)}}
section{{padding:26px 0}}
h2{{font-size:clamp(22px,3.4vw,29px);margin:0 0 14px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px 24px;margin:14px 0;box-shadow:0 1px 2px rgba(13,54,95,.04),0 8px 26px rgba(13,54,95,.06)}}
.steps{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}}
.step{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}}
.step b{{display:block;color:var(--navy);margin-bottom:5px}}
.step .n{{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--navy);color:#fff;font-family:var(--serif);font-weight:700;margin-bottom:9px}}
.step p{{margin:0;font-size:14px;color:var(--muted)}}
.band{{background:var(--teal-soft);border:1px solid color-mix(in srgb,var(--teal) 25%,transparent);border-radius:16px;padding:22px 26px;margin:14px 0}}
.band h2{{font-size:20px}}
.band p{{margin:8px 0 0;font-size:15.5px}}
.q{{background:var(--card);border:1px solid var(--line);border-radius:12px;margin:10px 0;padding:0 18px}}
.q summary{{cursor:pointer;font-weight:800;color:var(--navy);padding:15px 0;font-size:15.5px}}
.q .a{{padding:0 0 16px;color:var(--ink);font-size:15px}}
.near{{display:flex;flex-wrap:wrap;gap:9px}}
.near a{{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:7px 14px;font-size:13.5px;font-weight:700;text-decoration:none;color:var(--teal-deep)}}
.final{{background:linear-gradient(120deg,var(--navy),var(--teal-deep));border-radius:18px;color:#fff;text-align:center;padding:36px 26px;margin:20px 0}}
.final h2{{color:#fff}}
.final p{{color:rgba(255,255,255,.88)}}
.final .btn{{margin-top:8px}}
footer{{border-top:1px solid var(--line);margin-top:30px;padding:26px 0 40px;font-size:13px;color:var(--faint)}}
footer a{{color:var(--muted);font-weight:700;text-decoration:none;margin-right:14px}}
@media(max-width:720px){{.steps{{grid-template-columns:1fr 1fr}}header .cta a.lnk{{display:none}}}}
@media(max-width:480px){{.steps{{grid-template-columns:1fr}}}}
</style>
<script type="application/ld+json">{faq_ld}</script>
</head>
<body>
<header><div class="wrap row">
  <a class="wm" href="/local#caregivers">HomeTogether <b>Local</b></a>
  <span class="cta">
    <a class="lnk" href="/caregivers/{c['slug']}">For families</a>
    <a class="lnk" href="/help.html#contact">Support</a>
    <a class="btn" href="/local#join">Join free</a>
  </span>
</div></header>

<div class="wrap">
<section class="hero">
  <span class="eyebrow">Caregiver jobs · {html.escape(loc)}</span>
  <h1>Caregiving in {html.escape(c['city'])}, on your terms.</h1>
  <p class="lede">Set your own rate, choose the families you work with, and keep everything you earn. HomeTogether Local matches you with families near {html.escape(c['city'])} who need exactly what you offer. Joining is free, always.</p>
  <a class="btn" href="/local#join">Create your free profile →</a>
  <div class="trust"><span>Keep 100% of your rate</span><span>Choose your clients</span><span>Free to join, no monthly fees</span></div>
</section>

<section>
  <h2>How it works</h2>
  <div class="steps">
    <div class="step"><span class="n">1</span><b>Build your profile</b><p>Your experience, skills, rate, and how far you'll travel around {html.escape(c['city'])}.</p></div>
    <div class="step"><span class="n">2</span><b>Get verified</b><p>Identity and background check, plus your certifications, earn the Verified badge families look for.</p></div>
    <div class="step"><span class="n">3</span><b>Match with families</b><p>A real person introduces you to {html.escape(c['city'])} families who fit. You choose who to work with.</p></div>
    <div class="step"><span class="n">4</span><b>Get hired and reviewed</b><p>Do great work, get paid your full rate, and build reviews that bring more clients.</p></div>
  </div>
</section>

<section>
  <h2>What caregivers earn in {html.escape(c['city'])}</h2>
  <div class="card"><p style="margin:0">{html.escape(cg_rate_line(c))} Many caregivers on the big sites also pay a monthly fee just to respond to families. Here, talking to families is free, for you and for them.</p></div>
</section>
{tier_block}
<section>
  <h2>Common questions</h2>
  {faq_html}
</section>

<section>
  <h2>Caregiver jobs nearby</h2>
  <div class="near">{near}<a href="/caregiver-jobs/">All cities</a></div>
</section>

<div class="final">
  <h2>Your skills are needed in {html.escape(c['city'])}.</h2>
  <p>Five minutes to set up your profile. Free now, free always.</p>
  <a class="btn" href="/local#join">Join as a caregiver →</a>
</div>
</div>

<footer><div class="wrap">
  <div><a href="/local#caregivers">For caregivers</a><a href="/caregivers/{c['slug']}">Families: find care in {html.escape(c['city'])}</a><a href="/caregiver-jobs/">All cities</a><a href="/help.html">Help</a><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a></div>
  <div style="margin-top:10px">HomeTogether Local is a caregiver-matching service from the HomeTogether family, a Caring Companions company. Caregivers are independent providers hired directly by families, not our employees. Support: <a href="/help.html#contact">submit a request</a> · support@tryhometogether.com · © 2026 HomeTogether</div>
</div></footer>
</body>
</html>
"""

def jobs_index():
    groups = {}
    for c in CITIES:
        groups.setdefault(c["state"], []).append(c)
    order = ["Missouri"] + sorted(k for k in groups if k != "Missouri")
    body = ""
    for state in order:
        links = "".join(f'<a href="/caregiver-jobs/{c["slug"]}">{html.escape(c["city"])}</a>' for c in groups[state])
        body += f'<h2>{state}</h2><div class="near" style="margin-bottom:22px">{links}</div>'
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Caregiver Jobs by City | Set Your Own Rate | HomeTogether Local</title>
<meta name="description" content="Browse caregiver jobs by city. Set your own rate, choose your clients, keep 100 percent of what you earn. Free to join, no monthly fees.">
<link rel="canonical" href="{BASE}/caregiver-jobs/">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Nunito+Sans:wght@400;700;800&display=swap" rel="stylesheet">
<style>:root{{color-scheme:light}}body{{margin:0;background:#F8F7F3;color:#16283A;font-family:'Nunito Sans',sans-serif;line-height:1.6}}
h1,h2{{font-family:'Fraunces',Georgia,serif;color:#0D365F;margin:0 0 12px}}h2{{font-size:20px;margin-top:26px}}
.wrap{{max-width:860px;margin:0 auto;padding:0 22px 50px}}
header{{border-bottom:1px solid #E9E4DB;margin-bottom:30px}}header .row{{display:flex;align-items:center;height:62px}}
.wm{{font-family:'Fraunces',serif;font-weight:700;font-size:20px;color:#0D365F;text-decoration:none}}.wm b{{color:#C9821C}}
.btn{{margin-left:auto;background:#E9A23B;color:#3a2708;border-radius:12px;padding:11px 20px;font-weight:800;text-decoration:none;font-size:15px}}
.near{{display:flex;flex-wrap:wrap;gap:9px}}
.near a{{background:#fff;border:1px solid #E9E4DB;border-radius:999px;padding:7px 14px;font-size:13.5px;font-weight:700;text-decoration:none;color:#155A68}}
p.lede{{color:#5B6B79;max-width:60ch}}</style></head>
<body><header><div class="wrap row"><a class="wm" href="/local#caregivers">HomeTogether <b>Local</b></a><a class="btn" href="/local#join">Join free</a></div></header>
<div class="wrap"><h1>Caregiver jobs, on your terms</h1>
<p class="lede">Set your own rate, choose the families you work with, and keep everything you earn. Free to join, no monthly fees, ever. Choose your area:</p>
{body}</div></body></html>
"""

def index_page():
    groups = {}
    for c in CITIES:
        groups.setdefault(c["state"], []).append(c)
    order = ["Missouri"] + sorted(k for k in groups if k != "Missouri")
    body = ""
    for state in order:
        links = "".join(f'<a href="/caregivers/{c["slug"]}">{html.escape(c["city"])}</a>' for c in groups[state])
        body += f'<h2>{state}</h2><div class="near" style="margin-bottom:22px">{links}</div>'
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Find In-Home Caregivers by City | HomeTogether Local</title>
<meta name="description" content="Browse cities where HomeTogether Local matches families with vetted, background-checked in-home caregivers. Hand-picked matches, free to talk, no subscriptions.">
<link rel="canonical" href="{BASE}/caregivers/">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Nunito+Sans:wght@400;700;800&display=swap" rel="stylesheet">
<style>:root{{color-scheme:light}}body{{margin:0;background:#F8F7F3;color:#16283A;font-family:'Nunito Sans',sans-serif;line-height:1.6}}
h1,h2{{font-family:'Fraunces',Georgia,serif;color:#0D365F;margin:0 0 12px}}h2{{font-size:20px;margin-top:26px}}
.wrap{{max-width:860px;margin:0 auto;padding:0 22px 50px}}
header{{border-bottom:1px solid #E9E4DB;margin-bottom:30px}}header .row{{display:flex;align-items:center;height:62px}}
.wm{{font-family:'Fraunces',serif;font-weight:700;font-size:20px;color:#0D365F;text-decoration:none}}.wm b{{color:#C9821C}}
.btn{{margin-left:auto;background:#1E7A8C;color:#fff;border-radius:12px;padding:11px 20px;font-weight:800;text-decoration:none;font-size:15px}}
.near{{display:flex;flex-wrap:wrap;gap:9px}}
.near a{{background:#fff;border:1px solid #E9E4DB;border-radius:999px;padding:7px 14px;font-size:13.5px;font-weight:700;text-decoration:none;color:#155A68}}
p.lede{{color:#5B6B79;max-width:60ch}}</style></head>
<body><header><div class="wrap row"><a class="wm" href="/local">HomeTogether <b>Local</b></a><a class="btn" href="/local">Find care</a></div></header>
<div class="wrap"><h1>Find an in-home caregiver near you</h1>
<p class="lede">HomeTogether Local matches families with vetted, background-checked caregivers, hand-picked by a real person. Free to talk, no subscriptions, and you hire directly. Choose your area:</p>
{body}</div></body></html>
"""

def sitemap():
    urls = [f"{BASE}/", f"{BASE}/local", f"{BASE}/get", f"{BASE}/about.html", f"{BASE}/help.html",
            f"{BASE}/caregivers/", f"{BASE}/caregiver-jobs/"]
    urls += [f"{BASE}/caregivers/{c['slug']}" for c in CITIES]
    urls += [f"{BASE}/caregiver-jobs/{c['slug']}" for c in CITIES]
    items = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n'

JOBS_OUT = os.path.join(ROOT, "caregiver-jobs")
os.makedirs(OUT, exist_ok=True)
os.makedirs(JOBS_OUT, exist_ok=True)
for c in CITIES:
    with open(os.path.join(OUT, c["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(page(c))
    with open(os.path.join(JOBS_OUT, c["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(jobs_page(c))
with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_page())
with open(os.path.join(JOBS_OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(jobs_index())
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap())
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write("User-agent: *\nAllow: /\nSitemap: " + BASE + "/sitemap.xml\n")
print(f"generated {len(CITIES)} family pages + {len(CITIES)} caregiver-jobs pages + 2 indexes + sitemap + robots")
