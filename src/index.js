import chat from "./chat.js";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/chat") {
      return chat.fetch(request, env);
    }

    if (url.pathname === "/ar" || url.pathname === "/ar/" || url.pathname === "/ar/index.html" || url.pathname === "/index.html") {
      url.pathname = "/";
      return Response.redirect(url, 301);
    }

    if (url.pathname === "/en/index.html") {
      url.pathname = "/en/";
      return Response.redirect(url, 301);
    }

    if (url.pathname.startsWith("/ar/") || url.pathname === "/en" || url.pathname.startsWith("/en/")) {
      if (request.method !== "GET" && request.method !== "HEAD") {
        return new Response("Method not allowed", {
          status: 405,
          headers: { Allow: "GET, HEAD" },
        });
      }
    }

    return env.ASSETS.fetch(request);
  },
};
