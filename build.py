#!/usr/bin/env python3
"""Assembles the static site from the templates below into plain .html files.
No framework, no Node: this is the brief's 'plain HTML/CSS with a light build
step' option, run with the stdlib-only python3 already on this machine.
Re-run after any change in this file: `python3 build.py`.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
HAND_DIR = ROOT / "assets" / "handwriting"
SITE_URL = "https://daniecheverria.com"
EMAIL = "daniecheverriam@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/daniecheverria/"
RESUME = "assets/resume/dani-echeverria-resume.pdf"


def handwriting(word, css_class):
    """Inline one of the traced-handwriting SVGs, colored via CSS (currentColor),
    with a visually-hidden text twin so screen readers and search engines get
    the real word rather than a graphic."""
    svg = (HAND_DIR / f"{word}.svg").read_text()
    svg = re.sub(r'^<svg ', f'<svg class="ink {css_class}" aria-hidden="true" ', svg, count=1)
    svg = re.sub(r'\s*role="img"\s*aria-label="[^"]*"', '', svg, count=1)
    return f'<span class="ink-wrap"><span class="sr-only">{word}</span>{svg}</span>'


LOOP_SVG = '''<svg class="loop" viewBox="0 0 240 100" aria-hidden="true">
            <path d="M14,58 C10,22 88,6 152,12 C216,18 236,44 224,66 C210,92 118,98 62,88 C20,80 8,64 26,44"/>
          </svg>'''

CHECK_BADGE = '''<div class="check-badge" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 12.5 L10 18 L20 6"/></svg></div>'''

TODO = '<span class="todo-flag">[TODO: {}]</span>'


def head(title, description, canonical, og_image="assets/og-image.png"):
    prefix = "" if canonical == "" else canonical
    url = f"{SITE_URL}/{prefix}"
    return f'''<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta name="theme-color" content="#ECE8DE">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE_URL}/{og_image}">
<link rel="stylesheet" href="assets/css/fonts.css">
<link rel="stylesheet" href="assets/css/style.css">'''


def header_nav(home):
    p = "" if home else "index.html"
    logo_href = "#top" if home else "index.html"
    return f'''<header>
  <div class="wrap">
    <nav>
      <a class="logo" href="{logo_href}">Dani Echeverria<span>.</span></a>
      <ul class="nav-links">
        <li><a href="{p}#work">Work</a></li>
        <li class="hide-m"><a href="{p}#leadership">Leadership</a></li>
        <li class="hide-m"><a href="{p}#about">About</a></li>
        <li><a href="{p}#contact">Contact</a></li>
      </ul>
    </nav>
  </div>
</header>'''


FOOTER = '''<footer>
  <div class="wrap">
    <span class="mono">&copy; 2026 Dani Echeverria</span>
    <span class="mono">Every pixel here was reviewed by a human. Several times.</span>
  </div>
</footer>'''

SCRIPT_TAG = '<script src="assets/js/main.js"></script>'


def page(title, description, canonical, body, og_image="assets/og-image.png"):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
{head(title, description, canonical, og_image)}
</head>
<body>
{body}
{SCRIPT_TAG}
</body>
</html>
'''


# ---------------------------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------------------------

CASES = [
    dict(
        slug="case-populations-and-samples.html",
        tag="Audit workflow &middot; AI + automation",
        title="The twelve hours that happened outside the product",
        summary="Populations and samples run on every single audit, and the process took 12+ hours of manual work each time. Most of it happened in spreadsheets, handled by a separate ops team, outside the product entirely. I redesigned it so it lives inside the platform from start to finish.",
        impact="100% of audits &middot; a manual 12+ hour process, now automated &middot; the external ops team out of the loop entirely",
        impact_todo=None,
        card_media=f'<img src="assets/diagrams/audit-workflow-before-after.svg" alt="Abstracted before and after diagram of the population and sample workflow moving out of spreadsheets and into the product.">',
    ),
    dict(
        slug="case-ai-governance.html",
        tag="Leadership &middot; AI patterns",
        title="Teaching a company to build AI it can defend",
        summary="Teams started shipping AI features with no shared idea of what good looked like, inside a product whose entire value is that customers trust it. I wrote the patterns. Traceability by default, human review, graceful failure. Then I did the harder part, which was getting anyone to use them.",
        impact="Gave a company shipping AI fast a shared definition of what responsible looks like, starting with traceability by default. Presented company-wide, workshopped with a team of five designers.",
        impact_todo=None,
        card_media='<img src="assets/images/ai-principle-1-traceability.webp" alt="Slide describing Principle 1, Traceability by Default: log every AI action and decision, show what was done and when and why, and enable internal review, audits, and recovery.">',
    ),
    dict(
        slug="case-field-service.html",
        tag="Field service &middot; IoT &middot; Hardware + firmware",
        title="The screens were the easy part",
        summary="An installation app for technicians working with IoT hardware. The brief was a few clean screens. What I found on site was different: no connectivity where the work happens, failures arriving from three places at once, and three engineering teams who each assumed the others had it covered. The real project was uncovering that, then designing around it.",
        impact="The app is what let the hardware product ship. No app, no launch. The initial engagement led to a second one.",
        impact_todo=None,
        card_media='<img src="assets/diagrams/field-service-blueprint.png" alt="Swimlane blueprint mapping every interaction across the user flow, backend admin app, backend to hardware platform, and firmware and hardware layers.">',
    ),
    dict(
        slug="case-cuida.html",
        tag="Concept &middot; AI-native &middot; Consumer",
        title="Cuída: making invisible work visible",
        summary="The mental load of running a household is real work, and nobody can see it. I designed an AI-native concept where tasks get carried by small creatures you can hand to someone else, so you can actually watch your load get lighter.",
        impact="Proof the enterprise rigour holds up on a warm, human problem.",
        impact_todo=None,
        card_media='<img src="assets/images/cuida-app-screens.avif" alt="Screenshots of the Cuida app: a load board showing tasks carried by small colour-coded blob characters split between household members.">',
    ),
]


def case_card(c):
    todo = f'<br>{TODO.format(c["impact_todo"])}' if c["impact_todo"] else ""
    return f'''      <article class="case reveal">
        <div class="case-content">
          <span class="mono case-tag">{c["tag"]}</span>
          <h3>{c["title"]}</h3>
          <p>{c["summary"]}</p>
          <p class="impact">{c["impact"]}{todo}</p>
          <a class="case-link" href="{c["slug"]}">Read the case study <span class="arrow" aria-hidden="true">&rarr;</span></a>
        </div>
        <div class="case-media">
          {c["card_media"]}
          {CHECK_BADGE}
        </div>
      </article>'''


def build_home():
    cover = f'''  <section class="cover" id="top">
  <div class="wrap cover-in">
    <div class="cover-top">
      <span class="cover-name">Dani Echeverria<span class="dot">.</span></span>
      <span class="mono">Product design leader &middot; Enterprise SaaS &amp; AI</span>
    </div>
    <h1>Product visions built with
        <span class="loop-word">{handwriting("humans", "ink-humans")}
          {LOOP_SVG}
        </span>
        in the loop.</h1>
  </div>
  </section>'''

    intro = f'''<section class="intro">
  <div class="wrap">
    <p class="lede">I've spent 10+ years designing inside complicated, high-stakes products. Right now that means AI-powered compliance and audit. What I actually do is work out what design should {handwriting("solve", "ink-solve")} before we start designing, then build the shortest honest path through it. With AI that path usually isn't a faster version of the old process, it's a different process, and knowing the difference is most of the job now. I also manage designers, which turned out to be the part I like most.</p>
    <div class="cta-row">
        <a class="btn primary" href="#work">See the work <span aria-hidden="true">&darr;</span></a>
        <a class="btn ghost" href="{RESUME}">Download resume</a>
      </div>
    <p class="aside">Currently leading design for an AI-powered compliance and audit platform. Before that: IoT consultancy.</p>
  </div>
</section>'''

    strip_words = ["AI-native workflows", "Compliance &amp; audit", "Design leadership", "0&rarr;1 product vision", "Human-in-the-loop UX", "Enterprise SaaS", "Team coaching", "Design systems"]
    strip_spans = "".join(f"<span>{w}</span>" for w in strip_words * 2)
    strip = f'''<div class="strip" aria-hidden="true">
    <div class="strip-inner" id="strip">
      {strip_spans}
    </div>
  </div>'''

    work = f'''<section id="work">
    <div class="wrap">
      <div class="sec-head reveal">
        <h2>Selected work</h2>
        <span class="mono">Outcomes first</span>
      </div>
{chr(10).join(case_card(c) for c in CASES)}

      <div class="sec-head reveal" style="margin-top:96px">
        <h2 style="font-size:clamp(24px,2.6vw,32px)">More work</h2>
        <span class="mono">Happy to talk through any of them</span>
      </div>
      <div class="more-grid reveal">
        <div class="more-card"><span class="mono">Insurance &middot; AI</span><h4>Insurance AI platform</h4><p>Research, workshops, and UI for an AI underwriting platform, three weeks from discovery to concept. The heart of it was a conversational assistant for insurance professionals: generate leads, review policies, ask anything, all in plain language.</p></div>
        <div class="more-card"><span class="mono">Enterprise &middot; Strategy</span><h4>Enterprise compliance strategy</h4><p>Strategy work for serving the platform's biggest clients. I mapped where enterprise-scale audits strain the current workflows and tooling, and helped align product and leadership on where the platform has to flex. Less about screens, more about deciding what gets built.</p></div>
        <div class="more-card"><span class="mono">HR &middot; Payments</span><h4>Global payment platform</h4><p>UX, UI, and a design system for a global HR and payments web app. Enterprise scale, lots of flows, and a system built so the basics stayed consistent everywhere.</p></div>
      </div>
    </div>
  </section>'''

    leadership = f'''<section id="leadership" style="padding-top:0">
    <div class="wrap">
      <div class="sec-head reveal">
        <h2>How I lead</h2>
        <span class="mono">Method over process</span>
      </div>
      <div class="lead-grid reveal">
        <div class="lead-item"><span class="mono">01 &middot; Foundation</span><h4>Problems, then screens</h4><p>I don't start with what to design. I start with what design should {handwriting("solve", "ink-solve-sm")}. The business outcome, and the person stuck in the process. Then I go and make screens that look good and work properly. Both halves are the job.</p></div>
        <div class="lead-item"><span class="mono">02 &middot; Process</span><h4>Evidence over opinion</h4><p>I go where the work happens and watch someone do it. Opinions are cheap and everybody has one, me included. A decision should be able to point at something a real user did.</p></div>
        <div class="lead-item"><span class="mono">03 &middot; AI</span><h4>AI, both directions</h4><p>I design <em>for</em> AI: what a person needs to trust a system that's sometimes wrong, when to show the reasoning, where a human takes the wheel. And I design <em>with</em> it, using AI to move fast without automating a broken process by accident.</p></div>
        <div class="lead-item"><span class="mono">04 &middot; Craft</span><h4>Teams that raise the bar</h4><p>I coach designers on craft and on AI-native thinking. The aim is that quality stops depending on me being in the room.</p></div>
      </div>
    </div>
  </section>'''

    about = f'''<section id="about">
    <div class="wrap">
      <div class="sec-head reveal">
        <h2>About</h2>
        <span class="mono">How I actually work</span>
      </div>
      <div class="about-grid reveal">
        <div>
          <p><strong>My process holds up in any complex environment.</strong> I go and find whoever is stuck in the work, and I watch them do it. Then I map the system they're fighting rather than the screens they happen to be looking at. Somewhere in there is one decision that everything else hangs off. That's the one I design first.</p>
          <p>Compliance is a genuinely complex place to work. The rules are tangled, the consequences are real, and the people using the product are personally accountable for whatever it tells them. So trust here doesn't get to be a value on a slide. It's a set of concrete calls. How much does the system explain itself? Where does a human sign off? What does it do when the machine gets it wrong?</p>
          <p>I started in graphic design, and it still shows. I care about type and spacing more than is strictly reasonable. What I'm useful for now is wider than that: I help define what a product should be, I can still do the UI myself, and I've led teams of four to seven, working with leadership to set the metrics and practices design is held to. I manage for two things that pull against each other, what the company needs and what each person on the team needs to grow. I don't think you get the first without taking the second seriously.</p>
          <ul class="facts">
            <li>Based in Chile, working across time zones</li>
            <li>10+ years in product design across insurance, field service, and compliance</li>
            <li>Helped define and establish AI patterns for enterprise products</li>
            <li>Mom to a toddler and a dog</li>
          </ul>
        </div>
        <div class="about-photo">
          <div class="frame"><img src="assets/images/dani-photo.jpg" alt="Portrait of Dani Echeverria outdoors beside a river."></div>
          <p class="about-note">Yes, the loop up top is hand drawn. Some things shouldn't be automated.</p>
        </div>
      </div>
    </div>
  </section>'''

    contact = f'''<section class="contact" id="contact">
    <div class="wrap reveal">
      <span class="mono">Contact</span>
      <h2>Got a problem worth {handwriting("solving", "ink-solving")}?</h2>
      <div class="links">
        <a class="btn primary" href="mailto:{EMAIL}">{EMAIL}</a>
        <a class="btn ghost" href="{LINKEDIN}">LinkedIn</a>
        <a class="btn ghost" href="{RESUME}">Resume</a>
      </div>
    </div>
  </section>'''

    body = f'''<a class="skip" href="#work">Skip to work</a>
<main>
{cover}

{header_nav(home=True)}

{intro}

{strip}

{work}

{leadership}

{about}

{contact}
</main>

{FOOTER}'''

    return page(
        title="Dani Echeverria · Product Design Leader",
        description="Product design leader with 10+ years in complex, high-stakes products. Currently AI-powered compliance and audit. Product visions built with humans in the loop.",
        canonical="",
        body=body,
    )


# ---------------------------------------------------------------------------
# CASE STUDY PAGES
# ---------------------------------------------------------------------------

BREADCRUMB = '<div class="wrap"><p class="breadcrumb"><a href="index.html#work">&larr; Back to work</a></p></div>'


def case_hero(tag, title, impact_html, media_html):
    return f'''<section class="case-hero">
    <div class="wrap">
      <span class="mono case-tag">{tag}</span>
      <h1>{title}</h1>
      <p class="impact">{impact_html}</p>
      <div class="case-hero-media">{media_html}</div>
    </div>
  </section>'''


def figure_img(src, alt, caption):
    return f'''<figure>
        <div class="frame"><img src="{src}" alt="{alt}"></div>
        <figcaption>{caption}</figcaption>
      </figure>'''


def gallery(figures, full=False):
    cls = "case-gallery full" if full else "case-gallery"
    return f'<div class="{cls}">\n      ' + "\n      ".join(figures) + '\n    </div>'


def case_footer_nav(next_slug, next_title):
    return f'''<div class="wrap">
    <div class="case-footer-nav">
      <a class="case-link" href="index.html#work">&larr; Back to work</a>
      <a class="case-link" href="{next_slug}">Next case study: {next_title} <span class="arrow" aria-hidden="true">&rarr;</span></a>
    </div>
  </div>'''


def case_page(title, description, canonical, tag, h1, impact_html, hero_media, body_html, gallery_html, next_slug, next_title):
    body = f'''{header_nav(home=False)}
<main>
{BREADCRUMB}
{case_hero(tag, h1, impact_html, hero_media)}
<section style="padding-top:0">
  <div class="wrap">
    <article class="case-body">
{body_html}
    </article>
    {gallery_html}
  </div>
</section>
<section style="padding-top:0">
{case_footer_nav(next_slug, next_title)}
</section>
</main>

{FOOTER}'''
    return page(title=title, description=description, canonical=canonical, body=body)


def build_case_populations():
    tag = "Audit workflow &middot; AI + automation"
    h1 = "The twelve hours that happened outside the product"
    impact = "100% of audits &middot; a manual 12+ hour process, now automated &middot; the external ops team out of the loop entirely"
    hero_media = '<div class="frame"><img src="assets/diagrams/audit-workflow-before-after.svg" alt="Abstracted diagram comparing the population and sample workflow before and after the redesign, showing the process moving from spreadsheets and a separate ops team into the product."></div>'

    body_html = '''<h2>Problem</h2>
      <p>Every audit needs populations and samples. The auditor requests a population, the customer provides it, a sample is pulled, the sample is tested. Simple in theory.</p>
      <p>In practice: the auditor created a population request, received the full population, made files, and handed them to an ops team. Ops seeded the population, sampled it randomly in a spreadsheet, then uploaded the result back. The source of truth lived outside the product the whole time. Twelve-plus hours per audit, on 100% of audits, mostly manual, held together by a second team whose job was to be human middleware for a spreadsheet.</p>

      <h2>What was actually broken</h2>
      <p>Every user asked for something small. A fix here, a field there, an export. Each request was reasonable. Building them would have meant shipping a dozen patches onto a process that was never going to hold.</p>
      <p>Four groups touched this process: leadership, the customer, the lead auditor, and the tester. Nobody owned the whole thing, so nobody could see the whole thing. That was the actual problem. Not a missing feature, a missing connection. The process had left the product, so nothing could stay true, and keeping it true was somebody's full time job.</p>

      <h2>What I designed</h2>
      <p>The auditor now creates samples directly from the population request. Samples stay connected to their sample requests. The database is the source of truth, so everything stays current without anyone maintaining it. Testing is automated, with AI where judgment helps and deterministic logic where it doesn't.</p>
      <p>The interface had to serve four different people without becoming four different products. Leadership needs to see status. The customer needs to be asked once, clearly. The auditor needs control. The tester needs the work to be already done.</p>

      <h2>The hard part</h2>
      <p>The happy path was never the work. The work was every case that isn't: no population yet, resampling, samples shared across frameworks, functionality that no longer exists. Each has a different shape, and each one, left unhandled, sends the auditor straight back to the spreadsheet.</p>
      <p>The hardest was multi-framework. Two audits running in parallel against different frameworks, drawing on overlapping evidence. The customer should only have to do the work once, because burdening them twice is how you lose their trust. But the auditor shouldn't have to absorb that complexity either, because absorbing it is how you lose the rigour. So the system holds the complexity instead of a person.</p>

      <h2>My role</h2>
      <p>I led the design end to end, in close partnership with the PM. We ran the research together: interviews, sessions with auditors and customers, and a map of how the process actually worked versus how it should. That map is where the project turned. I worked directly with engineering on the technical dependencies, because the fix was structural before it was visual. I designed the flows and the screens, we reviewed as a team, and I stayed on it after ship: user testing, correcting, adjusting as real audits ran through it.</p>

      <h2>What changed</h2>
      <p>Populations and samples now run inside the platform on 100% of audits. The manual work is automated. The ops team is out of the loop entirely. The source of truth is the product, which means it stays true on its own.</p>'''

    gallery_html = gallery([
        figure_img("assets/diagrams/design-exploration-canvas.png",
                   "Design exploration canvas showing early frame level experiments across custom samples, testing tables, and sub population scoping, before landing on the final workflow.",
                   "Design exploration canvas: early frames before the final workflow."),
        figure_img("assets/diagrams/audit-workflow-screen-abstracted.svg",
                   "Abstracted recreation of the resulting screen, showing samples created directly from the population request.",
                   "What it became: an abstracted recreation of the shipped screen."),
    ]) + "\n    " + gallery([
        figure_img("assets/images/sample-record-prototype.png",
                   "Prototype of a sample record review screen, showing the evidence upload flow, sample status, and related requirements panel.",
                   "Prototype of the sample record screen, where evidence gets reviewed and attached."),
    ], full=True)

    return case_page(
        title="Populations and samples · Dani Echeverria",
        description="Redesigning the population and sample workflow that ran a 12+ hour manual process outside the product on 100% of audits.",
        canonical="case-populations-and-samples.html",
        tag=tag, h1=h1, impact_html=impact, hero_media=hero_media,
        body_html=body_html, gallery_html=gallery_html,
        next_slug="case-ai-governance.html", next_title="Teaching a company to build AI it can defend",
    )


def build_case_ai_governance():
    tag = "Leadership &middot; AI patterns"
    h1 = "Teaching a company to build AI it can defend"
    impact = 'Patterns adopted across product teams &middot; shifted the leadership conversation from AI as a feature to AI as a capability. Presented company-wide to leadership, and workshopped directly with a team of five designers.'
    hero_media = '<div class="frame"><img src="assets/images/ai-principle-1-traceability.webp" alt="Slide describing Principle 1, Traceability by Default: log every AI action and decision, show what was done and when and why, and enable internal review, audits, and recovery."></div>'

    body_html = '''<h2>Problem</h2>
      <p>AI landed in the company strategy and teams started building straight away. Each one invented its own answer to the same questions. How much do we tell the user the model is guessing? Who checks it? What do we do when it's wrong?</p>
      <p>In an audit product, those aren't UX questions. If the AI is confidently wrong and nobody can see how it got there, the customer is the one who has to answer for it. We were about to ship a dozen different answers to the same problem inside a product whose entire value is that people trust it.</p>

      <h2>What I wrote</h2>
      <p><strong>Principle 1: Traceability by default.</strong></p>
      <p>Log every AI action and decision, with a description of what happened and why. Not just afterwards. During. If the model is reasoning, the user gets to watch it reason.</p>
      <p>Show what was done, when, and why, in a form somebody can actually scan. Timestamped, summarised, no digging.</p>
      <p>Build for review and recovery, not just for the compliance log. Someone will need to go back through the history, understand a decision, and undo it. Design for that person before they exist.</p>
      <p>The rest of the patterns followed from the same instinct: human review at the points that carry consequences, and failure that degrades gracefully instead of guessing loudly.</p>

      <h2>The harder part</h2>
      <p>Writing patterns is the easy half. A pattern nobody uses is an opinion with a nice layout. So I ran workshops with the design team until the patterns were in their hands rather than in a document. I took it to leadership and argued that AI wasn't a feature we were adding, it was a capability that changed how we build. And I sat with product and engineering peers to get the patterns into real initiatives, because that's the only place they count.</p>

      <h2>What changed</h2>
      <p>Teams now start from a shared foundation instead of inventing one each time. Designers who were nervous about AI work have something to reach for. The leadership conversation moved from which features get AI to what AI changes about how we build.</p>'''

    gallery_html = ""

    return case_page(
        title="Teaching a company to build AI it can defend · Dani Echeverria",
        description="Writing the responsible AI patterns an audit product needed, then getting a design team and its leadership to actually use them.",
        canonical="case-ai-governance.html",
        tag=tag, h1=h1, impact_html=impact, hero_media=hero_media,
        body_html=body_html, gallery_html=gallery_html,
        next_slug="case-field-service.html", next_title="The screens were the easy part",
    )


def build_case_field_service():
    tag = "Field service &middot; IoT &middot; Hardware + firmware"
    h1 = "The screens were the easy part"
    impact = 'The app is what let the hardware product ship. No app, no launch. The initial engagement led to a second one.'
    hero_media = '<div class="frame"><img src="assets/diagrams/field-service-blueprint.png" alt="Swimlane blueprint mapping every interaction across the user flow, backend admin app, backend to hardware platform, and firmware and hardware layers."></div>'

    body_html = f'''<h2>Problem</h2>
      <p>From the outside this is a simple product. A technician installs a piece of hardware, the app confirms it worked. Three screens, maybe four.</p>
      <p>Everything hard about it is invisible. The hardware talks to firmware, the firmware talks to software, and any of them can fail. And the technician is standing inside a building with no connectivity at all, which turns out to change the entire shape of the product.</p>

      <h2>The thing that changed the design</h2>
      <p>There's no signal on site. So the question was never a layout preference. It was: does the technician configure every device first and connect them all later, or do it one at a time? The honest answer is that it depends on the building, and the building doesn't ask us. So the app had to support both, without making the technician think about which mode they were in.</p>

      <h2>Getting three teams to agree</h2>
      <p>Hardware, software, and firmware each understood their own failure modes and quietly assumed the others had theirs covered. Nobody had written down a single list of what can go wrong.</p>
      <p>I built a blueprint of every interaction the product needed, which surfaced the blockers nobody had named, and I got the three teams to align on one shared picture. That blueprint became the design. Every error state, how likely it was, whether the technician could recognise it, and whether they could fix it themselves or had to call for help. The interface stayed simple because the hard thinking happened somewhere else.</p>

      <h2>What shipped</h2>
      <p>The app was the gate on the hardware launch. It shipped, and the product went to market.</p>

      <h2>What user testing changed</h2>
      <p>User testing surfaced something worth designing around: most of the technicians spoke Spanish. That was a good finding, not a problem. It pushed the design to be more picture-driven rather than text-heavy, and it put translation on the roadmap as a priority to add later.</p>'''

    gallery_html = gallery([
        figure_img("assets/images/field-service-card-onboarding.png",
                   "Card onboarding flow documentation showing the Bluetooth card connection screens, the UX goals for the flow, and the troubleshooting states when Bluetooth is off or unavailable.",
                   "Card onboarding flow: connecting to the hardware over Bluetooth, with the recovery paths mapped alongside it."),
    ], full=True)

    return case_page(
        title="The screens were the easy part · Dani Echeverria",
        description="Designing an installation app for IoT hardware technicians working on sites with no connectivity, and getting three engineering teams to agree on what could go wrong.",
        canonical="case-field-service.html",
        tag=tag, h1=h1, impact_html=impact, hero_media=hero_media,
        body_html=body_html, gallery_html=gallery_html,
        next_slug="case-cuida.html", next_title="Cuída: making invisible work visible",
    )


def build_case_cuida():
    tag = "Concept &middot; AI-native &middot; Consumer"
    h1 = "Cuída: making invisible work visible"
    impact = 'Built during a product design course, on a problem I chose myself.'
    hero_media = '<div class="frame"><img src="assets/images/cuida-app-screens.avif" alt="Screenshots of the Cuida app: a load board showing tasks carried by small colour-coded blob characters split between household members, plus insights, settings, and onboarding screens."></div>'

    body_html = '''<h2>Problem</h2>
      <p>Running a household is a job. Remembering the dentist, the shoe sizes, the birthday gift, the vaccine schedule. It's real cognitive work, it's distributed unequally, and it's invisible, which is exactly why it doesn't get shared. Task apps don't fix this. They give you a list, and a list is just the invisible work written down. It doesn't help you hand any of it away.</p>

      <h2>What I designed</h2>
      <p>Cu&iacute;da Load Bounce. Tasks are carried by small colour-coded creatures that bounce around, and they visibly weigh something. You can see your load. You can hand a creature to someone else and watch your load get lighter.</p>
      <p>AI sits underneath as an ambient partner rather than an assistant you talk to. It sorts your brain dump into things that make sense, remembers context so you don't repeat yourself, and suggests what could go to someone else. It never asks you to manage it.</p>
      <p>Underneath the blobs are the same patterns I use in enterprise work: progressive disclosure, contextual memory, warm handoffs. The rigour is identical. The tone is not.</p>

      <h2>Why I made it</h2>
      <p>I built this during Become an AI Product Designer, a course that let me pick my own problem to solve. I chose this one because I'm a mom, this is my actual life, and I wanted to prove to myself that the same thinking I bring to a compliance audit works on a problem that runs on feeling rather than rules.</p>'''

    gallery_html = gallery([
        figure_img("assets/images/cuida-concept-board.webp",
                   "A concept exploration board mapping metaphors for sharing mental load, narrowing down to the final Load Bounce concept and its interaction model.",
                   "Getting to Load Bounce: exploring metaphors before landing on the final concept."),
    ], full=True)

    return case_page(
        title="Cuída: making invisible work visible · Dani Echeverria",
        description="A self-directed AI-native concept for sharing the invisible mental load of running a household.",
        canonical="case-cuida.html",
        tag=tag, h1=h1, impact_html=impact, hero_media=hero_media,
        body_html=body_html, gallery_html=gallery_html,
        next_slug="case-populations-and-samples.html", next_title="The twelve hours that happened outside the product",
    )


def main():
    pages = {
        "index.html": build_home(),
        "case-populations-and-samples.html": build_case_populations(),
        "case-ai-governance.html": build_case_ai_governance(),
        "case-field-service.html": build_case_field_service(),
        "case-cuida.html": build_case_cuida(),
    }
    for name, html in pages.items():
        (ROOT / name).write_text(html)
        print(f"wrote {name} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
