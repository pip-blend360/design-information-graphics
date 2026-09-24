# Brand Profiles

Store brand information outside the skill in a project or governed shared collection, such as `visualization/brands/<brand-id>/` with `brand-profile.yaml`, `examples/`, and authorized assets. Keep the skill generic.

Accept user-supplied PPTX, SVG, HTML/CSS, PDF, PNG, JPEG, or screenshots. Extract exact theme colors and fonts where formats expose them. Treat raster colors and typography as estimates. Distinguish functional data, emphasis, text, guide, and background colors from photography or decoration. Do not claim an exact font from raster evidence.

Separate verified properties from inferred ones and request confirmation when uncertainty is material. Store semantic roles, not only hex codes. Never download or redistribute fonts. If a font is unavailable, report it and propose a fallback; ask for confirmation if the substitution is material.

```yaml
brand_id: acme
version: 1
status: inferred-and-confirmed
sources: []
typography:
  heading: {family: Aptos Display, weight: semibold}
  body: {family: Aptos, weight: regular}
  fallbacks: [Arial, DejaVu Sans]
colors:
  primary: "#2474B5"
  accent: "#E87932"
  text: "#252A2E"
  background: "#FFFFFF"
semantic_colors:
  primary_series: primary
  comparison_series: "#71777C"
  emphasis: accent
composition:
  title_alignment: left
  direct_labels: preferred
  gridlines: restrained
```

Apply creator-approved overrides, then project standards, then the brand profile, then skill defaults. Preserve graphical integrity when brand conventions obscure evidence, and document the departure.
