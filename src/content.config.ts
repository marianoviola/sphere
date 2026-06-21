import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

// Documentation and theory, published from src/content/docs/*.md. Each doc
// carries a `status` (shipped / mixed / vision) so the site can frame it
// honestly: what ships today versus what is concept and direction.
const docs = defineCollection({
  loader: glob({ pattern: "*.md", base: "./src/content/docs" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    status: z.enum(["shipped", "mixed", "vision"]),
    order: z.number(),
    note: z.string().optional(),
  }),
});

export const collections = { docs };
