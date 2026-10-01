#!/usr/bin/env python3
"""Build the two Gzenaya reel PDFs (client guide FR + internal playbook EN).

Writes client.html / interne.html next to this file; render.mjs turns them into PDFs.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def ar(text):
    """Inline Arabic/Darija run inside a LTR paragraph."""
    return f'<bdi dir="rtl" class="ar">{html.escape(text)}</bdi>'


# ---------------------------------------------------------------- hooks (shared)
HOOK_SECRET = "واش فراسك السر ديال كيفاش يجيك الزاج رقيق؟"
HOOK_STAT = ("8 من 10 ديال les consultations ديال moins dix، moins quatorze، moins dix-huit "
             "كيجيوني خايفين الزاج يبان كبير ف العين هكا، ولا يبومبي من قدام.")
HOOK_WARN = "رد البال باش ما تتقولبش."

# ---------------------------------------------------------------- voice lines (shared)
V = {
    1: [
        HOOK_SECRET + " هاد الزاج، خمّن شحال فيه: moins six؟ moins dix؟",
        "هادي moins treize. و يلا درتي ليها زاج غالي ف monture غالطة، غتخلص بزاف و يجيك الزاج غليظ.",
        "تلت حوايج: indice 1.74، monture en plastique صغيرة، maximum 47، و le centrage بالمليمتر على العين.",
        "شوف الجنب. ماشي غليظ. و العين ما كتصغرش. voilà كيفاش كتجي.",
    ],
    2: [
        "واش فراسك شنو كتقول هاد الدائرة على عينيك؟ يلا كاين شي خطوط باينين كحل من لخرين، خاصك تعرف هادشي.",
        "غمّض عين وحدة. خلي النظارات يلا كنتي كتلبسهم.",
        "واش كاع الخطوط عندهم نفس le noir؟ دابا بدّل العين. نفس السؤال.",
        "يلا شي خطوط باينين كثر، ممكن يكون عندك astigmatisme. هادا ماشي diagnostic. شوف l'ophtalmologue باش يقيس ليك مزيان.",
    ],
    3: [
        HOOK_WARN + " l'ordonnance ديالك: يلا ما فهمتيش هاد الأرقام، ممكن تخلص على زاج ما محتاجوش.",
        "SPH هي la sphère. moins: كتشوف مزيان من قريب، و ضبابة من بعيد. plus: العكس.",
        "CYL هو l'astigmatisme. و l'axe من 0 حتى 180. يلا تحركات النظارات على وجهك، l'axe كيتبدل.",
        "ADD كتبان من بعد الأربعين. هادي هي اللي كتقول لينا واش خاصك progressifs.",
    ],
    4: [  # unchanged on purpose
        "«واش les progressifs كيدوّخو؟» شوف، كيدوّخو غير يلا تخدمو غلط. و تقدر تخلص أغلى زاج و ما تشوفش مزيان.",
        "القاعدة الأولى: قسم الكادر على جوج. العين ديالك خاصها تجي الفوق من الخط. يلا جات ف الوسط ولا التحت، غتدوخ و ما غتشوفش مزيان.",
        "القاعدة الثانية: يلا أول مرة و ADD عندك وصل plus trois، صعيب تتعود. ابدا بكري، ف plus un ولا plus un et demi.",
        "و الدوخة ديال البداية عادية: دوّر راسك، ماشي عينيك. تلت أيام من الصباح لليل، و كتمشي. يلا بقات من بعد سيمانة، رجع عندنا نشوفو le centrage.",
    ],
    5: [
        HOOK_STAT + " يلا عندك moins huit و فوق، ما تختارش الكادر بحال هادا.",
        "غتخلص زاج غالي و يجيك غليظ. حل la branche، غتلقى هنا واحد الأرقام.",
        "هادا هو العرض ديال الزاج. ما تفوتش 49. أحسن 47.",
        "الزاج رقيق ف الوسط و غليظ ف الجناب. كلما كبر الكادر، كلما كبر الغلاظ. و من moins dix و فوق، ما ديرش le noir.",
    ],
    6: [  # conversation: (speaker key, line)
        [("Q", "«خلصت 2500 درهم ف النظارات و الزاج جا غليظ و تقيل. واش تشفرت؟»")],
        [("A", "ماشي ضروري. الغلظ ما كيجيش من الثمن، كيجي من l'indice. هاد تلت ديال الزاج عندهم نفس l'ordonnance. "
               "1.5 هو العادي، كافي ف correction صغيرة. 1.67 أرق، كنقترحوه من moins quatre و فوق.")],
        [("Q", "«أنا عندي moins dix. واش الزاج غيبان كبير ف العين ولا يبومبي من قدام؟»"),
         ("A", "لا. يلا درتي 1.74 ف monture صغيرة، و le centrage مضبوط على العين، الزاج كيبقى رقيق و ما كيبانش.")],
        [("Q", "«قالو ليا خاصك 1.74. واش بصح ولا غير باش نخلص كثر؟»"),
         ("A", "يلا عندك moins deux و قالو ليك 1.74، خلصتي على والو. و يلا عندك moins huit و درتي 1.5، "
               "الزاج غيجي غليظ. الرقم ديال l'ordonnance هو اللي كيقرر.")],
    ],
    7: [
        "رد البال: يلا ولدك كيقرّب بزاف للتلفزة، ما تقولش غير عادة.",
        "كاينين quatre signes: كيغمّض عينيه باش يشوف من بعيد، كيقرّب بزاف للكتاب، كيشكي بالراس ف العشية، و كيحك عينيه بزاف.",
        "يلا شفتي وحدة من هادو، أول حاجة: l'ophtalmologue. هو اللي كيدير l'examen.",
        "و يلا خصو نظارات: monture flexible، و الزاج ديما organique. ما كيتهرسش، و خفيف على الوجه.",
    ],
    8: [
        "واش فراسك بلي وحدة من هاد تلت ديال الكادرات غالية ب تلت مرات؟ شكون فيهم؟",
        "A: شوف la charnière. معدن، flexible.",
        "B: acétate. اللون داخل ف المادة، ماشي صباغة من فوق.",
        "C: خفيفة بزاف. و الجواب هو B. l'acétate ما كيتقشرش، و كيتعاود يتشكل على وجهك.",
    ],
}

TIMES = {
    1: ["0–5 s", "5–10 s", "10–20 s", "20–35 s", "35–40 s"],
    2: ["0–5 s", "5–8 s", "8–20 s", "20–34 s", "34–40 s"],
    3: ["0–5 s", "5–14 s", "14–26 s", "26–38 s", "38–45 s"],
    4: ["0–3 s", "3–16 s", "16–28 s", "28–40 s", "40–45 s"],
    5: ["0–8 s", "8–14 s", "14–22 s", "22–34 s", "34–40 s"],
    6: ["0–4 s", "4–15 s", "15–27 s", "27–39 s", "39–45 s"],
    7: ["0–3 s", "3–20 s", "20–28 s", "28–40 s", "40–45 s"],
    8: ["0–4 s", "4–14 s", "14–24 s", "24–34 s", "34–40 s"],
}

CTA = {
    "number": "Kteb l'correction dyalk f commentaire: -6? -10? Add?",
    "test": "Galli chnou chfti: l'khtout kamlin kif kif wla la?",
    "save": "Sauvegardi had l'vidéo, ghadi t7tajha nhar tchri nnaddarat",
    "send": "Sifto l chi wa7ed f 3a2iltek kayb3ed t'téléphone bach y9ra",
    "series": "Tab3ni, kol simana kanjawb 3la so2al wa7ed 3la chouf dyalk",
    "ask": "Sewwelni ay so2al 3la progressifs f commentaire, w njawbek b video",
    "story": "Nta chhal hadi w nta labes nnaddarat?",
    "dm": "Sift 'GUIDE' f DM, nsift lik chnou tsewwel l'opticien 9bel ma tchri progressifs",
}

CSS = """
@font-face { font-family: "Noto Sans Arabic"; font-weight: 400; src: url("fonts/NotoSansArabic-Regular.ttf"); }
@font-face { font-family: "Noto Sans Arabic"; font-weight: 700; src: url("fonts/NotoSansArabic-Bold.ttf"); }
@page { size: A4; margin: 12mm 12mm 12mm 12mm; }
* { box-sizing: border-box; }
:root {
  --navy: #1f2a44; --teal: #127566; --teal-l: #dff1ee; --red: #b4231c; --orange: #b4530e;
  --slate: #475569; --grey: #f2f3f6; --line: #d9dce3; --cream: #fcefdc; --pink: #fbe3e3; --ink: #1f2937; --mute: #6b7280;
}
html, body { margin: 0; padding: 0; background: #fff; }
body { font-family: Arial, "Liberation Sans", Helvetica, sans-serif; color: var(--ink); font-size: 14px; line-height: 1.45; }
.ar { font-family: "Noto Sans Arabic", Arial, sans-serif; }
.page { break-after: page; }
.page:last-child { break-after: auto; }
.banner { background: var(--navy); color: #fff; border-radius: 5px; padding: 14px 16px 12px; margin-bottom: 12px; }
.banner.teal { background: var(--teal); }
.banner h1 { margin: 0; font-size: 24px; line-height: 1.3; }
.banner .sub { font-size: 12px; opacity: .85; margin-top: 4px; }
.tag { display: inline-block; vertical-align: middle; background: #fff; color: var(--ink); font-size: 11px; font-weight: bold;
       border-radius: 9px; padding: 1px 8px; margin-left: 4px; }
h1.plain { font-size: 24px; margin: 0 0 8px; color: var(--navy); }
h2 { font-size: 18px; color: var(--navy); margin: 16px 0 8px; }
h2.red { color: var(--red); }
h2 .ph { color: var(--teal); }
h2 em { font-weight: normal; font-size: 13px; color: var(--mute); }
p.lead { color: var(--mute); margin: 0 0 10px; }
.callout { background: var(--teal-l); border-radius: 5px; padding: 9px 12px; margin: 10px 0; }
.callout.pink { background: var(--pink); }
.callout .k { color: var(--red); font-weight: bold; }
.kit { background: var(--teal-l); border-radius: 5px; padding: 10px 12px; font-size: 12px; margin-top: 14px; }
.kit .lab { color: var(--teal); font-weight: bold; font-size: 10px; letter-spacing: .06em; text-transform: uppercase; margin-bottom: 2px; }
ul { margin: 6px 0; padding-left: 16px; }
li { margin: 3px 0; }
table { width: 100%; border-collapse: collapse; }
table.rules td { padding: 7px 8px; background: var(--grey); border-bottom: 2px solid #fff; vertical-align: middle; }
table.rules td.n { background: var(--teal); color: #fff; font-weight: bold; text-align: center; width: 34px; font-size: 13px; }
table.rules.big td.n { font-size: 20px; }
table.rules td.t { font-weight: bold; width: 210px; }
table.rules td.d { font-size: 13px; }
table.std th { background: var(--navy); color: #fff; font-size: 9.5px; letter-spacing: .06em; text-transform: uppercase; text-align: left; padding: 7px 8px; }
table.std.teal th { background: var(--teal); }
table.std td { padding: 7px 8px; border-bottom: 1px solid var(--line); vertical-align: top; font-size: 13px; }
table.std tr:nth-child(odd) td { background: var(--grey); }
table.std tr:nth-child(even) td { background: #fff; }
table.std td.b { font-weight: bold; }
table.std td.i { font-style: italic; }
table.std td.ph-k { color: var(--teal); font-weight: bold; }
table.std td.ph-l { color: var(--navy); font-weight: bold; }
.win { color: var(--teal); font-weight: bold; font-size: 15px; }
.flop { color: var(--red); font-weight: bold; font-size: 15px; }
.stats { display: flex; gap: 8px; margin-bottom: 6px; }
.stat { flex: 1; border-radius: 5px; padding: 12px; background: var(--grey); }
.stat.t { background: var(--teal-l); } .stat.o { background: var(--cream); }
.stat .lab { font-size: 10px; font-weight: bold; letter-spacing: .06em; color: var(--teal); }
.stat.o .lab, .stat.o .big { color: var(--orange); }
.stat .big { font-size: 26px; font-weight: bold; color: var(--teal); margin: 2px 0; }
.stat .s { font-size: 11.5px; color: var(--mute); }
.steps { display: flex; gap: 4px; margin: 6px 0 4px; align-items: flex-start; }
.step { flex: 1; }
.step .h { color: #fff; padding: 6px 8px; border-radius: 4px 4px 0 0; font-size: 11px; font-weight: bold; }
.step .h span { display: block; font-weight: normal; font-size: 10px; opacity: .85; }
.step .b { background: var(--grey); padding: 7px 8px; font-size: 13px; border-radius: 0 0 4px 4px; }
.c-navy { background: var(--navy); } .c-red { background: var(--red); } .c-teal { background: var(--teal); }
.c-orange { background: var(--orange); } .c-slate { background: var(--slate); }
.cards { display: flex; gap: 6px; margin-bottom: 10px; }
.card { flex: 1; background: var(--grey); border-radius: 5px; padding: 8px 9px; }
.card:first-child, .card:nth-child(2) { flex: .62; }
.card .lab { font-size: 9.5px; letter-spacing: .06em; color: var(--mute); font-weight: bold; text-transform: uppercase; }
.card .v { font-weight: bold; font-size: 14px; margin-top: 2px; }
table.script { table-layout: fixed; }
table.script th { background: var(--navy); color: #fff; font-size: 9.5px; letter-spacing: .06em; text-transform: uppercase; text-align: left; padding: 7px 8px; }
table.script th.vh { text-align: right; }
table.script td { border: 1px solid var(--line); padding: 8px; vertical-align: top; font-size: 13.5px; }
table.script td.tm { width: 72px; font-weight: bold; }
table.script td.tm span { display: block; text-transform: uppercase; font-size: 9.5px; letter-spacing: .06em; color: var(--mute); font-weight: bold; margin-top: 3px; }
table.script td.see { width: 180px; }
table.script td.scr { width: 122px; font-weight: bold; }
table.script td.voice { text-align: right; }
table.script td.voice .ar { font-size: 16px; line-height: 1.85; display: block; }
table.script tr.hook td { background: var(--teal-l); }
table.script tr.hook td.tm { color: var(--teal); }
table.script tr.cta td { background: var(--cream); }
table.script tr.cta td.tm { color: var(--orange); }
table.script tr.cta td.voice { text-align: left; font-weight: bold; font-style: italic; }
.spk { display: block; text-align: left; font-size: 9.5px; letter-spacing: .06em; text-transform: uppercase; font-weight: bold; margin-top: 4px; }
.spk.q { color: var(--orange); } .spk.a { color: var(--teal); }
.spk:first-child { margin-top: 0; }
.boxes { break-inside: avoid; display: flex; gap: 8px; margin-top: 10px; }
.box { flex: 1; border-radius: 5px; padding: 10px 12px; font-size: 12px; }
.box.t { background: var(--teal-l); } .box.o { background: var(--cream); }
.box .lab { font-size: 10px; font-weight: bold; letter-spacing: .06em; text-transform: uppercase; margin-bottom: 4px; }
.box.t .lab { color: var(--teal); } .box.o .lab { color: var(--orange); }
.box ul { margin: 0; }
.method { font-size: 10.5px; color: var(--mute); margin-top: 14px; }
"""


def doc(title, lang, pages):
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>{CSS}</style></head><body>
{''.join(f'<section class="page">{p}</section>' for p in pages)}
</body></html>"""


def banner(title, sub, color="navy", tag=None):
    t = f' <span class="tag">{tag}</span>' if tag else ""
    cls = "banner teal" if color == "teal" else "banner"
    return f'<div class="{cls}"><h1>{title}{t}</h1><div class="sub">{sub}</div></div>'


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def std_table(headers, rows, cls="std", widths=None):
    w = widths or [None] * len(headers)
    th = "".join((f'<th style="width:{x}">' if x else "<th>") + f"{h}</th>" for h, x in zip(headers, w))
    body = ""
    for r in rows:
        body += "<tr>" + "".join(
            (f'<td class="{c[0]}">{c[1]}</td>' if isinstance(c, tuple) else f"<td>{c}</td>") for c in r) + "</tr>"
    return f'<table class="{cls}"><tr>{th}</tr>{body}</table>'


def steps(items):
    out = '<div class="steps">'
    for color, name, t, body in items:
        out += f'<div class="step"><div class="h c-{color}">{name}<span>{t}</span></div><div class="b">{body}</div></div>'
    return out + "</div>"


def voice_cell(v, speakers):
    if isinstance(v, list):
        parts = []
        for who, line in v:
            parts.append(f'<span class="spk {"q" if who == "Q" else "a"}">{speakers[who]}</span>'
                         f'<span dir="rtl" class="ar">{html.escape(line)}</span>')
        return "".join(parts)
    return f'<span dir="rtl" class="ar">{html.escape(v)}</span>'


def reel_page(r, L):
    """r: reel spec, L: language labels."""
    sub = r["sub"]
    out = banner(r["title"], sub, r["color"], r.get("tag"))
    out += '<div class="cards">' + "".join(
        f'<div class="card"><div class="lab">{lab}</div><div class="v">{val}</div></div>'
        for lab, val in zip(L["cards"], r["cards"])) + "</div>"
    hdr = L["cols"][:]
    if r.get("voice_header"):
        hdr[3] = r["voice_header"]
    out += (f'<table class="script"><colgroup><col style="width:72px"><col style="width:170px">'
            f'<col style="width:118px"><col></colgroup><tr><th>{hdr[0]}</th><th>{hdr[1]}</th><th>{hdr[2]}</th>'
            f'<th class="vh">{hdr[3]}</th></tr>')
    times = TIMES[r["n"]]
    voices = V[r["n"]]
    for i in range(4):
        cls = ' class="hook"' if i == 0 else ""
        see, scr = r["rows"][i]
        out += (f'<tr{cls}><td class="tm">{times[i]}<span>{L["steps"][i]}</span></td>'
                f'<td class="see">{see}</td><td class="scr">{scr}</td>'
                f'<td class="voice">{voice_cell(voices[i], L.get("speakers", {}))}</td></tr>')
    see, scr = r["rows"][4]
    out += (f'<tr class="cta"><td class="tm">{times[4]}<span>{L["steps"][4]}</span></td>'
            f'<td class="see">{see}</td><td class="scr">{scr}</td><td class="voice">{CTA[r["cta"]]}</td></tr></table>')
    if r.get("important"):
        k, txt = r["important"]
        out += f'<div class="callout pink"><span class="k">{k}</span> {txt}</div>'
    out += (f'<div class="boxes"><div class="box t"><div class="lab">{L["before"]}</div>{ul(r["before"])}</div>'
            f'<div class="box o"><div class="lab">{L["after"]}</div>{ul(r["after"])}</div></div>')
    return out


# ====================================================================== CLIENT (FR)
def client():
    L = {
        "cards": ["Durée", "Étiquette", "Dans la main dès le début", "Phrase de fin"],
        "cols": ["Temps", "Ce qu'on voit", "À l'écran", "Ce que vous dites (darija + français)"],
        "steps": ["Accroche", "L'erreur", "La règle", "La preuve", "Fin"],
        "before": "Avant de filmer", "after": "Après le montage",
        "speakers": {"Q": "Saad (hors champ)", "A": "Vous"},
    }

    def before(badge):
        return ["Le produit est dans votre main avant le premier mot", "Lancez la vidéo, comptez 1, parlez",
                f"L'étiquette « {badge} » en haut à gauche, dès le début"]

    def after(sec):
        return ["Coupez tous les silences de plus d'une seconde",
                f"Durée proche de {sec} s, la phrase de fin dite d'un seul souffle",
                "Sous-titres en darija, 7 mots maximum par ligne"]

    P1 = "Phase 1 · « Ça parle de moi »"
    P2 = "Phase 2 · « Je lui fais confiance »"
    fin = "Phrase de fin à l'écran"
    reels = [
        dict(n=1, title="Vidéo 1 · Devine la correction", sub=f"{P1} · 40 s", color="teal", cta="number",
             cards=["40 s", "? → −13", "Le verre (ou la paire) −13 terminé", "Commente ta correction"],
             rows=[("Le bord du verre poussé vers la caméra, votre visage derrière", "Étiquette « ? »"),
                   ("Vous reculez le verre, visage face caméra", ""),
                   ("Photo de la vraie ordonnance, −13 entouré en vert", "Étiquette « −13 »"),
                   ("Le bord du verre de profil, puis vous mettez la paire (clip solaire)", "1.74 · 47"),
                   ("Face caméra, verre en main", fin)],
             before=before("? → −13"), after=after(40)),
        dict(n=2, title="Vidéo 2 · Test d'astigmatisme en 10 secondes", sub=f"{P1} · 40 s", color="teal", cta="test",
             cards=["40 s", "TEST 10 s", "Le cadran du test, imprimé sur une carte", "Commente ton résultat"],
             rows=[("Vous approchez la carte jusqu'à remplir l'écran", "TEST 10 s"),
                   ("Vous cachez un œil avec la main", ""),
                   ("La carte remplit l'écran, compte à rebours de 10 s", "10 · 9 · 8 …"),
                   ("Face caméra, carte en main", "« Ce n'est pas un diagnostic »"),
                   ("Face caméra", fin)],
             before=before("TEST 10 s"), after=after(40)),
        dict(n=3, title="Vidéo 3 · Lire son ordonnance en 30 secondes", sub=f"{P1} · 45 s", color="teal", cta="send",
             cards=["45 s", "SPH · CYL · AXE · ADD", "Une vraie ordonnance (nom caché)", "Envoie-la à un proche"],
             rows=[("L'ordonnance poussée vers la caméra", "SPH · CYL · AXE · ADD"),
                   ("Photo de l'ordonnance, SPH entouré en vert", "SPH"),
                   ("Le cercle vert passe sur CYL puis AXE", "CYL · AXE"),
                   ("Cercle vert sur ADD, puis un verre progressif en main", "ADD +1.50"),
                   ("Face caméra, ordonnance en main", fin)],
             before=before("SPH · CYL · AXE · ADD"), after=after(45)),
        dict(n=4, title="Vidéo 4 · Réponse à un commentaire : « Les progressifs donnent le vertige ? »",
             tag="Réponse à un commentaire", sub=f"{P2} · 45 s", color="navy", cta="ask",
             cards=["45 s", "Progressif", "Une monture haute et une monture trop basse", "Pose-moi ta question"],
             rows=[("Autocollant « réponse au commentaire » à l'écran dès la 1re image. Deux montures levées vers la caméra",
                    "Commentaire + « Progressif »"),
                   ("Vous tenez la monture basse et tracez une ligne au milieu avec le doigt", "Règle 1"),
                   ("Vous mettez la monture haute : l'œil est en haut de la monture", "Règle 2 · ADD +3.00"),
                   ("Ordonnance avec ADD entouré en vert, puis vous tournez la tête au lieu des yeux", "3 jours"),
                   ("Face caméra", fin)],
             important=("Important :", "Utilisez un vrai commentaire reçu (nom caché). Si vous n'en avez pas encore, "
                        f"écrivez à l'écran « {ar('سؤال كيجيني بزاف')} » au lieu d'inventer un commentaire."),
             before=before("Progressif"), after=after(45)),
        dict(n=5, title="Vidéo 5 · Même correction, 2 montures", sub=f"{P1} · 40 s", color="teal", cta="number",
             cards=["40 s", "−8 · A / B", "Une grande monture en métal et une petite en acétate", "Commente ta correction"],
             rows=[("Les deux montures levées vers la caméra. Au mot « هكا », vous montrez avec la main", "Étiquette « −8 »"),
                   ("Vous ouvrez la branche de la grande monture, près de la caméra", ""),
                   ("Gros plan sur les chiffres gravés de la branche, entourés en vert", "45 – 49 max"),
                   ("Le bord de chaque verre de profil, puis vous portez la petite", "A ❌ · B ✅"),
                   ("Face caméra, petite monture sur le nez", fin)],
             important=("Important :", "dites « 8 sur 10 » seulement si c'est vrai dans vos consultations. "
                        f"Sinon dites « {ar('أغلب')} » (la plupart)."),
             before=before("−8 · A / B"), after=after(40)),
        dict(n=6, title="Vidéo 6 · Conversation : 3 questions sur les verres épais", tag="Conversation",
             sub=f"{P1} · 45 s · Saad pose les questions derrière la caméra", color="teal", cta="save",
             cards=["45 s", "1.5 · 1.67 · 1.74", "3 verres avec la même ordonnance", "Enregistre la vidéo"],
             voice_header="Qui parle · ce qu'on dit (darija + français)",
             rows=[("Saad tient le téléphone et pose la question hors champ. Vous : 3 verres en éventail en main",
                    "Question 1 + étiquette"),
                   ("Le bord du verre 1.5 près de la caméra, puis le 1.67", "1.5 · 1.67"),
                   ("Question de Saad, puis le bord du verre 1.74 face caméra, à côté d'une petite monture", "Question 2 · 1.74"),
                   ("Question de Saad, puis les 3 verres côte à côte, du plus épais au plus fin", "Question 3"),
                   ("Face caméra, les 3 verres en main", fin)],
             important=("Important :", "ne lisez pas vos réponses, parlez comme à un client au comptoir. Ces 3 "
                        "questions sont les 3 peurs de vos clients : payé trop cher, verre épais, verre qui se voit."),
             before=["Les 3 verres dans votre main avant la première question",
                     "Saad lance la vidéo et pose la question 1 direct",
                     "Étiquette « 1.5 · 1.67 · 1.74 » en haut à gauche"],
             after=["Chaque question de Saad écrite à l'écran",
                    "Durée proche de 45 s, phrase de fin d'un seul souffle",
                    "Sous-titres en darija, 7 mots maximum par ligne"]),
        dict(n=7, title="Vidéo 7 · Enfants : 4 signes", sub=f"{P2} · 45 s", color="navy", cta="story",
             cards=["45 s", "4 – 12 ans", "Une petite monture souple avec verres organiques", "Raconte ton histoire"],
             rows=[("La monture enfant levée vers la caméra", "Étiquette « 4 – 12 ans »"),
                   ("Vous comptez sur vos doigts, monture en main", "1 · 2 · 3 · 4"),
                   ("Face caméra", "« Ophtalmologue d'abord »"),
                   ("Vous pliez la branche souple, puis montrez le verre organique", "Toujours l'organique"),
                   ("Face caméra", fin)],
             before=before("4 – 12 ans"), after=after(45)),
        dict(n=8, title="Vidéo 8 · Test à l'aveugle : quelle monture est la plus chère ?", sub=f"{P2} · 40 s",
             color="navy", cta="series",
             cards=["40 s", "A · B · C", "3 montures, lettres A, B, C", "Abonne-toi pour la série"],
             rows=[("Trois montures en éventail vers la caméra", "A · B · C"),
                   ("Monture A : la charnière près de la caméra", "A"),
                   ("Monture B : le bord en acétate face caméra", "B"),
                   ("Monture C dans la paume (le poids), puis la réponse", "B ✅"),
                   ("Face caméra, B sur le nez", fin)],
             before=before("A · B · C"), after=after(40)),
    ]

    p1 = banner("Vos reels Instagram : la méthode", "Gzenaya Optique Tanger · Guide de tournage · Octobre 2026")
    p1 += ('<div class="callout"><b>En une phrase :</b> on a étudié 34 vidéos d\'un opticien marocain qui fait '
           "jusqu'à 213 000 vues. Les vidéos qui marchent suivent toutes les 7 règles ci-dessous. Le même sujet mal "
           "filmé fait 10 fois moins de vues.</div>")
    p1 += "<h2>Les 7 règles</h2><table class=\"rules\">"
    rules = [
        ("Parlez tout de suite", "Le premier mot avant 1 seconde. Pas de « salam », pas de présentation, pas de "
         "« aujourd'hui je vais vous montrer »."),
        ("Ouvrez avec une phrase qui accroche", f"Une question : « {ar(HOOK_SECRET)} ». Un chiffre : « {ar('8 من 10 ديال les consultations…')} ». "
         f"Un avertissement : « {ar(HOOK_WARN)} ». Ou lisez directement les chiffres d'une vraie ordonnance."),
        ("Dites l'erreur qui coûte cher", "Dans les 5 premières secondes : payer cher et avoir des verres épais, "
         "lourds, ou mal voir."),
        ("Le produit dans la main", "Monture, verre ou ordonnance dans votre main dès la première image. "
         "Approchez-le de la caméra."),
        ("Un seul chiffre simple", "« 47 maximum », « +3.00 », « à partir de −10, pas de monture noire ». Le client "
         "vérifie sur sa propre ordonnance."),
        ("Montrez la preuve", "Le bord du verre face caméra, l'ordonnance, puis les lunettes sur le visage."),
        ("Une seule prise, dans la boutique", "Téléphone à la main, les étagères de montures derrière vous. "
         "40 à 45 secondes."),
    ]
    for i, (t, d) in enumerate(rules, 1):
        p1 += f'<tr><td class="n">{i}</td><td class="t">{t}</td><td class="d">{d}</td></tr>'
    p1 += "</table><h2>Pourquoi ça marche avec vos clients</h2>" + ul([
        "Vos clients ont peur de payer cher et d'avoir des verres épais, lourds, ou de mal voir. La vidéo parle de "
        "cette peur dès le début.",
        "Le chiffre leur permet de vérifier sur leur propre ordonnance : « moi j'ai −10, donc pas de monture noire ». "
        "Ils se sentent concernés et ils commentent.",
        "Ils voient le vrai verre, la vraie ordonnance et le résultat sur un visage, dans votre boutique. Ils vous "
        "font confiance sans que vous ayez besoin de vendre.",
    ])

    p2 = '<h1 class="plain">Une vidéo = 5 étapes (40 à 45 secondes)</h1>'
    p2 += steps([
        ("navy", "ACCROCHE", "0–5 s", "La phrase d'accroche + le produit dans la main. Premier mot avant 1 seconde"),
        ("red", "L'ERREUR", "5–10 s", "Ce que ça coûte : argent, verre épais, mal voir"),
        ("teal", "LA RÈGLE", "10–22 s", "Un chiffre à vérifier. Ordonnance entourée en vert"),
        ("orange", "LA PREUVE", "22–36 s", "Le bord du verre face caméra, puis les lunettes sur le visage"),
        ("slate", "PHRASE DE FIN", "36–42 s", "Une seule phrase (voir page suivante)"),
    ])
    p2 += "<h2>Les 3 phrases d'accroche</h2>"
    p2 += std_table(["Type", "Ce que vous dites", "Vidéos"], [
        [("b", "La question"), ar(HOOK_SECRET), "1 · 2 · 8"],
        [("b", "Le chiffre"), ar(HOOK_STAT), "5"],
        [("b", "L'avertissement"), ar(HOOK_WARN), "3 · 7"],
    ], widths=["130px", None, "70px"])
    p2 += ('<p class="lead" style="margin-top:6px">La vidéo 4 commence par le commentaire du client, la vidéo 6 par '
           "la question de Saad. Adaptez la fin de la phrase au produit que vous tenez.</p>")
    p2 += '<h2 class="red">À ne jamais faire</h2>' + ul([
        "Filmer de loin avec un trépied, derrière le bureau", "Filmer l'écran de l'ordinateur",
        "Montrer seulement les mains, sans votre visage", "Parler sans rien montrer",
        "Commencer par « salam », « aujourd'hui je vais… » ou une question vague qui ne promet rien",
    ])
    p2 += "<h2>Deux formats spéciaux</h2>" + ul([
        "<b>Réponse à un commentaire (vidéo 4)</b> : vous lisez la question d'un client à voix haute, puis vous "
        "répondez. Mêmes règles : le produit en main, un chiffre.",
        "<b>Conversation (vidéo 6)</b> : Saad, derrière la caméra, vous pose 3 questions que vos clients ont peur de "
        "poser (« j'ai payé cher et mes verres sont épais », « mon verre va se voir ? », « on m'a dit 1.74, c'est "
        "vrai ? »). Vous répondez face caméra, les verres en main.",
        f"Pour la vidéo 4 : utilisez un <b>vrai</b> commentaire reçu, avec le nom caché. Si vous n'en avez pas encore, "
        f"écrivez à l'écran « {ar('سؤال كيجيني بزاف')} » (une question qu'on me pose souvent). N'inventez jamais une "
        "fausse capture.",
    ])
    p2 += ('<div class="kit"><div class="lab">Le matériel</div>iPhone à hauteur de poitrine, un peu en dessous du '
           "visage, en vertical · Les étagères de montures derrière vous · Un micro-cravate · Le chiffre important "
           "dans une étiquette blanche en haut à gauche · Ordonnances : cachez le nom du patient, entourez le chiffre "
           f"en vert · Sous-titres en darija · Vous êtes opticien, pas médecin : si ça ressemble à une maladie, dites "
           f"« {ar('شوف')} l'ophtalmologue ».</div>")

    p3 = '<h1 class="plain">Les phrases de fin</h1><p class="lead">Chaque vidéo finit par <b>une seule</b> de ces ' \
         "phrases. Dites-la d'un seul souffle, le produit toujours en main.</p>"
    hdr = ["Phrase", "Ce que vous dites", "Pourquoi"]
    wd = ["170px", "270px", None]
    p3 += '<h2><span class="ph">Phase 1</span> <em>« Ça parle de moi »</em></h2>'
    p3 += std_table(hdr, [
        [("b", "Commente ta correction"), ("i", CTA["number"]), "Les gens écrivent leur chiffre. On voit qui a une "
         "forte correction, et Instagram montre la vidéo à plus de monde."],
        [("b", "Commente ton résultat"), ("i", CTA["test"]), "Il vient de faire le test. Répondre ne lui coûte rien."],
        [("b", "Enregistre la vidéo"), ("i", CTA["save"]), "Quelqu'un qui enregistre la vidéo pense acheter bientôt."],
        [("b", "Envoie-la à un proche"), ("i", CTA["send"]), "Le client de 40 à 55 ans reçoit souvent la vidéo de "
         "son fils ou de sa fille."],
    ], cls="std teal", widths=wd)
    p3 += '<h2>Phase 2 <em>« Je lui fais confiance »</em></h2>'
    p3 += std_table(hdr, [
        [("b", "Abonne-toi pour la série"), ("i", CTA["series"]), "On promet le prochain épisode, donc les gens "
         "reviennent."],
        [("b", "Pose-moi ta question"), ("i", CTA["ask"]), "Chaque question devient une nouvelle vidéo, et la "
         "personne se sent écoutée."],
        [("b", "Raconte ton histoire"), ("i", CTA["story"]), "Les gens parlent d'eux, et ils s'attachent à vous."],
        [("b", "Écris « GUIDE » en message privé"), ("i", CTA["dm"]), "On offre une petite liste gratuite, on ne "
         "vend rien. Ça ouvre une conversation en privé."],
    ], widths=wd)
    p3 += "<h2>Quelle phrase pour quelle vidéo</h2>"
    p3 += std_table(["#", "Vidéo", "Phrase de fin"], [
        [("b", "1"), ("i", "Devine la correction"), "Commente ta correction"],
        [("b", "2"), ("i", "Test d'astigmatisme en 10 secondes"), "Commente ton résultat"],
        [("b", "3"), ("i", "Lire son ordonnance en 30 secondes"), "Envoie-la à un proche"],
        [("b", "4"), ("i", "Réponse à un commentaire : « Les progressifs donnent le vertige ? »"), "Pose-moi ta question"],
        [("b", "5"), ("i", "Même correction, 2 montures"), "Commente ta correction"],
        [("b", "6"), ("i", "Conversation : 3 questions sur les verres épais"), "Enregistre la vidéo"],
        [("b", "7"), ("i", "Enfants : 4 signes"), "Raconte ton histoire"],
        [("b", "8"), ("i", "Test à l'aveugle : quelle monture est la plus chère ?"), "Abonne-toi pour la série"],
    ], widths=["40px", None, "250px"])

    pl = '<h1 class="plain">Dans quel ordre publier</h1>'
    pl += std_table(["Semaine", "Vidéos", "Pourquoi"], [
        [("b", "1"), ("i", "5 · Même correction, 2 montures<br>1 · Devine la correction"),
         "Ce sont les deux formats qui font le plus de vues. Ils font commenter les gens avec leur chiffre."],
        [("b", "2"), ("i", "4 · Réponse à un commentaire<br>2 · Test d'astigmatisme"),
         "Les vidéos de la semaine 1 vous auront apporté de vrais commentaires pour la vidéo 4. Le test fait "
         "beaucoup commenter."],
        [("b", "3"), ("i", "3 · Lire son ordonnance<br>6 · Conversation : 3 questions"),
         "Les gens les enregistrent pour le jour où ils viennent acheter. La vidéo 6 répond aux peurs de vos clients."],
        [("b", "4"), ("i", "7 · Enfants : 4 signes<br>8 · Test à l'aveugle"),
         "Pour que les gens s'attachent à vous et suivent la série."],
    ], widths=["85px", "250px", None])
    pl += "<h2>À préparer avant de filmer</h2>" + ul([
        "Un ou deux vrais clients avec une forte correction (−8, −13), d'accord par écrit pour montrer leur "
        "ordonnance (nom caché)",
        "Les verres que vous avez vraiment en stock (1.5, 1.6, 1.67, 1.74) et les tailles de montures pour la vidéo 5",
        "Les vraies montures et les vrais prix pour la vidéo 8",
        "Des captures de vrais commentaires pour la vidéo 4 (nom caché)",
        f"Le « 8 sur 10 » de la vidéo 5 : dites-le seulement si c'est vrai chez vous, sinon « {ar('أغلب')} » (la plupart)",
        "Un moment avec Saad pour la vidéo 6 : il tient le téléphone et pose les 3 questions",
        "La même personne devant la caméra dans toutes les vidéos : les clients font confiance à un visage",
    ])
    pl += ('<div class="callout"><b>Le plus important :</b> le produit dans la main, une phrase d\'accroche tout de '
           "suite, un chiffre simple, la preuve, une phrase de fin. Si vous ne retenez qu'une chose, c'est ça.</div>")

    pages = [p1, p2, p3] + [reel_page(r, L) for r in reels] + [pl]
    return doc("Gzenaya · Guide des reels", "fr", pages)


# ====================================================================== INTERNAL (EN)
def internal():
    L = {
        "cards": ["Length", "Badge", "Object in frame 1", "CTA"],
        "cols": ["Time", "What we see", "On screen", "Voice (darija + fr)"],
        "steps": ["Hook", "Mistake", "Rule", "Proof", "CTA"],
        "before": "Before you film", "after": "Check after the edit",
        "speakers": {"Q": "Saad (off camera)", "A": "Optician"},
    }

    def before(badge):
        return ["Object in hand and in frame before you say the first word",
                "First word before 0.7 s: start recording, count 1, talk",
                f"Badge \"{badge}\" top left, in the first frame"]

    def after(sec):
        return ["No pause longer than 1.5 s (cut it)", f"Length close to {sec} s, CTA said in one breath",
                "Darija captions on, 7 words or fewer per line"]

    reels = [
        dict(n=1, title="Reel 1 · Guess the correction", color="teal", cta="number",
             sub="Know phase · 40 s · Pattern: Benjelloun 183K (reads the real numbers, lens in hand) + 67K (−14, "
                 "\"47 maximum\") · Hook: secret question",
             cards=["40 s", "? → −13", "The finished −13 lens/pair", "Comment your number"],
             rows=[("Lens edge pushed into the camera, his face behind it", "Badge ?"),
                   ("Pulls the lens back, face to camera", ""),
                   ("Overlay: photo of the real prescription, green circle on −13", "Badge −13"),
                   ("Lens edge side-on to camera, then he puts the pair on (sun clip on and off)", "1.74 · 47"),
                   ("Face to camera, lens still in hand", "CTA text")],
             before=before("? → −13"), after=after(40)),
        dict(n=2, title="Reel 2 · Astigmatism self-test", color="teal", cta="test",
             sub="Know phase · 40 s · Pattern: Optinova self-test 303K (vs 1.2K median) rebuilt in Benjelloun's "
                 "one-take selfie style · Hook: secret question",
             cards=["40 s", "TEST 10 s", "Printed astigmatism dial card", "Comment your test result"],
             rows=[("He pushes the printed dial card toward the lens until it fills the frame", "Badge TEST 10 s"),
                   ("Covers one eye with his hand", ""),
                   ("Card fills the frame, 10-second countdown", "10 · 9 · 8 …"),
                   ("Face to camera, card in hand", "\"Ce n'est pas un diagnostic\""),
                   ("Face to camera", "CTA text")],
             before=before("TEST 10 s"), after=after(40)),
        dict(n=3, title="Reel 3 · Read your prescription in 30 seconds", color="teal", cta="send",
             sub="Know phase · 45 s · Pattern: Benjelloun prescription overlays (5 of 8 viral) + tt 53K "
                 "\"Addition +3.00\" · Hook: warning",
             cards=["45 s", "SPH · CYL · AXE · ADD", "A real prescription (name hidden)", "Send it to someone"],
             rows=[("Prescription pushed toward the camera", "Badge SPH · CYL · AXE · ADD"),
                   ("Overlay: prescription photo, green circle on SPH", "SPH"),
                   ("Green circle moves to CYL and AXE", "CYL · AXE"),
                   ("Green circle on ADD, then he holds a progressive lens", "ADD +1.50"),
                   ("Face to camera, prescription in hand", "CTA text")],
             before=before("SPH · CYL · AXE · ADD"), after=after(45)),
        dict(n=4, title="Reel 4 · Comment reply: \"Do progressives make you dizzy?\"", tag="Comment reply",
             color="navy", cta="ask",
             sub="Like phase · 45 s · Pattern: Reply-to-comment format. Angle and hook kept from Benjelloun 139K "
                 "(frame split in two) + tt 53K (+3.00)",
             cards=["45 s", "Progressif", "A tall frame and a too-short frame", "Ask him a question"],
             rows=[("Instagram \"reply to comment\" sticker on screen from frame 1; two frames in hand raised to the lens",
                    "Comment sticker + badge Progressif"),
                   ("Holds the short frame, draws a line through its middle with a finger", "Rule 1"),
                   ("Puts the tall frame on: the eye sits high in the frame", "Rule 2 ADD +3.00"),
                   ("Prescription with ADD circled in green, then he turns his head instead of his eyes", "3 jours"),
                   ("Face to camera", "CTA text")],
             important=("Authenticity:", "Use a real comment the account received (name hidden). Until one comes in, "
                        f"write «{ar('سؤال كيجيني بزاف')}» on screen instead of showing a made-up comment."),
             before=before("Progressif"), after=after(45)),
        dict(n=5, title="Reel 5 · Same correction, 2 frames", color="teal", cta="number",
             sub="Know phase · 40 s · Pattern: Benjelloun 213K \"Le choix de la monture\" + 67K \"Monture 47, le noir "
                 "non\" + 26.8K \"−10 et plus oublie le noir\" · Hook: number",
             cards=["40 s", "−8 · A / B", "A big metal frame and a small acetate frame", "Comment your number"],
             rows=[("Both frames raised to the lens; hand gesture on \"هكا\"", "Badge −8"),
                   ("Opens the temple of the big metal frame, close to the camera", ""),
                   ("Overlay: close-up of the temple engraving, size circled in green", "45 – 49 max"),
                   ("Lens edge of each pair side-on to camera, then he wears the small one", "A ❌ · B ✅"),
                   ("Face to camera, small frame on", "CTA text")],
             important=("Check:", "the \"8 out of 10\" must match the shop's own consultations. If they can't stand "
                        f"behind it, say «{ar('أغلب')}» (most) instead."),
             before=before("−8 · A / B"), after=after(40)),
        dict(n=6, title="Reel 6 · Conversation: 3 questions about thick lenses", tag="Conversation",
             color="teal", cta="save",
             sub="Know phase · 45 s · Saad asks 3 questions off camera, each one an ICP fear (paid too much, thick "
                 "lens, lens that shows). Proof kept from the indices reel (edge-to-camera, 183K / 67K)",
             cards=["45 s", "1.5 · 1.67 · 1.74", "3 lenses with the same prescription", "Save"],
             voice_header="Who talks · voice (darija + fr)",
             rows=[("Saad holds the phone and asks off camera; optician faces the lens, 3 lenses fanned in hand",
                    "Q1 caption + badge"),
                   ("1.5 lens edge close to the camera, then the 1.67", "1.5 · 1.67"),
                   ("Saad's question, then the 1.74 edge to camera next to a small frame", "Q2 · 1.74"),
                   ("Saad's question, then the 3 lenses side by side, thickest to thinnest", "Q3"),
                   ("Face to camera, the 3 lenses in hand", "CTA text")],
             important=("How to shoot:", "Saad holds the phone at chest height and asks for real, like a chat at the "
                        "counter; the optician wears the lav. Each question goes on screen as a caption. Don't script "
                        "the answers word for word. The three questions are the ICP's three fears: paid too much, a "
                        "thick heavy lens, a lens that shows."),
             before=["3 lenses in hand and in frame before the first question",
                     "Saad starts recording and asks question 1 before 0.7 s",
                     "Badge \"1.5 · 1.67 · 1.74\" top left, in the first frame"],
             after=["Each of Saad's questions captioned on screen (Q1, Q2, Q3)",
                    "No pause longer than 1.5 s (cut it); length close to 45 s",
                    "Darija captions on, 7 words or fewer per line"]),
        dict(n=7, title="Reel 7 · Kids: 4 signs", color="navy", cta="story",
             sub="Like phase · 45 s · Pattern: Benjelloun \"Les enfants toujours l'organique\" (13K, the topic reaches "
                 "less) + Gzenaya's parent-led ads · Hook: warning",
             cards=["45 s", "4 – 12 ans", "A small flexible kids' frame with organic lenses", "Tell your story"],
             rows=[("Kids' frame raised to the lens", "Badge 4 – 12 ans"),
                   ("Counts on his fingers, frame still in hand", "1 · 2 · 3 · 4"),
                   ("Face to camera", "\"Ophtalmologue d'abord\""),
                   ("Bends the flexible temple, then holds the organic lens to the camera", "Toujours l'organique"),
                   ("Face to camera", "CTA text")],
             before=before("4 – 12 ans"), after=after(45)),
        dict(n=8, title="Reel 8 · Blind test: which frame is the expensive one?", color="navy", cta="series",
             sub="Like phase · 40 s · Pattern: Benjelloun object-in-hand single take, applied to Gzenaya's range · "
                 "Hook: secret question",
             cards=["40 s", "A · B · C", "3 frames, letters A/B/C", "Follow for the series"],
             rows=[("Three frames fanned in hand toward the camera", "Badge A · B · C"),
                   ("Frame A: hinge close to the camera", "A"),
                   ("Frame B: acetate edge to camera", "B"),
                   ("Frame C in the palm (weight), then reveal", "B ✅"),
                   ("Face to camera, B on", "CTA text")],
             before=before("A · B · C"), after=after(40)),
    ]

    p1 = banner("Benjelloun Vision: why his reels go viral",
                "Gzenaya Optique Tanger · Reel playbook v3 (internal) · Oct 2026 · 34 reels analysed (views seen 30 Sept 2026)")
    p1 += ('<div class="stats">'
           '<div class="stat"><div class="lab">REELS ANALYSED</div><div class="big">34</div><div class="s">Median 21K views</div></div>'
           '<div class="stat t"><div class="lab">VIRAL (≥ 50K)</div><div class="big">8</div><div class="s">53K to 213K, 2.5× to 10× his median</div></div>'
           '<div class="stat o"><div class="lab">TRANSCRIBED</div><div class="big">6 / 8</div><div class="s">2 viral reels have no voice in the file Instagram serves</div></div>'
           "</div>")
    p1 += '<h2>The 7 rules</h2><table class="rules big">'
    rules = [
        ("Talk before 0.7 s", "In all 6 viral reels with a voice track, the first word lands between 0.54 and 0.84 s. "
         "No salam, no name, no \"today I will show you\"."),
        ("Open with a hook line or the real numbers",
         f"His viral openers: \"{ar('شوف، يلا كنتي غادير…')}\", reading a real prescription aloud (\"{ar('هادي ناقصة عشرة…')}\"), "
         f"or \"{ar('الناس اللي عندهم…')}\". Ours drop \"{ar('شوف')}\" for a secret, a number or a warning (v3 below)."),
        ("Name the costly mistake in the first 5 s",
         f"213K: \"{ar('غاطيح فلوسك، دير زاج غالي ويجيك الزاج غليظ')}\". 139K: \"{ar('تقدر دير أغلى زاج وما تشوفش مزيان')}\". "
         "The fear is losing money at the shop."),
        ("The product is in his hand from frame 1", "A frame, a lens or a prescription is in shot from the first "
         "frame in 6 of the 8 viral reels, but only 2 of the bottom 10. He pushes it toward the lens."),
        ("One hard number the viewer can check", "\"45 à 49 maximum\", \"+3.00\", \"-10 et plus, oublie le noir\", "
         "\"47\". The viewer checks it against their own prescription or frame."),
        ("Prove it on camera", "Lens edge turned to the camera to show thickness, a real prescription photo with a "
         "green circle, then the glasses on the face (often with the sun clip)."),
        ("One take, selfie, in the shop", "Handheld, slightly low angle, shelves of frames behind. 2.2 to 2.9 words "
         "per second, no pause longer than 1.6 s. Viral length 31 to 59 s, median 41 s."),
    ]
    for i, (t, d) in enumerate(rules, 1):
        p1 += f'<tr><td class="n">{i}</td><td class="t">{t}</td><td class="d">{d}</td></tr>'
    p1 += "</table><h2>Why it works on our ICP</h2>" + ul([
        "Our buyers (people with strong corrections, first-time progressive buyers aged 40–55, parents) are about to "
        "spend money at an optician. His openers name what they fear: paying for an expensive lens that comes out "
        "thick, heavy, or that they can't see well with.",
        "The hard number turns the reel into a self-check: the viewer looks at their own prescription or frame "
        "(\"I'm −10, so no black frame\"). That is the \"this is about me\" moment of the Know phase, and it drives "
        "comments with numbers.",
        "The proof is physical and filmed in his own shop: a real lens, a real prescription, the result on a face. "
        "That builds the trust of the Like phase without any selling. He never asks for a sale on camera.",
    ])
    p1 += "<h2>v3: new hooks, #6 becomes a conversation</h2>" + ul([
        f"<b>Hooks.</b> \"{ar('شوف')}\" no longer opens our reels. #1, #2, #8 open with a secret question "
        f"(\"{ar(HOOK_SECRET)}\"), #5 with a number (\"{ar('8 من 10 ديال les consultations ديال moins dix، moins quatorze، moins dix-huit…')}\"), "
        f"#3 and #7 with a warning (\"{ar(HOOK_WARN)}\"). The question must promise the payoff: a bare "
        f"\"{ar('واش خبارك أن…')}\" FAQ still sits at 9K–22K.",
        f"<b>#4 stays a comment reply</b> (\"{ar('واش les progressifs كيدوّخو؟')}\"). Unchanged. Like phase; feeds \"Ask him a question\".",
        "<b>#6 becomes a conversation</b> (was the DM read-out). Saad asks 3 questions off camera, each one an ICP "
        "fear: \"I paid 2500 DH and the lenses are thick, did I get scammed?\", \"I'm −10, will the lens look big or "
        "bulge?\", \"They told me I need 1.74, is that true?\". The optician answers on camera with the 3 lenses in "
        "hand. No fake DM needed.",
    ])

    p2 = '<h1 class="plain">Same topic, opposite results</h1><p class="lead">The topic does not make the reel go ' \
         "viral. The opener, the object and the shot do.</p>"
    p2 += std_table(["Topic", "Win", "What the winner did", "Flop", "What the flop did"], [
        [("b", "Frame choice for strong corrections"), '<span class="win">213K</span>',
         f"Frame in hand at 0 s. \"{ar('شوف… غاطيح فلوسك')}\". Lens diagram, then the frame size engraved on the "
         "temple circled in green: \"45–49 maximum\".", '<span class="flop">38K / 13K</span>',
         "38K: pen in hand, close-up inserts. 13K: talking hands, then a screen recording of the edging software."],
        [("b", "Progressive lenses"), '<span class="win">139K</span>',
         f"Frame in hand, \"Progressif\" badge. \"{ar('شوف، يلا كنتي غادير… ركز معايا')}\". Rule: the eye must sit "
         "above the frame's middle line.", '<span class="flop">9K</span>',
         f"Pen only, nothing physical. Opener \"{ar('واش خبارك أن كاين أحسن وقت…')}\" sounds like a FAQ."],
        [("b", "Mineral vs organic lens"), '<span class="win">183K</span>',
         "Reads the −10 prescription aloud while holding the lens. Prescription photo, lens edge, try-on with sun clip.",
         '<span class="flop">33K</span>', "Wide tripod shot across the desk, face small in the frame, badge only."],
    ], widths=["135px", "55px", None, "70px", "175px"])
    p2 += (f'<p class="lead" style="margin-top:6px">Openers at the bottom of his feed: "{ar("واش خبارك أن…")}" (22K, 9K), '
           f'"{ar("أهلا بيكم")}" (13K). "{ar("شوف")}" alone is not enough (it also opens two 16–19K reels): it works '
           "with the object in hand, the costly mistake and the number.</p>")
    p2 += '<h2 class="red">Never do (none of these passed 35K)</h2>' + ul([
        "Wide tripod shot from across the desk (best result: 33K)", "Screen recording of software (13K–21K)",
        "Hands only, no face (14K)", "Abstract topic with no object to show (pen only: 9K–11K)",
        "Opening with a question that sounds like a FAQ, a greeting or \"today\"",
    ])
    p2 += "<h2>Anatomy of a reel (40–45 s)</h2>" + steps([
        ("navy", "HOOK", "0–5 s", "Hook line (secret, number or warning) + object in shot. First word ≤ 0.7 s"),
        ("red", "THE MISTAKE", "5–10 s", "What it costs: money, a thick lens, not seeing well"),
        ("teal", "RULE + NUMBER", "10–22 s", "One number to check. Prescription overlay, green circle"),
        ("orange", "PROOF", "22–36 s", "Lens edge to camera, then the glasses on the face"),
        ("slate", "CTA", "36–42 s", "One line from the CTA bank"),
    ])
    p2 += ('<div class="kit"><div class="lab">Filming kit</div>iPhone held at chest height, slightly low angle, 9:16 · '
           "Shot in the shop with the frame shelves behind · One take. Cut only to remove pauses · Lav mic · Badge in "
           "a white rounded box, top left, carrying the key number · Prescription photos with the patient's name "
           "hidden and a green circle on the number · Darija captions, 7 words or fewer (darija-transcribe → SRT) · "
           f"Optician, never doctor: anything that sounds like a symptom → \"{ar('شوف')} l'ophtalmologue\".</div>")

    p3 = '<h1 class="plain">CTA bank</h1><p class="lead">Each reel ends with one line from this bank. Never two. ' \
         "Say it in one breath, while still holding the object.</p>"
    hdr = ["CTA", "Line (darija)", "Why it fits"]
    wd = ["140px", "300px", None]
    p3 += '<h2><span class="ph">Know phase</span> <em>"this is about me"</em></h2>'
    p3 += std_table(hdr, [
        [("b", "Comment your number"), ("i", CTA["number"]), "Qualifies the viewer and lifts reach. The self-test and "
         "guess-the-correction formats got the most comments in our data (2.1 per 1,000 views)"],
        [("b", "Comment your test result"), ("i", CTA["test"]), "The viewer just did the test, so answering costs him nothing"],
        [("b", "Save"), ("i", CTA["save"]), "Fits education videos. Saves predict buying intent"],
        [("b", "Send it to someone"), ("i", CTA["send"]), "The 40–55 buyer is often sent the video by a son or daughter"],
    ], cls="std teal", widths=wd)
    p3 += '<h2>Like phase <em>"I trust this guy"</em></h2>'
    p3 += std_table(hdr, [
        [("b", "Follow for the series"), ("i", CTA["series"]), "A promise of the next episode. YourVision's series "
         "episode drew 246 comments"],
        [("b", "Ask him a question"), ("i", CTA["ask"]), "Every answer becomes a new video, and the asker feels heard"],
        [("b", "Tell your story"), ("i", CTA["story"]), "Personal comments build familiarity"],
        [("b", "Soft DM keyword"), ("i", CTA["dm"]), "A free checklist, not an offer. It opens a DM thread and "
         "creates a GHL contact without selling"],
    ], widths=wd)
    p3 += "<h2>Which CTA goes on which reel</h2>"
    K, Lk = ("ph-k", "Know"), ("ph-l", "Like")
    p3 += std_table(["#", "Reel", "Phase", "CTA"], [
        [("b", "1"), ("i", "Guess the correction"), K, "Comment your number"],
        [("b", "2"), ("i", "Astigmatism self-test"), K, "Comment your test result"],
        [("b", "3"), ("i", "Read your prescription in 30 seconds"), K, "Send it to someone"],
        [("b", "4"), ("i", "Comment reply: \"Do progressives make you dizzy?\""), Lk, "Ask him a question"],
        [("b", "5"), ("i", "Same correction, 2 frames"), K, "Comment your number"],
        [("b", "6"), ("i", "Conversation: 3 fear questions, Saad off camera"), K, "Save"],
        [("b", "7"), ("i", "Kids: 4 signs"), Lk, "Tell your story"],
        [("b", "8"), ("i", "Blind test: which frame is the expensive one?"), Lk, "Follow for the series"],
    ], widths=["40px", None, "85px", "220px"])

    pl = '<h1 class="plain">Release order and shop checklist</h1>'
    pl += std_table(["Week", "Reels", "Why this order"], [
        [("b", "1"), ("i", "#5 Two frames · #1 Guess the correction"), "Closest to his 213K and 183K reels. They set "
         "the account's average and pull in \"comment your number\"."],
        [("b", "2"), ("i", "#4 Comment reply · #2 Self-test"), "#4 needs a real comment: by week 2, week 1's reels "
         "have brought some in. The self-test drew the most comments in our data."],
        [("b", "3"), ("i", "#3 Prescription · #6 Conversation"), "Saves and shares. #6 answers the money and "
         "thickness fears head-on, with Saad asking off camera."],
        [("b", "4"), ("i", "#7 Kids · #8 Blind test"), "Like phase: familiarity and the series. Kids reaches less on "
         "his account (13K), but it matches Gzenaya's parent-led ads."],
    ], widths=["65px", "235px", None])
    pl += "<h2>Confirm with the shop before filming</h2>" + ul([
        "Real strong-correction cases (−8, −13) with the client's written consent to show the prescription (name hidden)",
        "The lens indices actually stocked (1.5 / 1.6 / 1.67 / 1.74) and the frame sizes for #5",
        "The real frames and prices for the blind test (#8)",
        "Real comments for #4 (screenshots with names hidden)",
        f"The \"8 out of 10\" line in #5 matches their own consultations; if not, the optician says \"{ar('أغلب')}\" (most)",
        "Saad on set for #6, holding the phone and asking the 3 questions off camera",
        "Who appears on camera: the same optician on every reel, so the Like phase builds trust in one face",
    ])
    pl += ('<p class="method">Method: 34 Benjelloun Vision reels (33 Instagram, 1 TikTok), views as seen on 30 Sept '
           "2026. Voice transcribed locally with darija-transcribe (MoulSot v0.3 + MMS word alignment): 6 viral reels "
           "in full, the rest on their opening 12 s (6 of those files had no audio). Every reel coded frame by frame "
           "for shot, object, badge and overlays. \"🤝\" (83K) and \"L'ophtalmo le matin\" (78K) have no voice in the "
           "downloadable file, so they were coded on the image only. The client edition of this playbook (French) "
           "leaves out every other optician's name.</p>")

    pages = [p1, p2, p3] + [reel_page(r, L) for r in reels] + [pl]
    return doc("Gzenaya · Reel playbook (internal)", "en", pages)


if __name__ == "__main__":
    for name, fn in (("client.html", client), ("interne.html", internal)):
        with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
            f.write(fn())
        print("wrote", name)
