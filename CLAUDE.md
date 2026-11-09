# cressida.at – Arbeitsanleitung

Ratgeber-Seite zu Trennung und Scheidung in Österreich. Betreiber: FRABANTO AUSTRIA GmbH, Mag. Anton Scharmitzer. Sprache: Deutsch (Österreich), Sie-Form, ruhig und sachlich, keine Kampfrhetorik, keine Parteinahme für eine Seite.

## Aufbau
- Repository-Wurzel = veröffentlichte Seite (statische HTML-Dateien) + `vercel.json`. Kein Build-Schritt.
- Seiten: `/` (Startseite mit FAQ), `/wegweiser/` (Quiz, Logik im Inline-Skript), `/unterhaltsrechner/` (Rechner, Funktion `berechne()` ohne DOM), `/impressum/`, `/datenschutz/`, `404.html`.
- Gemeinsames Layout: `styles.css`; Schrift lokal in `/fonts/pjs.woff2` (keine Google Fonts, keine Fremd-Skripte, keine Cookies).
- Veröffentlichen: Push auf `main`; Vercel baut automatisch (Projekt `cressida`, Team `team_b8wfYEGY3egOk8PEs8TaaKhF`).
- Commits als `Claude <noreply@anthropic.com>`.
- Neue Seite: in `sitemap.xml` und bei Bedarf in `llms.txt` eintragen, danach IndexNow anpingen: `https://api.indexnow.org/indexnow?url=<neue URL>&key=d0dbce36479e9f529e372ec4804deeed`.

## Hosting-Regel (Vercel Hobby)
- Solange das Projekt im Gratis-Plan läuft: keine Preise, Kaufbuttons, Partner-Abos, Werbung oder Affiliate-Links (Vercel-Regel zu kommerzieller Nutzung). Kommerzielle Teile erst nach Umzug auf Hetzner oder Vercel Pro.

## Inhaltliche Regeln
- Jede Zahl, Frist, Gebühr und Voraussetzung an der Primärquelle prüfen (oesterreich.gv.at, justiz.gv.at, bundeskanzleramt.gv.at, ris.bka.gv.at, Statistik Austria) und mit Stand-Datum angeben. Nicht gefundene Werte weglassen und offen benennen.
- Erster Absatz jedes Artikels beantwortet die Suchfrage in 2–4 Sätzen. FAQ-Abschnitt mit 3–6 Fragen.
- Keine Einzelfall-Rechtsberatung, keine Vertragsentwürfe. Hinweis „ersetzt keine Rechtsberatung“.
- Österreich-spezifisch schreiben und deutsche Irrtümer richtigstellen (kein Trennungsjahr, keine Düsseldorfer Tabelle).
- Bei Gewalt in der Beziehung immer auf Schutz statt Mediation verweisen (Frauenhelpline 0800 222 555, Notruf 133).
- Unterhaltswerte: Prozentsätze 16/18/20/22 %, Regelbedarf jährlich zum 1. Jänner aktualisieren.
