import type { MetadataRoute } from "next";
import { ALL_NODES } from "@/lib/data";

import { SITE_URL } from "@/lib/site";

const PAGES = ["", "/graph", "/narratives", "/nodes", "/quality", "/prompts", "/review", "/contribute", "/pipeline", "/about"];

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    ...PAGES.map((p) => ({ url: `${SITE_URL}${p}` })),
    ...ALL_NODES.map((n) => ({ url: `${SITE_URL}/nodes/${n.id}` })),
  ];
}
