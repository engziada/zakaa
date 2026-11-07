import { projects } from "../assets/project-data.js";

const MODEL = "@cf/meta/llama-3.1-8b-instruct-fp8";
const RATE_LIMIT = 10;
const RATE_WINDOW_MS = 5 * 60 * 1000;
const hits = new Map();

function isRateLimited(ip) {
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter((t) => now - t < RATE_WINDOW_MS);
  if (recent.length >= RATE_LIMIT) {
    hits.set(ip, recent);
    return true;
  }
  recent.push(now);
  hits.set(ip, recent);
  if (hits.size > 5000) {
    for (const key of hits.keys()) {
      if (hits.get(key).every((t) => now - t >= RATE_WINDOW_MS)) hits.delete(key);
    }
  }
  return false;
}

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
  };
}

function jsonResponse(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...corsHeaders() },
  });
}

const portfolioContent = projects.map((project) => `${project.name}: ${project.en}`).join("\n");

const siteContent = `Zaka2 / ذكاء. Website https://zakaa-ai.net.
Services: AI and custom software; workflow automation, integrations, reporting and customer support; websites and e-commerce storefront design; business operations consulting, crisis management and business continuity.
Products: ERP360, WorkTracker, YourSpace and Gathering. Configuration and implementation are scoped with the client. ERP360 supports customization and additional modules.
Academy & Learning Experiences: AI workshops for educators/lecturers, children and youth; programming and AI training for adults, employees and executives; leadership and soft skills, crisis and continuity exercises. Learning experiences include Kids AI Academy, Little Explorer and Family Games.
Community initiatives: Madinaty AI for residential communities groups its administration, life, kitchen and delivery portals. AutoStop is an in-development community carpool application, not a production-ready transport marketplace. Loqma / لقمة is a home-kitchen initiative: only its general concept is confirmed, do not invent operational features or launch readiness.
Separate projects: Souk El Kanto and Masar are in development; EduFlow is a blueprint and prototypes. These are not part of the ready-made product catalogue.
Current catalogue details:
${portfolioContent}
Contact by phone or WhatsApp: +201026655008, https://wa.me/201026655008. Email: Hello@Zakaa-AI.net or Support@Zakaa-AI.net.
Serving Cairo including Madinaty, Al Rehab, Nasr City, Heliopolis, Shorouk City and Mohandessin. Do not invent prices, schedules, locations, client results or availability. Direct visitors to the team to confirm them.
`;

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders() });
    }

    if (request.method !== "POST") {
      return jsonResponse({ error: "Method not allowed" }, 405);
    }

    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    if (isRateLimited(ip)) {
      return jsonResponse({ error: "Too many requests" }, 429);
    }

    let body;
    try {
      body = await request.json();
    } catch (err) {
      return jsonResponse({ error: "Invalid JSON body" }, 400);
    }

    const message = typeof body?.message === "string" ? body.message.trim().slice(0, 2000) : "";
    if (!message) {
      return jsonResponse({ error: "Missing message" }, 400);
    }

    const history = Array.isArray(body?.history)
      ? body.history
          .filter(
            (m) =>
              m &&
              (m.role === "user" || m.role === "assistant") &&
              typeof m.content === "string" &&
              m.content.trim()
          )
          .slice(-10)
          .map((m) => ({ role: m.role, content: m.content.trim().slice(0, 1000) }))
      : [];

    try {
      const result = await env.AI.run(MODEL, {
        messages: [
          {
            role: "system",
            content: `You are the ZAKAA AI assistant. ZAKAA is an AI consultancy that makes intelligence useful for businesses. Answer visitor questions about ZAKAA's services based on the website content below. Be concise, friendly, and helpful. If asked about booking, mention that consultations can be booked via WhatsApp. Keep responses under 3 sentences. Always respond in the same language the visitor writes in (English or Arabic).\n\nWebsite content:\n${siteContent}`,
          },
          ...history,
          { role: "user", content: message },
        ],
        max_tokens: 256,
      });

      const reply = typeof result?.response === "string" ? result.response.trim() : "";
      if (!reply) {
        return jsonResponse({ error: "Empty response from AI" }, 502);
      }
      return jsonResponse({ response: reply });
    } catch (err) {
      return jsonResponse({ error: "Something went wrong" }, 500);
    }
  },
};
