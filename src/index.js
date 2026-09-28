import chat from "./chat.js";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/chat") {
      return chat.fetch(request, env);
    }

    return env.ASSETS.fetch(request);
  },
};
