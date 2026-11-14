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

    if (url.pathname === "/") {
      const localizedUrl = new URL(request.url);
      localizedUrl.pathname = "/index.html";
      return env.ASSETS.fetch(new Request(localizedUrl, request));
    }

    if (url.pathname.startsWith("/ar/")) {
      if (request.method !== "GET" && request.method !== "HEAD") {
        return new Response("Method not allowed", {
          status: 405,
          headers: { Allow: "GET, HEAD" },
        });
      }

      const localizedUrl = new URL(request.url);
      const page = localizedUrl.pathname.replace(/^\/ar\/?/, "").replace(/\/+$/, "");
      localizedUrl.pathname = page ? `/ar/${page}.html` : "/ar/index.html";
      return env.ASSETS.fetch(new Request(localizedUrl, request));
    }

    if (url.pathname === "/en" || url.pathname.startsWith("/en/")) {
      if (request.method !== "GET" && request.method !== "HEAD") {
        return new Response("Method not allowed", {
          status: 405,
          headers: { Allow: "GET, HEAD" },
        });
      }

      const englishUrl = new URL(request.url);
      const page = englishUrl.pathname.replace(/^\/en\/?/, "").replace(/\/+$/, "");
      englishUrl.pathname = page ? `/en/${page}.html` : "/en/index.html";
      return env.ASSETS.fetch(new Request(englishUrl, request));
    }

    return env.ASSETS.fetch(request);
  },
};
