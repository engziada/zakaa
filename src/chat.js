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

const siteContent = `ZAKAA (Arabic: Zakaa) - "Intelligence, made useful."
ZAKAA is an AI consultancy that builds custom AI solutions for growing businesses. Website: https://Zakaa-AI.net

Why we exist: The future of work is not more software, it is less friction. Growing businesses do not need another dashboard to babysit. They need their systems to talk, their repetitive work to disappear, and their information to become useful. ZAKAA designs the intelligence layer that makes it happen, shaped around the client's people and processes. Not another AI tool - a better way to work, built around your business.

What we build (no boxes to fit into, only possibilities to build; every engagement starts with the client's workflow, not a product shelf):
1. Workflow automation - connects scattered tools and removes repetitive handoffs so teams can focus on work that moves the business forward.
2. Customer support - builds smarter support journeys that help customers faster and give the team the context to handle what matters.
3. Reporting and insights - turns fragmented operational data into a clearer view of performance, opportunities, and what needs attention.
4. Forecasting - uses available data to explore what may come next, with practical forecasts designed to support better planning.

The idea behind ZAKAA: Your business with a new layer of intelligence. Not a replacement for your team, an extension of what they can do. ZAKAA connects the information, tools, and decisions already inside the business, then builds the right intelligence around them.

How we work (first understand, then make it work - no one-size-fits-all platform):
1. Find the friction - map the work, the bottlenecks, and the outcomes worth improving.
2. Design around you - shape a practical AI solution around existing people, data, and tools.
3. Build, learn, improve - implement, validate with real workflows, and refine based on what works.

Proof over promises: ZAKAA is building its first public case studies. No invented metrics, no off-the-shelf demos presented as client work. The best example could be the one built together with you.

FAQ:
- Does ZAKAA sell ready-made AI products? No. ZAKAA designs and builds solutions around each business's needs, systems, and priorities.
- Do clients need to replace existing tools? Not necessarily. ZAKAA starts by understanding what is already used and where integration or improvement makes the most sense.
- Where should a small business start? Start with a process that consumes time, creates delays, or hides useful information. A consultation helps identify a practical first use case.
- Can ZAKAA guarantee a specific saving or forecast accuracy? Not before reviewing processes and data. ZAKAA agrees on measurable goals and validates results against real operating conditions.

About ZAKAA (company profile): ZAKAA was founded with a clear vision to empower organizations and companies through comprehensive digital transformation, delivering integrated technology solutions that combine efficient software architecture with precise analytics and innovative intelligence.
Our vision: To be the trusted, leading technology partner delivering software solutions and AI applications that advance business paths and make a real difference in information infrastructure and systems.
Our mission: To bridge the gap between advanced technologies and real market needs through custom, creative, and simplified software systems and applications that empower organizations and individuals to lead their digital future with confidence and intelligence.
What we do: (1) Software and application design and development - smart custom software and web applications tailored to each project's nature and scale. (2) Digital solutions and AI applications - integrating modern AI into work environments to automate tasks, raise productivity, and support decision-making. (3) Information systems foundation - building, structuring, and managing databases and information systems for flexible flow, fast retrieval, and top security standards. (4) Website and digital platform design - seamless, modern user experiences that reflect the client's identity and value. (5) Digital consulting and development - technology consulting for software infrastructure, data quality, and governance.
Why choose ZAKAA: Truly custom solutions (no off-the-shelf ideas; every solution starts from a precise understanding of the client's needs). Flexibility and speed (modern methodologies, efficient delivery in the shortest time). Smart integration (AI is an intrinsic part of the software, not a cosmetic add-on, giving a sustainable competitive advantage).

Contact: Consultations can be booked via WhatsApp (https://wa.me/201555558533) or by phone 02-01555558533. Email: Hello@Zakaa-AI.net or Support@Zakaa-AI.net. ZAKAA serves clients in English and Arabic and is based in Egypt.`;

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
