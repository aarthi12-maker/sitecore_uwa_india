# UWA India — Scholarships screen

Run `npm start` and open http://127.0.0.1:3000. The Scholarships screen is available at `index.html` and `scholarships.html`. The previous screens remain at `how-to-apply.html` and `home.html`.

The scholarship layout and copy follow the supplied screenshot. Pages 7–8 of the supplied content PDF request that existing scholarship content be carried over. Shared branding follows UWA Brand Guidelines v1.1 (pp. 53–54, 60–68): Vivid Blue, UWA Blue, Melun Display and TT Norms Pro, with the logo proportions preserved. The card uses the approved neutral `#F2EFEC`.

The exact two reference photos have not yet been located; current photos are official UWA assets and can be replaced without changing the layout.

Page-specific styles are in `assets/css/scholarships.css`; shared header and footer styles are in `assets/css/how-to-apply.css`. Fonts and images are served locally. The previous application screen retains its FAQ dialog and application links.

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
  screenshot. Fonts are Google stand-ins (Kumbh Sans, Kanit).
- **Images & logo** — low-res crops from the screenshot; swap for originals
  (same filenames).
- **Why Choose cards 3 & 4** — copy was cut off in the design; placeholder text.
- **Form data** — programs, courses and intakes in `form-data.js` are samples.
- **Captcha & submit** — client-side demo only; wire to Sitecore Forms /
  reCAPTCHA and the CRM endpoint (`TODO(sitecore)` in `main.js`).
- **Desktop layout** — extrapolated; the design supplied is mobile only.
