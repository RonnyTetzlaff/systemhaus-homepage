# systemhaus r.tetzlaff — Homepage

Neuauflage der alten iWeb-Homepage (www.ronnytetzlaff.de, 2006–2014) als schlichte,
statische Website im Stil des Originals: schwarzer Namensblock mit Taupe-Band,
warmes Grau, Helvetica, Schwarzweiß-/Sepia-Fotos und die Zeile
`+++ consulting +++ softwarearchitekturen +++ coaching +++`.

## Aufbau

| Pfad | Inhalt |
|---|---|
| `data/site.json` | Kontaktdaten, Claim, Profil |
| `data/projects.json` | Projektliste (aus den iWeb-Blogeinträgen übernommen) |
| `tools/build.py` | erzeugt `index.html`, `profil.html`, `projekte.html`, `impressum.html` |
| `assets/` | Stylesheet, Fotos, Favicon |

## Inhalte ändern

1. `data/site.json` oder `data/projects.json` bearbeiten
2. `python3 tools/build.py` ausführen (nur Python-Standardbibliothek)
3. Committen und pushen

Lokale Vorschau: `python3 -m http.server 8000` und dann http://localhost:8000 öffnen.

## Hosting

Die Seiten sind reines HTML/CSS und laufen auf jedem Webspace oder über GitHub Pages
(Settings → Pages → Branch `main`, Ordner `/`). GitHub Pages aus einem **privaten**
Repository erfordert einen kostenpflichtigen GitHub-Plan (Pro/Team); die
veröffentlichte Website selbst ist dann trotzdem öffentlich.
