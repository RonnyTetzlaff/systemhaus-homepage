#!/usr/bin/env python3
"""Erzeugt die statischen HTML-Seiten aus data/site.json und data/projects.json.

Aufruf (im Repo-Hauptordner):  python3 tools/build.py
Keine Abhängigkeiten außer der Python-Standardbibliothek.
"""
import json
import re
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
site = json.loads((ROOT / "data/site.json").read_text(encoding="utf-8"))
projects = json.loads((ROOT / "data/projects.json").read_text(encoding="utf-8"))

CURRENT = ' aria-current="page"'
NAV = [("index.html", "willkommen"), ("profil.html", "profil"), ("projekte.html", "projekte")]

FILTERS = [
    ("java", r"\bJava\b|J2EE|JEE"),
    ("portal", r"Portal|Portlet"),
    ("soa & webservices", r"WebService|SOA|ServiceBus|Message-Broker|EAI"),
    ("corba", r"CORBA|ORB"),
    ("host", r"Host|REXX|COBOL|PL/I|3270"),
    ("c++ & smalltalk", r"C\+\+|Smalltalk"),
]


def e(s):
    return escape(s, quote=True)


def page(file, title, body, description):
    nav = "\n".join(
        f'    <a href="{href}"{CURRENT if href == file else ""}>{label}</a>'
        for href, label in NAV
    )
    full_title = site["firma"] if file == "index.html" else f'{title} · {site["firma"]}'
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<meta name="theme-color" content="#000000">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<header>
  <div class="masthead"><a class="brand" href="index.html">{e(site["firma"])}</a><div class="band" aria-hidden="true"></div></div>
  <p class="owner">{e(site["inhaber"])}</p>
  <nav class="main" aria-label="Hauptnavigation">
{nav}
  </nav>
</header>
<main>
{body}
</main>
<footer class="site">
  <span>{" · ".join(e(x) for x in site["anschrift"])}</span>
  <nav aria-label="Rechtliches"><a href="impressum.html">impressum</a><a href="impressum.html#datenschutz">datenschutz</a><span>© {date.today().year}</span></nav>
</footer>
</body>
</html>
"""


def contact_block():
    tel = "".join(
        f'<p><a href="tel:{t["tel"]}">{e(t["anzeige"])}</a> <small>[{e(t["label"])}]</small></p>'
        for t in site["telefon"]
    )
    addr = "<br>".join(e(x) for x in site["anschrift"])
    host = re.sub(r"^https?://", "", site["url"])
    return f"""<section class="contact" aria-label="Kontakt">
  <div><h2>anschrift</h2><p>{addr}</p></div>
  <div><h2>telefon</h2>{tel}</div>
  <div><h2>email</h2><p><a href="mailto:{e(site["email"])}">{e(site["email"])}</a></p>
       <h2>internet</h2><p><a href="{e(site["url"])}">{e(host)}</a></p></div>
</section>"""


def build_index():
    claim = " <b>+++</b> ".join(f"<span>{e(c)}</span>" for c in site["claim"])
    body = f"""<figure class="hero"><img src="assets/img/hafen.jpg" width="1237" height="494" alt="Segelhafen in Schwarzweiß"></figure>
<p class="claim"><b>+++</b> {claim} <b>+++</b></p>
{contact_block()}"""
    return page("index.html", "willkommen", body,
                "systemhaus r.tetzlaff – Consulting, Softwarearchitekturen und Coaching. Inhaber Ronny Tetzlaff, Dipl.-Informatiker (TU), Ludwigsburg.")


def build_profil():
    groups = []
    for g in site["profil"]:
        if "skala" in g:
            items = "".join(
                f'<div class="skill"><strong>{e(n)}</strong><span>{e(lvl)}{", " + e(x) if x else ""}</span></div>'
                for n, lvl, x in g["skala"]
            )
            groups.append(f'<section class="group"><h2>{e(g["gruppe"])}</h2><div class="skills">{items}</div></section>')
        else:
            rows = "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in g["eintraege"])
            groups.append(f'<section class="group"><h2>{e(g["gruppe"])}</h2><dl>{rows}</dl></section>')
    body = f"""<div class="page-head"><div><h1>profil</h1><p>Teilprojektleiter, Architekt, Systemdesigner und Entwickler – seit 1994 in Projekten für Banken, Versicherungen, Bausparkassen und Börsen.</p></div></div>
<div class="strip" aria-hidden="true"><img src="assets/img/kanal.jpg" alt="" loading="lazy"><img src="assets/img/mast.jpg" alt="" loading="lazy"><img src="assets/img/segel.jpg" alt="" loading="lazy"></div>
<div class="profile">
{chr(10).join(groups)}
</div>"""
    return page("profil.html", "profil", body, "Profil von Ronny Tetzlaff, Dipl.-Informatiker (TU): Kenntnisse, Werkzeuge und Schulungen.")


def build_projekte():
    btns = '<button type="button" aria-pressed="true" data-filter="">alle</button>' + "".join(
        f'<button type="button" aria-pressed="false" data-filter="{e(name)}">{e(name)}</button>' for name, _ in FILTERS
    )
    items = []
    for i, p in enumerate(projects):
        text = " ".join([p["title"], p["description"], *p["tasks"], *p["tech"]])
        cats = [name for name, rx in FILTERS if re.search(rx, text)]
        tasks = "".join(f"<li>{e(t)}</li>" for t in p["tasks"])
        tech = "".join(f"<li>{e(t)}</li>" for t in p["tech"])
        items.append(f"""<li class="project" data-cats="{e("|".join(cats))}">
  <details{" open" if i == 0 else ""}>
    <summary><span class="when">{e(p["from"])} – {e(p["to"])}</span><h3>{e(p["title"])}</h3><span class="toggle" aria-hidden="true">+</span></summary>
    <div class="body">
      <p>{e(p["description"])}</p>
      <p class="label">aufgaben</p>
      <ul class="tasks">{tasks}</ul>
      <p class="label">technologien</p>
      <ul class="tags">{tech}</ul>
    </div>
  </details>
</li>""")
    body = f"""<div class="page-head"><div><h1>projekte</h1><p>{len(projects)} Projekte von 1994 bis heute – zum Aufklappen auf einen Eintrag tippen.</p></div>
<img src="assets/img/schiff.jpg" alt="" width="220" style="filter:grayscale(1);max-width:220px" loading="lazy"></div>
<div class="filters" role="group" aria-label="Projekte filtern">{btns}</div>
<ol class="timeline">
{chr(10).join(items)}
</ol>
<script>
document.querySelectorAll('.filters button').forEach(function (b) {{
  b.addEventListener('click', function () {{
    var f = b.dataset.filter;
    document.querySelectorAll('.filters button').forEach(function (x) {{ x.setAttribute('aria-pressed', x === b); }});
    document.querySelectorAll('.project').forEach(function (p) {{
      p.hidden = !!f && p.dataset.cats.split('|').indexOf(f) < 0;
    }});
  }});
}});
</script>"""
    return page("projekte.html", "projekte", body, "Projektliste des systemhaus r.tetzlaff: Softwarearchitektur, Portale, SOA, J2EE und CORBA seit 1994.")


def build_impressum():
    addr = "<br>".join(e(x) for x in site["anschrift"])
    tel = "<br>".join(f'Telefon: <a href="tel:{t["tel"]}">{e(t["anzeige"])}</a> ({e(t["label"])})' for t in site["telefon"])
    body = f"""<div class="page-head"><div><h1>impressum</h1></div></div>
<div class="prose">
<h2>angaben gemäß § 5 DDG</h2>
<p>{addr}<br>Inhaber: Ronny Tetzlaff</p>
<h2>kontakt</h2>
<p>{tel}<br>E-Mail: <a href="mailto:{e(site["email"])}">{e(site["email"])}</a></p>
<h2 id="datenschutz">datenschutz</h2>
<p>Diese Website verwendet keine Cookies, keine Analyse- oder Trackingdienste und lädt keine Inhalte von Drittanbietern.
Beim Aufruf der Seiten verarbeitet der Hosting-Anbieter technisch notwendige Verbindungsdaten (z. B. IP-Adresse, Zeitpunkt, aufgerufene Seite) in Server-Logdateien,
um die Auslieferung und Sicherheit der Website zu gewährleisten (Art. 6 Abs. 1 lit. f DSGVO).</p>
<p>Wenn Sie per E-Mail oder Telefon Kontakt aufnehmen, werden Ihre Angaben ausschließlich zur Bearbeitung Ihrer Anfrage verwendet.
Sie haben das Recht auf Auskunft, Berichtigung, Löschung und Einschränkung der Verarbeitung Ihrer Daten sowie ein Beschwerderecht bei einer Datenschutz-Aufsichtsbehörde.</p>
</div>"""
    return page("impressum.html", "impressum", body, "Impressum und Datenschutzhinweise des systemhaus r.tetzlaff.")


if __name__ == "__main__":
    for name, html in [("index.html", build_index()), ("profil.html", build_profil()),
                       ("projekte.html", build_projekte()), ("impressum.html", build_impressum())]:
        (ROOT / name).write_text(html, encoding="utf-8")
        print("geschrieben:", name)
