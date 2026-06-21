// @ts-check
import { defineConfig } from "astro/config";

// Static output, suitable for Cloudflare Pages (no adapter needed for a fully
// static build; Pages serves the dist/ directory directly).
export default defineConfig({
  site: "https://sphere.pub",
  output: "static",
  build: {
    format: "directory",
  },
});
