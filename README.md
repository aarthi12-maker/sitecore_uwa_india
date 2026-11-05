# UWA India — Homepage (front-end build)

Static HTML/CSS/JS build of the UWA India homepage, matched to the approved
mobile design. Open `index.html` in a browser — no build step needed.

```
index.html               homepage markup
assets/css/tokens.css    ALL colours, fonts, sizes  ← update from brand guidelines
assets/css/main.css      component styles (mobile-first, desktop ≥768px)
assets/js/main.js        menu, search, carousel, country switcher, form logic
assets/js/form-data.js   form dropdown data (states, campuses, courses, intakes)
assets/images/           images (currently cropped from the design screenshot)
```

## Sitecore rendering map

Each section has a `data-rendering` attribute naming the Sitecore rendering it
should become when converted to XM Cloud / JSS components:

| Rendering         | Section                                   | Datasource fields |
|-------------------|-------------------------------------------|-------------------|
| `Header`          | Logo, menu, search, page title            | Logo, Nav links |
| `HeroBanner`      | Hero image + chevron panel                | Image, Title, Text, CTA 1, CTA 2 |
| `FeatureCarousel` | Why Choose UWA India?                     | Title, child Feature items (Title, Text) |
| `TextWithImage`   | Build a career                            | Title, Bullet list, CTA, Image |
| `CourseSearch`    | Find your course                          | Label, Placeholder, Link |
| `CampusCards`     | Our Campuses                              | Title, Intro, child Campus items (Image, Title, Text, Link) |
| `QuickLinks`      | 4 arrow links                             | Link list |
| `JourneySteps`    | Your Journey with UWA India               | Title, Steps, CTA |
| `PromoCard`       | Join a globally recognised university     | Image, Title, Bullets, CTA |
| `CtaBanner`       | Need help choosing your path?             | Title, Text, CTA |
| `LinkCards`       | Ready to start your journey?              | Title, Link list |
| `EnquiryForm`     | Register your interest                    | → Sitecore Forms / CRM |
| `Footer`          | Address, contacts, links, country switch  | Footer settings item |

## Still to replace before go-live

- **Brand tokens** — colours/fonts in `tokens.css` were sampled from the
  screenshot. Fonts are Google stand-ins (Outfit, Archivo).
- **Images & logo** — low-res crops from the screenshot; swap for originals
  (same filenames).
- **Why Choose cards 3 & 4** — copy was cut off in the design; placeholder text.
- **Form data** — programs, courses and intakes in `form-data.js` are samples.
- **Captcha & submit** — client-side demo only; wire to Sitecore Forms /
  reCAPTCHA and the CRM endpoint (`TODO(sitecore)` in `main.js`).
- **Desktop layout** — extrapolated; the design supplied is mobile only.
