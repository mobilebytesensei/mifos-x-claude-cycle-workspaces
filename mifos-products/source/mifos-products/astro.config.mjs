// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// Static output — the whole site is a content-driven product catalog.
// `site` is overridden at build (SITE_URL env) so canonical/OG/sitemap URLs point
// at the deployed domain (mifos-products.pages.dev → products.mifos.org).
export default defineConfig({
  site: process.env.SITE_URL || "https://products.mifos.org",
  output: "static",
  build: { format: "directory" },
  integrations: [sitemap()],
});
