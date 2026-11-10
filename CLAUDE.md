# cressida.at – Arbeitsanleitung

Ratgeber-Seite zu Trennung und Scheidung in Österreich. Betreiber: FRABANTO AUSTRIA GmbH, Mag. Anton Scharmitzer. Sprache: Deutsch (Österreich), Sie-Form, ruhig und sachlich, keine Kampfrhetorik, keine Parteinahme für eine Seite.

## Aufbau
- Repository-Wurzel = veröffentlichte Seite (statische HTML-Dateien) + `vercel.json`. Vercel baut nichts; erzeugte Seiten werden mit committet.
- Ratgeber: Artikeltext in `_quelle/ratgeber/<handle>.html`, Metadaten (h1, SEO-Titel ≤ 60 Zeichen, Beschreibung ≤ 155 Zeichen, phase, published, modified) in der Liste `ARTIKEL` in `_quelle/build.py`. Bauen: `cd _quelle && python3 build.py` – schreibt `/ratgeber/<handle>/index.html`, `/ratgeber/index.html` und `sitemap.xml` (Article-, FAQ- und Breadcrumb-Schema automatisch). Danach `llms.txt` ergänzen und Startseite/Werkzeuge intern verlinken.
- Artikel-Aufbau: erster Absatz `<strong>Die kurze Antwort:</strong>`, H2 als Fragen, mindestens eine Tabelle oder Checkliste, `<h2>Häufige Fragen</h2>` mit 3–6 `<h3>` + genau einem `<p>`, am Ende `<h2>Quellen</h2>` mit Stand-Datum.
- Seiten: `/` (Startseite mit FAQ), `/ratgeber/` (Übersicht + Artikel), `/wegweiser/` (Quiz, Logik im Inline-Skript), `/unterhaltsrechner/` (Rechner, Funktion `berechne()` ohne DOM), `/impressum/`, `/datenschutz/`, `404.html`.
- Startseite: Die Link-Listen der vier Phasen-Karten erzeugt `build.py` aus `ARTIKEL` (Feld `phase`, Linktext optional über Feld `start` oder `START_TITEL`; feste Zusatzlinks in `START_EXTRA`). Keine Titel ohne fertigen Artikel ankündigen, weder auf der Startseite noch anderswo.
- `/ueber-uns/` (wer dahintersteht, Prüfweise, Finanzierung) erzeugt `build.py` in `ueber_uns()`; Autor-Angaben der Artikel verweisen dorthin. Ändert sich die Finanzierung (Produkte, Partner), dort zuerst anpassen.
- Gemeinsames Layout: `styles.css`; Schrift lokal in `/fonts/pjs.woff2` (keine Google Fonts, keine Fremd-Skripte, keine Cookies).
- Veröffentlichen: Push auf `main`; Vercel baut automatisch (Projekt `cressida`, Team `team_b8wfYEGY3egOk8PEs8TaaKhF`).
- Commits als `Claude <noreply@anthropic.com>`.
- Neue Seite: in `sitemap.xml` und bei Bedarf in `llms.txt` eintragen, danach IndexNow anpingen: `https://api.indexnow.org/indexnow?url=<neue URL>&key=d0dbce36479e9f529e372ec4804deeed`.

## Formulare (gleicher Aufbau wie daheimklar.at)
- `api/` = Vercel Functions: `lead.js` (typ=newsletter mit Double-Opt-in; typ=anfrage nur mit Umgebungsvariable `ANFRAGEN_AKTIV=1`), `bestaetigen.js`, `abmelden.js`, `aufraeumen.js` (Cron täglich, löscht nach 180 Tagen), `export.js` (CSV mit `?key=`), `health.js`. Seitenspezifisches (Einwilligungstexte, Anliegen) in `api/_site.js`; Textänderung = Version erhöhen.
- Speicher: privater Vercel-Blob-Store (`BLOB_READ_WRITE_TOKEN`). Umgebungsvariablen: `SITE_BASE_URL`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM`, `NOTIFY_TO`, `EXPORT_KEY`, `CRON_SECRET`, optional `ANFRAGEN_AKTIV`.
- Newsletter-Box: `newsletter_box()` in `_quelle/build.py` (Artikel) und handeingefügt in `index.html`. Danke-/Fehler-/Newsletter-Seiten erzeugt `build.py`.

## Hosting-Regel (Vercel Hobby)
- Solange das Projekt im Gratis-Plan läuft: keine Preise, Kaufbuttons, Partner-Abos, Werbung oder Affiliate-Links (Vercel-Regel zu kommerzieller Nutzung). Kommerzielle Teile erst nach Umzug auf Hetzner oder Vercel Pro.

## Inhaltliche Regeln
- Jede Zahl, Frist, Gebühr und Voraussetzung an der Primärquelle prüfen (oesterreich.gv.at, justiz.gv.at, bundeskanzleramt.gv.at, ris.bka.gv.at, Statistik Austria) und mit Stand-Datum angeben. Nicht gefundene Werte weglassen und offen benennen.
- Erster Absatz jedes Artikels beantwortet die Suchfrage in 2–4 Sätzen. FAQ-Abschnitt mit 3–6 Fragen.
- Keine Einzelfall-Rechtsberatung, keine Vertragsentwürfe. Hinweis „ersetzt keine Rechtsberatung“.
- Österreich-spezifisch schreiben und deutsche Irrtümer richtigstellen (kein Trennungsjahr, keine Düsseldorfer Tabelle).
- Bei Gewalt in der Beziehung immer auf Schutz statt Mediation verweisen (Frauenhelpline 0800 222 555, Notruf 133).
- Unterhaltswerte: Prozentsätze 16/18/20/22 %, Regelbedarf jährlich zum 1. Jänner aktualisieren.

## Themenliste Ratgeber (nach Priorität, erledigte streichen)
1. ~~Einvernehmliche Scheidung~~ – erledigt 09.11.2026
2. ~~Scheidungskosten~~ – erledigt 09.11.2026
3. ~~Kindesunterhalt~~ – erledigt 09.11.2026
4. Scheidungsvergleich: Mustergliederung und Checkliste (ohne Vertragsentwurf)
5. Elternberatung vor der Scheidung: Ablauf, Anbieter, Bestätigung
6. Obsorge und Kontaktrecht nach der Trennung
7. Ehewohnung: bleiben, ausziehen, auszahlen
8. Ehegattenunterhalt in Österreich
9. Strittige Scheidung: Ablauf, Verschulden, Fristen
10. Aufteilung von Vermögen und Schulden (Frist 1 Jahr nach Rechtskraft)
11. ~~Unterhaltsvorschuss beantragen~~ – erledigt 10.11.2026
12. Gemeinsamer Kredit nach der Trennung
