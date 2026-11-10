#!/usr/bin/env python3
"""Erzeugt /ratgeber/<handle>/index.html und /ratgeber/index.html aus _quelle/ratgeber/<handle>.html.

Aufruf (im Ordner _quelle):  python3 build.py
Schreibt direkt in die Repository-Wurzel und aktualisiert sitemap.xml.
"""
import html, json, re, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_quelle" / "ratgeber"
SITE = "https://cressida.at"

# Reihenfolge = Reihenfolge auf der Übersicht
ARTIKEL = [
    dict(handle="einvernehmliche-scheidung",
         h1="Einvernehmliche Scheidung in Österreich: Ablauf, Voraussetzungen, Kosten",
         seo="Einvernehmliche Scheidung: Ablauf & Kosten 2026 | Cressida",
         desc="Einvernehmliche Scheidung in Österreich: Voraussetzungen, Ablauf in 6 Schritten, Checkliste für die Vereinbarung und Gebühren 2026 (812 €).",
         kurz="Voraussetzungen, Ablauf in sechs Schritten und Checkliste für die Scheidungsvereinbarung.",
         phase="Entscheiden", published="2026-11-09", modified="2026-11-15"),
    dict(handle="scheidung-kosten",
         h1="Was kostet eine Scheidung in Österreich?",
         seo="Was kostet eine Scheidung in Österreich 2026? | Cressida",
         desc="Scheidungskosten in Österreich 2026: Gerichtsgebühren einvernehmlich und strittig, Anwalt, Verfahrenshilfe und Tariftabelle der geförderten Mediation.",
         kurz="Gerichtsgebühren, Anwaltskosten, Verfahrenshilfe und Selbstbehalt bei geförderter Mediation.",
         phase="Entscheiden", published="2026-11-09", modified="2026-11-09"),
    dict(handle="kindesunterhalt",
         h1="Kindesunterhalt in Österreich 2026: So wird er berechnet",
         seo="Kindesunterhalt 2026: Berechnung in Österreich | Cressida",
         desc="Kindesunterhalt in Österreich: Prozentsätze 16–22 %, Abzüge, Regelbedarf 2026, Obergrenze, Doppelresidenz und Rechenbeispiel mit zwei Kindern.",
         kurz="Prozentsätze, Abzüge, Regelbedarf 2026, Obergrenze und ein durchgerechnetes Beispiel.",
         phase="Umsetzen", published="2026-11-09", modified="2026-11-09"),
    dict(handle="unterhaltsvorschuss",
         h1="Unterhaltsvorschuss in Österreich 2026: Anspruch, Höhe, Antrag",
         seo="Unterhaltsvorschuss 2026: Höhe & Antrag | Cressida",
         desc="Unterhaltsvorschuss in Österreich 2026: wer ihn bekommt, Höchstbetrag 855,16 €, feste Beträge ohne Titel, Antrag in 5 Schritten und Unterlagen.",
         kurz="Wenn der andere Elternteil nicht zahlt: Anspruch, Beträge 2026, Antrag und Unterlagen.",
         phase="Umsetzen", published="2026-11-10", modified="2026-11-10"),
    dict(handle="kontaktrecht",
         h1="Kontaktrecht nach der Trennung: Was in Österreich gilt",
         seo="Kontaktrecht (Besuchsrecht) in Österreich | Cressida",
         desc="Kontaktrecht nach Trennung in Österreich: übliche Besuchszeiten, Checkliste für die Vereinbarung, Antrag bei Gericht, Besuchsbegleitung, Kinder ab 14.",
         kurz="Übliche Besuchszeiten, Checkliste für die Vereinbarung und was hilft, wenn Kontakte scheitern.",
         phase="Umsetzen", published="2026-11-11", modified="2026-11-11"),
    dict(handle="obsorge",
         h1="Obsorge nach der Scheidung: gemeinsam oder allein?",
         seo="Obsorge nach Scheidung in Österreich | Cressida",
         desc="Obsorge nach Scheidung in Österreich: gemeinsame Obsorge als Regel, hauptsächlicher Aufenthalt, alleinige Obsorge, Verfahren und Rechte ohne Obsorge.",
         kurz="Gemeinsame Obsorge als Regel, wer was entscheidet, alleinige Obsorge und das Gerichtsverfahren.",
         phase="Vereinbaren", published="2026-11-12", modified="2026-11-12"),
    dict(handle="ehegattenunterhalt",
         h1="Ehegattenunterhalt nach der Scheidung in Österreich",
         seo="Ehegattenunterhalt nach Scheidung: Höhe | Cressida",
         desc="Ehegattenunterhalt in Österreich: Vereinbarung oder Verschulden, Richtwerte 33 % und 40 %, Unterhalt bei Kinderbetreuung, Rechenbeispiel und Checkliste.",
         kurz="Vereinbarung oder Gesetz, Richtwerte 33 und 40 Prozent, Rechenbeispiel und wann der Anspruch endet.",
         phase="Vereinbaren", published="2026-11-13", modified="2026-11-13"),
    dict(handle="elternberatung",
         h1="Elternberatung vor der Scheidung: Ablauf und Anbieter",
         seo="Elternberatung vor Scheidung (§ 95 AußStrG) | Cressida",
         desc="Elternberatung vor der einvernehmlichen Scheidung in Österreich: wer muss hin, Ablauf, anerkannte Berater finden, Bestätigung fürs Gericht, Kosten.",
         kurz="Wer zur Pflichtberatung muss, Ablauf in vier Schritten, Anbieter finden und Bestätigung fürs Gericht.",
         phase="Vereinbaren", published="2026-11-14", modified="2026-11-14"),
    dict(handle="ehewohnung",
         h1="Ehewohnung bei der Scheidung: Wer bleibt, wer zahlt?",
         seo="Ehewohnung bei Scheidung in Österreich | Cressida",
         desc="Ehewohnung bei Scheidung in Österreich: wann sie aufgeteilt wird, was das Gericht anordnen kann, gemeinsamer Kredit, Jahresfrist und Checkliste.",
         kurz="Wann die Wohnung aufgeteilt wird, was das Gericht anordnen kann, Kredit und Jahresfrist.",
         phase="Umsetzen", published="2026-11-15", modified="2026-11-15"),
]

AUTOR = {"@type": "Person", "name": "Anton Scharmitzer", "honorificPrefix": "Mag.",
         "jobTitle": "Herausgeber, Betriebswirt", "url": f"{SITE}/ueber-uns/"}

LOGO = ('<svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true"><circle cx="17" cy="17" r="16" fill="var(--accent)"/>'
        '<path d="M22 11.5a8 8 0 1 0 0 11" fill="none" stroke="var(--accent-ink)" stroke-width="2.6" stroke-linecap="round"/>'
        '<circle cx="23.5" cy="17" r="1.8" fill="var(--accent-ink)"/></svg>')

def header(current=""):
    def a(href, text):
        cur = ' aria-current="page"' if href == current else ""
        return f'<a href="{href}"{cur}>{text}</a>'
    return ('<header class="site"><div class="w">'
            f'<a class="logo" href="/">{LOGO}<span>Cressida</span></a>'
            '<nav class="main" aria-label="Hauptnavigation">'
            + a("/ratgeber/", "Ratgeber") + a("/wegweiser/", "Wegweiser") + a("/unterhaltsrechner/", "Unterhaltsrechner")
            + '</nav></div></header>')

FOOTER = ('<footer class="site"><div class="w"><p>Cressida bietet allgemeine Informationen zum österreichischen Recht. '
          'Die Inhalte ersetzen keine individuelle Rechtsberatung. © 2026 cressida.at</p>'
          '<nav aria-label="Fußzeile"><a href="/ratgeber/">Ratgeber</a><a href="/ueber-uns/">Über Cressida</a><a href="/impressum/">Impressum</a><a href="/datenschutz/">Datenschutz</a></nav>'
          '</div></footer>')

def head(title, desc, url, ogtype, graph):
    return f"""<!doctype html>
<html lang="de-AT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="theme-color" content="#1F5F5B">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/pjs.woff2" as="font" type="font/woff2" crossorigin>
<meta property="og:type" content="{ogtype}">
<meta property="og:locale" content="de_AT">
<meta property="og:site_name" content="Cressida">
<meta property="og:title" content="{html.escape(title.replace(' | Cressida', ''))}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}
</script>
</head>"""

def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()

def faq_aus(body):
    teil = body.split("<h2>Häufige Fragen</h2>", 1)
    if len(teil) < 2:
        raise SystemExit("FAQ-Abschnitt fehlt")
    faq_html = teil[1].split("<h2", 1)[0]
    paare = re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", faq_html, re.S)
    if not 3 <= len(paare) <= 6:
        raise SystemExit(f"FAQ braucht 3–6 Fragen, gefunden {len(paare)}")
    return [(strip_tags(q), strip_tags(a)) for q, a in paare]

def toc_aus(body):
    eintraege, n = [], 0
    def ersetze(m):
        nonlocal n
        attrs, text = m.group(1), m.group(2)
        if 'id="' in attrs:
            hid = re.search(r'id="([^"]+)"', attrs).group(1)
        else:
            n += 1
            hid = "a" + str(n)
            attrs = f' id="{hid}"' + attrs
        if strip_tags(text) not in ("Quellen",):
            eintraege.append((hid, strip_tags(text)))
        return f"<h2{attrs}>{text}</h2>"
    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", ersetze, body)
    return body, eintraege

def datum(iso):
    d = datetime.date.fromisoformat(iso)
    monate = ["Jänner", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
    return f"{d.day}. {monate[d.month-1]} {d.year}"

def artikel_seite(a, alle):
    url = f"{SITE}/ratgeber/{a['handle']}/"
    body = (SRC / f"{a['handle']}.html").read_text(encoding="utf-8")
    faqs = faq_aus(body)
    body, toc = toc_aus(body)
    erster = strip_tags(re.search(r"<p>(.*?)</p>", body, re.S).group(1)).replace("Die kurze Antwort:", "").strip()
    graph = [
        {"@type": "Article", "@id": url + "#article", "headline": a["h1"], "description": a["desc"],
         "inLanguage": "de-AT", "datePublished": a["published"], "dateModified": a["modified"],
         "author": AUTOR, "publisher": {"@id": f"{SITE}/#organization"},
         "mainEntityOfPage": url, "image": f"{SITE}/og.png", "abstract": erster,
         "about": {"@type": "Thing", "name": a["h1"].split(":")[0]},
         "spatialCoverage": {"@type": "Country", "name": "Österreich"}},
        {"@type": "Organization", "@id": f"{SITE}/#organization", "name": "Cressida", "url": f"{SITE}/", "logo": f"{SITE}/icon.svg"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Startseite", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Ratgeber", "item": f"{SITE}/ratgeber/"},
            {"@type": "ListItem", "position": 3, "name": a["h1"].split(":")[0], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in faqs]},
    ]
    toc_html = "".join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t in toc)
    weitere = "".join(
        f'<li><a href="/ratgeber/{b["handle"]}/">{html.escape(b["h1"].split(":")[0])}</a><span>{html.escape(b["kurz"])}</span></li>'
        for b in alle if b["handle"] != a["handle"])
    return head(a["seo"], a["desc"], url, "article", graph) + f"""
<body>
{header("/ratgeber/")}
<main>
<div class="w narrow art">
<nav class="crumbs" aria-label="Brotkrumen"><a href="/">Startseite</a> › <a href="/ratgeber/">Ratgeber</a></nav>
<p class="eyebrow">Ratgeber · {html.escape(a['phase'])}</p>
<h1>{html.escape(a['h1'])}</h1>
<p class="meta">Geprüft am {datum(a['modified'])} an den amtlichen Quellen · Von <a href="/ueber-uns/" rel="author">Mag. Anton Scharmitzer</a></p>
<details class="toc"><summary>Inhalt</summary><ol>{toc_html}</ol></details>
<div class="prose">
{body}
<div class="autor"><p><strong>Über diesen Ratgeber:</strong> Herausgegeben von Mag. Anton Scharmitzer, Betriebswirt (Studium der Internationalen Betriebswirtschaft an der Universität Wien). Alle Zahlen, Fristen und Gebühren sind an den verlinkten amtlichen Quellen mit Stand-Datum geprüft. Dieser Ratgeber ersetzt keine Rechtsberatung. Für Ihren Einzelfall wenden Sie sich an eine Familienberatungsstelle, die Arbeiterkammer oder eine Anwältin bzw. einen Anwalt.</p></div>
</div>
<aside class="tools-box"><p class="eyebrow">Kostenlose Werkzeuge</p><div class="row"><a class="btn primary" href="/unterhaltsrechner/">Unterhalt berechnen</a><a class="btn ghost" href="/wegweiser/">Welcher Weg passt? Wegweiser</a></div></aside>
<section class="weiter"><h2>Weitere Ratgeber</h2><ul>{weitere}</ul></section>
{newsletter_box("/ratgeber/" + a["handle"] + "/")}
</div>
</main>
{FOOTER}
</body>
</html>
"""

def uebersicht(alle):
    url = f"{SITE}/ratgeber/"
    graph = [
        {"@type": "CollectionPage", "@id": url, "url": url, "name": "Ratgeber Trennung und Scheidung in Österreich",
         "inLanguage": "de-AT", "isPartOf": {"@id": f"{SITE}/#website"},
         "hasPart": [{"@type": "Article", "headline": a["h1"], "url": f"{SITE}/ratgeber/{a['handle']}/"} for a in alle]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Startseite", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Ratgeber", "item": url}]},
    ]
    karten = "".join(
        f'<a class="card rg" href="/ratgeber/{a["handle"]}/"><p class="num">{html.escape(a["phase"])}</p>'
        f'<h2>{html.escape(a["h1"])}</h2><p>{html.escape(a["kurz"])}</p></a>' for a in alle)
    return head("Ratgeber Scheidung & Trennung Österreich | Cressida",
                "Ratgeber zu Scheidung und Trennung in Österreich: einvernehmliche Scheidung, Kosten, Kindesunterhalt. Mit amtlichen Quellen und Stand-Datum.",
                url, "website", graph) + f"""
<body>
{header("/ratgeber/")}
<main>
<div class="w pad-s">
<nav class="crumbs" aria-label="Brotkrumen"><a href="/">Startseite</a> › Ratgeber</nav>
<p class="eyebrow">Ratgeber</p>
<h1>Trennung und Scheidung in Österreich</h1>
<p class="lead">Jede Antwort steht im ersten Absatz, jede Zahl ist an der amtlichen Quelle geprüft und mit Stand-Datum versehen. Nur österreichisches Recht.</p>
<div class="grid4">{karten}</div>
</div>
</main>
{FOOTER}
</body>
</html>
"""

# ---------- Formulare (gleicher Aufbau wie daheimklar.at; Logik in /api) ----------

def _einwilligung(art):
    s = (ROOT / "api" / "_site.js").read_text(encoding="utf-8")
    return re.search(art + r": \['v\d+', '(.*?)'\]", s).group(1)

def newsletter_box(quelle):
    return f"""<section class="nl-box" aria-labelledby="nl-titel">
<p class="eyebrow">Neue Ratgeber per E-Mail</p>
<h2 id="nl-titel">Bleiben Sie auf dem aktuellen Stand</h2>
<p>Höchstens einmal im Monat: neue Ratgeber und Änderungen bei Regeln und Fristen. Kein Spam, jederzeit abbestellbar.</p>
<form method="post" action="/api/lead">
<input type="hidden" name="typ" value="newsletter">
<input type="hidden" name="quelle" value="{html.escape(quelle)}">
<div class="hp" aria-hidden="true"><label>Website <input name="website" tabindex="-1" autocomplete="off"></label></div>
<div class="nl-row"><label class="sr" for="nl-email">E-Mail-Adresse</label><input id="nl-email" type="email" name="email" required autocomplete="email" placeholder="Ihre E-Mail-Adresse"><button class="btn primary" type="submit">Anmelden</button></div>
<label class="nl-check"><input type="checkbox" name="newsletter" value="ja" required> <span>{html.escape(_einwilligung("newsletter"))}</span></label>
<p class="hint">Wir verwenden Ihre Adresse nur dafür. <a href="/datenschutz/">Datenschutz</a></p>
</form>
</section>"""

def info_seite(path, titel, text, links=True):
    weiter = '<p><a href="/">Zur Startseite</a> · <a href="/ratgeber/">Ratgeber lesen</a></p>' if links else ""
    inhalt = f"""<div class="w narrow legal" style="padding-block:56px 72px">
<h1 style="font-size:clamp(30px,4vw,42px)">{titel}</h1>
{text}
{weiter}
</div>"""
    return head(f"{titel} | Cressida", titel, SITE + path, "website", []).replace('content="index, follow, max-snippet:-1, max-image-preview:large"', 'content="noindex, nofollow"') + f"\n<body>\n{header()}\n<main>\n{inhalt}\n</main>\n{FOOTER}\n</body>\n</html>\n"

FORM_SEITEN = {
    "danke/index.html": ("/danke/", "Danke, Ihre Anfrage ist angekommen.",
        "<p>Wir melden uns innerhalb eines Werktags bei Ihnen.</p>"),
    "fehler/index.html": ("/fehler/", "Das hat leider nicht geklappt.",
        "<p>Bitte prüfen Sie Ihre Angaben und versuchen Sie es noch einmal. Klappt es wieder nicht, schreiben Sie uns an office@frabanto.eu.</p>"),
    "newsletter-pruefen/index.html": ("/newsletter-pruefen/", "Fast geschafft: Bitte bestätigen Sie Ihre Anmeldung.",
        "<p>Wir haben Ihnen eine E-Mail mit einem Bestätigungslink geschickt. Erst nach Ihrem Klick bekommen Sie unsere Ratgeber. Keine E-Mail da? Sehen Sie bitte auch im Spam-Ordner nach.</p>"),
    "newsletter-bestaetigt/index.html": ("/newsletter-bestaetigt/", "Danke, Ihre Anmeldung ist bestätigt.",
        "<p>Sie bekommen höchstens einmal im Monat neue Ratgeber und Änderungen. Abmelden geht mit einem Klick in jeder E-Mail.</p>"),
}

DATENSCHUTZ_FORMULARE = """<h2>Newsletter</h2>
<p>Den Newsletter senden wir nur nach Bestätigung per E-Mail (Double-Opt-in, Art. 6 Abs. 1 lit. a DSGVO, § 174 TKG 2021). Wir speichern Ihre E-Mail-Adresse, den Zeitpunkt und den Text Ihrer Einwilligung als Nachweis. Bestätigen Sie die Anmeldung nicht, löschen wir die Adresse nach 6 Monaten. Abmelden können Sie sich jederzeit über den Link in jeder E-Mail.</p>
<h2>Anfragen</h2>
<p>Wenn Sie uns über ein Formular eine Anfrage schicken, speichern wir Ihre Angaben (Name, Kontaktdaten, Anliegen, Bundesland, Postleitzahl, Ihre freiwillige Nachricht) auf Grundlage Ihrer Einwilligung bzw. Ihrer Anfrage (Art. 6 Abs. 1 lit. a und b DSGVO). Ohne Auftrag löschen wir die Anfrage nach 6 Monaten. Über jede neue Anfrage werden wir per E-Mail an unser eigenes Postfach informiert.</p>
<h2>Schutz vor Missbrauch</h2>
<p>Zu jedem abgesendeten Formular speichern wir eine gekürzte IP-Adresse (die letzte Stelle ist entfernt), um Spam und Missbrauch zu erkennen (Art. 6 Abs. 1 lit. f DSGVO).</p>
<h2>Speicherort und E-Mail-Versand</h2>
<p>Formulardaten werden in einem privaten Speicher von Vercel in Frankfurt am Main abgelegt. E-Mails versenden wir über unseren E-Mail-Anbieter.</p>
"""

# --------------------------------------------------------------------------- Startseite: Phasen-Listen
# Die vier Phasen-Karten auf der Startseite zeigen nur Links auf Seiten, die es gibt. Die Listen werden hier aus
# ARTIKEL (Feld "phase", optional "start" als Linktext) erzeugt; angekündigte Titel ohne Artikel gibt es nicht mehr.
START_TITEL = {
    "einvernehmliche-scheidung": "Einvernehmliche Scheidung: Ablauf und Dauer",
    "scheidung-kosten": "Was eine Scheidung wirklich kostet",
    "kindesunterhalt": "Kindesunterhalt: so wird gerechnet",
    "unterhaltsvorschuss": "Unterhaltsvorschuss, wenn der Unterhalt ausbleibt",
}
# Feste Zusatzlinks je Phase (Werkzeuge, Sprungmarken), nach den Artikeln der Phase
START_EXTRA = {
    "Vereinbaren": [("/ratgeber/scheidung-kosten/#mediation", "Mediation: Kosten und Förderung")],
    "Umsetzen": [("/unterhaltsrechner/", "Kindesunterhalt berechnen")],
    "Entscheiden": [("/wegweiser/", "Wegweiser: welcher Weg passt?")],
}
# Abweichende Phase nur für die Startseite (Metadaten in ARTIKEL bleiben unverändert)
START_PHASE = {"unterhaltsvorschuss": "Neu anfangen"}

def start_titel(a):
    if a.get("start"):
        return a["start"]
    if a["handle"] in START_TITEL:
        return START_TITEL[a["handle"]]
    t = a["h1"].split(":")[0]
    t = re.sub(r"\s+in Österreich", "", t)
    return re.sub(r"\s+20\d\d\b", "", t).strip()

def startseite_phasen(alle):
    """Schreibt die <ul> der Phasen-Karten in index.html neu. Mehrfach ausführbar."""
    pfad = ROOT / "index.html"
    seite = pfad.read_text(encoding="utf-8")
    def karte(m):
        phase = m.group(2)
        links = [(f"/ratgeber/{a['handle']}/", start_titel(a)) for a in alle if START_PHASE.get(a["handle"], a["phase"]) == phase]
        links += [l for l in START_EXTRA.get(phase, []) if l[0] not in {x[0] for x in links}]
        lis = "".join(f'<li><a href="{h}">{html.escape(t)}</a></li>' for h, t in links)
        return m.group(1) + (f"<ul>{lis}</ul>" if lis else "") + "</article>"
    neu, n = re.subn(r'(<article class="card phase"><p class="num">Phase \d</p><h3>([^<]+)</h3><p>[^<]*</p>)(?:<ul>.*?</ul>)?</article>', karte, seite)
    assert n == 4, f"Phasen-Karten auf der Startseite nicht gefunden ({n})"
    pfad.write_text(neu, encoding="utf-8")

# --------------------------------------------------------------------------- Über Cressida
UEBER_UNS_STAND = "2026-11-10"

def ueber_uns():
    url = f"{SITE}/ueber-uns/"
    titel = "Über Cressida: wer dahintersteht und wie wir prüfen | Cressida"
    desc = "Wer cressida.at betreibt, wie die Ratgeber zu Trennung und Scheidung entstehen und geprüft werden und wie sich die Seite finanziert."
    graph = [
        {"@type": "AboutPage", "@id": url, "url": url, "inLanguage": "de-AT", "about": {"@id": f"{SITE}/#organization"}},
        {"@type": "Organization", "@id": f"{SITE}/#organization", "name": "Cressida", "url": f"{SITE}/", "logo": f"{SITE}/icon.svg"},
        AUTOR,
    ]
    inhalt = """<main class="w narrow legal" style="padding-block:56px 72px">
<h1 style="font-size:clamp(30px,4vw,42px)">Über Cressida</h1>
<p><strong>Die kurze Antwort:</strong> cressida.at ist ein kostenloser Ratgeber zu Trennung und Scheidung in Österreich. Er wird von Mag. Anton Scharmitzer und der FRABANTO AUSTRIA GmbH in Wien herausgegeben. Jede Zahl, Frist und Gebühr prüfen wir an der amtlichen Quelle und versehen sie mit einem Prüfdatum.</p>
<h2>Wer steht dahinter?</h2>
<p>Herausgeber ist Mag. Anton Scharmitzer, Betriebswirt (Studium der Internationalen Betriebswirtschaft an der Universität Wien) und Geschäftsführer der FRABANTO AUSTRIA GmbH in Wien. Cressida ist keine Anwaltskanzlei und keine Beratungsstelle. Die Seite erklärt, wie Trennung und Scheidung in Österreich ablaufen, damit Sie vorbereitet in Gespräche mit Gericht, Beratungsstelle, Mediation oder Anwältin gehen.</p>
<h2>Wie entstehen die Ratgeber?</h2>
<ul>
<li>Recherche an amtlichen Quellen: oesterreich.gv.at, Justiz, Bundeskanzleramt, Rechtsinformationssystem (RIS) und Statistik Austria.</li>
<li>Jede Zahl, Frist und Gebühr wird an der Quelle geprüft. Was sich nicht belegen lässt, lassen wir weg und sagen das offen.</li>
<li>Jeder Ratgeber nennt seine Quellen und das Datum der letzten Prüfung. Beträge und Gebühren prüfen wir zum Jahreswechsel neu.</li>
<li>Alle Inhalte gelten für österreichisches Recht. Wir nehmen nicht Partei für eine Seite.</li>
</ul>
<h2>Wegweiser und Unterhaltsrechner</h2>
<p>Beide Werkzeuge rechnen nur in Ihrem Browser. Ihre Eingaben werden nicht an uns übertragen und nicht gespeichert. Die Ergebnisse sind Orientierungswerte; verbindlich ist immer die Entscheidung des Gerichts.</p>
<h2>Wie finanziert sich Cressida?</h2>
<p>Die Ratgeber und Werkzeuge sind kostenlos und ohne Werbung. Derzeit verdient Cressida kein Geld; die Seite wird von der FRABANTO AUSTRIA GmbH getragen. Sollte sich das ändern, steht es hier, bevor es gilt. Bezahlte Artikel gibt es nicht.</p>
<h2>Was Cressida nicht ist</h2>
<p>Wir ersetzen keine Rechtsberatung und beurteilen keinen Einzelfall. Dafür gibt es Familienberatungsstellen, die Arbeiterkammer, Mediatorinnen und Mediatoren sowie Anwältinnen und Anwälte. Bei Gewalt in der Beziehung geht Schutz vor: Frauenhelpline 0800 222 555, Polizei-Notruf 133.</p>
<h2>Fehler gefunden?</h2>
<p>Wenn sich eine Regel ändert oder Ihnen ein Fehler auffällt, schreiben Sie an <a href="mailto:office@frabanto.eu">office@frabanto.eu</a>. Wir korrigieren und aktualisieren das Prüfdatum.</p>
<p style="font-size:14px;color:var(--muted)">FRABANTO AUSTRIA GmbH · Theodor-Körner-Gasse 34, 1210 Wien · <a href="/impressum/">Impressum</a></p>
</main>"""
    stil = "<style>.legal h2{font-size:21px;margin:32px 0 8px}.legal p,.legal li{color:var(--body)}</style>\n</head>"
    return head(titel, desc, url, "website", graph).replace("</head>", stil) + f"\n<body>\n{header()}\n{inhalt}\n{FOOTER}\n</body>\n</html>\n"

def sitemap(alle):
    seiten = [("/", "2026-11-09"), ("/ratgeber/", max(a["modified"] for a in alle)),
              ("/wegweiser/", "2026-11-09"), ("/unterhaltsrechner/", "2026-11-09"), ("/ueber-uns/", UEBER_UNS_STAND)]
    seiten += [(f"/ratgeber/{a['handle']}/", a["modified"]) for a in alle]
    zeilen = "\n".join(f"  <url><loc>{SITE}{p}</loc><lastmod>{d}</lastmod></url>" for p, d in seiten)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{zeilen}\n</urlset>\n'

if __name__ == "__main__":
    for a in ARTIKEL:
        assert len(a["seo"]) <= 60, (a["handle"], len(a["seo"]))
        assert len(a["desc"]) <= 155, (a["handle"], len(a["desc"]))
        ziel = ROOT / "ratgeber" / a["handle"] / "index.html"
        ziel.parent.mkdir(parents=True, exist_ok=True)
        ziel.write_text(artikel_seite(a, ARTIKEL), encoding="utf-8")
        print("geschrieben:", ziel.relative_to(ROOT))
    (ROOT / "ratgeber" / "index.html").write_text(uebersicht(ARTIKEL), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(sitemap(ARTIKEL), encoding="utf-8")
    startseite_phasen(ARTIKEL)
    (ROOT / "ueber-uns").mkdir(exist_ok=True)
    (ROOT / "ueber-uns" / "index.html").write_text(ueber_uns(), encoding="utf-8")
    for rel, (pfad, titel, text) in FORM_SEITEN.items():
        z = ROOT / rel
        z.parent.mkdir(parents=True, exist_ok=True)
        z.write_text(info_seite(pfad, titel, text), encoding="utf-8")
    print("Übersicht, Startseiten-Listen, Über-uns, Formularseiten und sitemap.xml aktualisiert")
