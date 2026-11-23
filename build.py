# -*- coding: utf-8 -*-
"""
Builds the portfolio from data.py + templates/page.html into dist/.

    python build.py

Standard library only - no pip install needed.
"""

from datetime import date
from pathlib import Path
import shutil

import data

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "templates" / "page.html"
DIST = ROOT / "dist"


def skill_card(skill):
    return f"""
      <article class="skill">
        <img class="skill__icon" src="{skill['icon']}" alt="" loading="lazy" width="34" height="34">
        <h3 class="skill__name">{skill['name']}</h3>
        <p class="skill__note">{skill['note']}</p>
      </article>"""


def cert_card(cert, index):
    wide = " cert--wide" if cert.get("wide") else ""
    return f"""
      <article class="cert{wide}">
        <button class="cert__frame" data-cert="{index}" aria-label="View {cert['title']}">
          <img class="cert__img" src="{cert['image']}" alt="{cert['title']}" loading="lazy">
          <span class="cert__hover">view</span>
        </button>
        <div class="cert__meta">
          <h3 class="cert__title">{cert['title']}</h3>
          <p class="cert__sub">{cert['issuer']} <span class="dot">.</span> {cert['date']}</p>
        </div>
      </article>"""


def lightbox_panel(cert, index):
    return f"""
      <figure class="lightbox__panel" data-panel="{index}" hidden>
        <img src="{cert['image']}" alt="{cert['title']}">
        <figcaption>{cert['title']} <span class="dot">.</span> {cert['issuer']} <span class="dot">.</span> {cert['date']}</figcaption>
      </figure>"""


def meta_row(key, value):
    return f"""
        <div class="meta__row">
          <dt>{key}</dt>
          <dd>{value}</dd>
        </div>"""


def contact_row(number, label, value, href=None, external=False):
    # no href -> plain row, no link and no arrow
    if href is None:
        return f"""
      <div class="link-row link-row--static">
        <span class="link-row__num">{number}</span>
        <span class="link-row__label">{label}</span>
        <span class="link-row__value">{value}</span>
      </div>"""
    target = ' target="_blank" rel="noreferrer"' if external else ""
    return f"""
      <a class="link-row" href="{href}"{target}>
        <span class="link-row__num">{number}</span>
        <span class="link-row__label">{label}</span>
        <span class="link-row__value">{value}</span>
        <span class="link-row__arrow" aria-hidden="true">&rarr;</span>
      </a>"""


def build():
    if not TEMPLATE.exists():
        raise SystemExit(f"Missing template: {TEMPLATE}")

    html = TEMPLATE.read_text(encoding="utf-8")

    tokens = {
        "name": data.NAME,
        "initials": data.INITIALS,
        "role": data.ROLE,
        "tagline": data.TAGLINE,
        "hero_tag": data.HERO_TAG,
        "hero_year": data.HERO_YEAR,
        "portrait": data.PORTRAIT,
        "portrait_caption": data.PORTRAIT_CAPTION,
        "about_1": data.ABOUT_1,
        "about_2": data.ABOUT_2,
        "email": data.EMAIL,
        "phone": data.PHONE,
        "year": str(date.today().year),
        "skills": "".join(skill_card(s) for s in data.SKILLS),
        "certs": "".join(cert_card(c, i) for i, c in enumerate(data.CERTIFICATES)),
        "lightbox_panels": "".join(lightbox_panel(c, i) for i, c in enumerate(data.CERTIFICATES)),
        "meta": "".join(meta_row(k, v) for k, v in data.META),
        "contacts": "".join([
            contact_row("01", "Email", data.EMAIL, f"mailto:{data.EMAIL}", False),
            contact_row("02", "Phone", data.PHONE),
            contact_row("03", "Facebook", data.FACEBOOK_LABEL),
            contact_row("04", "LinkedIn", data.LINKEDIN_LABEL, data.LINKEDIN, True),
        ]),
    }

    for key, value in tokens.items():
        html = html.replace("{{" + key + "}}", value)

    leftovers = [part.split("}}")[0] for part in html.split("{{")[1:]]
    if leftovers:
        raise SystemExit("Unfilled tokens in template: " + ", ".join(leftovers))

    DIST.mkdir(exist_ok=True)
    if (DIST / "assets").exists():
        shutil.rmtree(DIST / "assets")
    shutil.copytree(ROOT / "assets", DIST / "assets")
    (DIST / "index.html").write_text(html, encoding="utf-8")

    print(f"Built {DIST / 'index.html'}")
    print("Next: run 'python serve.py' and open http://localhost:8000")


if __name__ == "__main__":
    build()
