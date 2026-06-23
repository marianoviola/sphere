// @ts-check
import { defineConfig } from "astro/config";

import cloudflare from "@astrojs/cloudflare";

// Turn ```mermaid fenced code blocks into <pre class="mermaid"> so the client
// Mermaid runtime renders them, instead of letting Shiki highlight them as code.
function remarkMermaid() {
  const escape = (s) =>
    s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const walk = (nodes) => {
    if (!Array.isArray(nodes)) return;
    for (let i = 0; i < nodes.length; i += 1) {
      const node = nodes[i];
      if (node.type === "code" && node.lang === "mermaid") {
        nodes[i] = {
          type: "html",
          value: `<pre class="mermaid">${escape(node.value)}</pre>`,
        };
      } else if (node.children) {
        walk(node.children);
      }
    }
  };
  return (tree) => walk(tree.children);
}

// Static output, suitable for Cloudflare Pages (no adapter needed for a fully
// static build; Pages serves the dist/ directory directly).
export default defineConfig({
  site: "https://sphere.pub",
  output: "static",

  build: {
    format: "directory",
  },

  markdown: {
    // Dark theme for code snippets so the cards stay harmonious with the dark
    // page. The card background is overridden in CSS to the site panel colour.
    shikiConfig: {
      theme: "github-dark-dimmed",
    },
    remarkPlugins: [remarkMermaid],
  },

  adapter: cloudflare()
});