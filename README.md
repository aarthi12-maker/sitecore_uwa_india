# UWA India — Course listing screens

Run `npm start` and open http://127.0.0.1:3000. The latest default screen is Postgraduate courses (`index.html`, also `postgraduate-courses.html`). Undergraduate courses is at `undergraduate-courses.html`. Both are linked in every page’s menu. The prior screens remain at `why-uwa-india.html`, `scholarships.html`, `how-to-apply.html`, and `home.html`.

The two layouts follow the supplied course-listing screenshots: full-width laboratory images, overlapping Vivid Blue chevron panels, two hero actions, centred course cards and the complete shared footer. Introductory copy is from the supplied content PDF, pages 6–7. Card titles follow the screenshots. The first two undergraduate image cards have no visible titles in the reference; their accessible names describe course exploration without inventing program names.

Brand reference: UWA Brand Guidelines v1.1, pages 53–54 and 60–68. Uses local Melun Display and TT Norms Pro, Vivid Blue `#0032FF`, UWA Blue `#003087`, white and black, with logo proportions preserved and no display tracking adjustments.

The undergraduate banner is cropped from the supplied local course-page design. Campus card images reuse `join-uwa.jpg`. The postgraduate banner uses the same lab photograph from the official UWA High Performance Computing page, but its public rendition is cropped more tightly than the supplied screenshot; the full-frame original is needed for an exact photo match.

Page styles: `assets/css/course-listings.css`. Course cards open a native dialog with the application guide and a prefilled course enquiry email; no unsupported fees, intakes or eligibility criteria are invented. Behaviour: `assets/js/course-listings.js`. Header/footer behaviour remains shared.

Validation: Chrome at 390px, 581px and 1440px for both screens; image/font loading, horizontal overflow, course dialog and Escape, menu, search, country selector and Why UWA navigation. No browser errors observed.

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
