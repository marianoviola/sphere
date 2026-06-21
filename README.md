# Sphere site

This repository is the public Sphere website: the landing page plus the published
documentation and theory. It is a static [Astro](https://astro.build) site and
deploys to Cloudflare Pages.

This repo is the front door, not the implementation. The implementation lives in
two separate repositories:

- [sphere-node](https://github.com/marianoviola/sphere-node) - the self-hostable
  content server on Cloudflare Workers.
- [sphere-plugin](https://github.com/marianoviola/sphere-plugin) - the local
  Claude desktop (MCPB) plugin for preparing and validating fragments.

The fragment contract is canonical in `sphere-node` under `spec/`
(`fragment.schema.json` and `node-api.md`). This site links to it and never
redefines it.

## Develop

```bash
npm install
npm run dev      # local dev server at http://localhost:4321
npm run build    # static build to dist/
npm run preview  # serve the production build locally
```

## Structure

- `src/pages/` - the landing page (`index.astro`), the docs index and pages, and
  the theory note.
- `src/components/` - hero, nav, and footer.
- `src/layouts/Base.astro` - shared head, fonts, and meta.
- `src/content/docs/` - the documentation and theory, as a content collection.
  Each document carries a `status` of `shipped`, `mixed`, or `vision` so the site
  can frame honestly what exists today versus what is concept and direction.
- `src/styles/global.css` - the design system (dark cosmic theme, IBM Plex Mono
  and Source Serif 4).
- `public/scripts/sphere-field.js` - the hero canvas animation.
- `public/assets/` - favicon and Open Graph image.

## Deploy

The site is static. On Cloudflare Pages, set the build command to
`npm run build` and the output directory to `dist`. No adapter or server runtime
is required.

## License

The site code is the author's. The documentation reflects the Sphere project by
Mariano Viola. Sphere is an independent project.
