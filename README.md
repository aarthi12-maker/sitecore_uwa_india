# UWA India — complete static website

Run `npm start` and open http://127.0.0.1:3000. The homepage remains `index.html` (`home.html` is an alias). Open **All pages** at `site-map.html` to review every screen.

## Screens

There are 36 distinct screens, delivered as 37 HTML files including the homepage alias.

| Area | Screens |
| --- | --- |
| Home and Study | Homepage, Study hub, Why UWA India, undergraduate catalogue, postgraduate catalogue |
| Course details | Seven undergraduate offerings and two postgraduate offerings |
| Applying | How to apply, Fees, Scholarships, English language requirements, FAQs, Contact us |
| Student life | Student life, Events, Safety on campus, Student support services, Campus facilities, Mumbai campus, Chennai campus |
| Current students | Current students hub, Academic support, Library, LMS, Career support |
| Other navigation | Work with UWA India, Policies, Search, All pages |

Every page has consistent navigation, breadcrumbs, and the complete branded footer. Navigation distinguishes staff recruitment from student career support.

## Content and brand

The supplied **UWA India content – Copy.docx.pdf** is the primary content source. All its named page sections now have screens. Academic support, Library and LMS retain their detailed supplied content. Document metadata, editorial instructions and confidentiality footers are not displayed as public copy.

The supplied **UWA Brand Guidelines v1.1** govern typography and colours: local Melun Display for uppercase impact headlines with unchanged tracking, TT Norms Pro for supporting content, Vivid Blue `#0032FF`, UWA Blue `#003087`, approved secondary accents, white and black. Original logo proportions are preserved. The homepage's Google substitute fonts have been removed.

Pages that the PDF asks to import from the existing website use verified official sources, checked on **11 November 2026**. Course cards now use the current India catalogue, replacing the unverified screenshot labels “Bachelor of Computing” and “Master of Data Science.” Each detail page links to its definitive official course page. Published fees are explicitly first-year figures for 2026 commencing students; they are not presented as future-intake or whole-degree prices.

See [content coverage](docs/content-coverage.md) and the machine-readable `assets/data/content-coverage.json` for provenance and remaining confirmations.

## Working interactions

- Search indexes all distinct screens locally; no search backend is required.
- Course search filters by name/study area, study level and campus. Homepage course search passes those selections to the Study hub.
- Every course card opens a populated detail page.
- FAQ sections use keyboard-accessible native disclosures.
- Enquiry forms validate required fields and consent, then prepare an email draft with an explicit **Open email draft** action and a copyable fallback. They do not send personal data or claim a server submission.
- Events filter the published campus event-directory links; no unverified event dates are displayed.
- Campus maps use address-based map links. LMS orientation uses the video supplied in the PDF.
- Header search/menu support Escape and focus restoration.

## Checks and generation

```sh
npm run check
npm run generate
```

`check` verifies required pages, local assets, links, fragments, single page headings, duplicate IDs and removal of incomplete course cards. `generate` rebuilds document-based pages and upgrades shared components. It is repeatable without accumulating markup. Snapshot templates are in `scripts/templates/`.

Browser validation covered all 37 HTML files at 320px, 390px, 581px and 1440px, plus search, filtering, course navigation, enquiry validation/draft preparation, FAQ and header/footer controls. No missing images, horizontal document overflow or JavaScript errors were observed. External services were not exercised as part of local browser checks.

## Limits requiring external information or integration

- Campus-specific security contacts, assembly points and after-hours arrangements need institutional confirmation. The safety page provides verified India emergency 112 and wellbeing contact information; Perth's emergency contact is clearly labelled.
- Official event sources contain conflicting dates. The Events screen links to official directories without asserting upcoming dates.
- No CRM, server submission, authentication or Sitecore deployment is configured. Enquiries use the explicit email-draft workflow.
- Some existing reference photos are available only as tighter crops or comparable UWA imagery. No exact-photo match is claimed for those assets.

This is a local frontend implementation. It has not been published or migrated into Sitecore. The `data-rendering` attributes identify reusable rendering boundaries for that later integration.

## Homepage registration form

The full **Register your interest** form is present on `index.html` and `home.html`, including four enquiry-type tiles, enquiring-as choices, name/email/mobile, state/city, campus/program/course, intake guidance, optional message, client-side captcha and consent. State/city and campus/program/course controls are dependent; cities not listed can be entered manually. No unconfirmed intake dates are displayed. Submit validates the form and prepares a complete email draft. It does not claim CRM submission or server-side captcha protection.

The reusable markup is in `scripts/templates/register-interest.html`, styles in `assets/css/registration.css`, and behaviour in `assets/js/registration.js`. Regeneration preserves this full form.
