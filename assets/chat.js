/* Same-origin Workers AI chat. Responses are rendered as text, never HTML. */
(() => {
  const toggle = document.getElementById('zakaa-chat-toggle');
  if (!toggle) return;
  const text = {
    en: {title:'Zaka2 assistant',sub:'AI guidance · Human expertise',open:'Ask Zaka2',close:'Close chat',greeting:'Hello. Tell me what you want to improve, or ask about our services and projects.',placeholder:'What could work better?',send:'Send',typing:'Thinking…',label:'Your message',human:'Talk to our team ↗',services:'What can you build?',projects:'Tell me about your projects',consult:'How do I book a consultation?',error:'We could not connect. Please try again or contact our team.',rate:'Please wait a few minutes before sending another message.',timeout:'The reply took too long. Please try again.',retry:'Retry',notice:'AI assistant. Please avoid sharing sensitive information.'},
    ar: {title:'مساعد ذكاء',sub:'إرشاد بالذكاء الاصطناعي · خبرة بشرية',open:'اسأل ذكاء',close:'إغلاق المحادثة',greeting:'أهلًا بك. أخبرني بما تريد تحسينه، أو اسأل عن خدماتنا ومشاريعنا.',placeholder:'كيف نساعدك في تطوير عملك؟',send:'إرسال',typing:'جارٍ التفكير…',label:'رسالتك',human:'تواصل مع فريقنا ↗',services:'ما الحلول التي تقدمونها؟',projects:'أخبرني عن مشاريعكم',consult:'كيف أحجز استشارة؟',error:'تعذر الاتصال. حاول مرة أخرى أو تواصل مع فريقنا.',rate:'يرجى الانتظار بضع دقائق قبل إرسال رسالة أخرى.',timeout:'استغرق الرد وقتًا طويلًا. حاول مرة أخرى.',retry:'حاول مجددًا',notice:'مساعد بالذكاء الاصطناعي. يرجى عدم مشاركة معلومات حساسة.'}
  };
  const dialog = document.createElement('dialog');
  dialog.id = 'zakaa-chat-panel'; dialog.className = 'chat-panel'; dialog.setAttribute('aria-labelledby', 'chat-title');
  // This template contains only fixed, developer-controlled markup.
  dialog.innerHTML = `<div class="chat-heading"><div><h2 id="chat-title"></h2><p class="chat-sub"></p></div><button class="chat-close" type="button">×</button></div><div class="chat-messages" role="log" aria-live="polite" aria-relevant="additions text"><p class="chat-bubble assistant chat-greeting"></p></div><div class="chat-suggestions"></div><div class="chat-status" role="status"></div><button class="chat-retry" type="button" hidden></button><form class="chat-form"><label class="sr-only" for="zakaa-chat-input"></label><input id="zakaa-chat-input" name="message" maxlength="2000" autocomplete="off" required><button class="chat-send" type="submit"></button></form><p class="chat-notice"></p><a class="chat-human" href="https://wa.me/201555558533" target="_blank" rel="noopener noreferrer"></a>`;
  document.body.append(dialog);
  const input = dialog.querySelector('input');
  const send = dialog.querySelector('.chat-send');
  const log = dialog.querySelector('.chat-messages');
  const status = dialog.querySelector('.chat-status');
  const retry = dialog.querySelector('.chat-retry');
  const suggestions = dialog.querySelector('.chat-suggestions');
  const history = [];
  let pending = false, failed = null, errorKey = null;
  const lang = () => document.documentElement.lang === 'ar' ? 'ar' : 'en';
  const copy = () => text[lang()];
  function localize() {
    const t = copy();dialog.dir = lang() === 'ar' ? 'rtl' : 'ltr';dialog.lang = lang();
    dialog.querySelector('h2').textContent = t.title;
    dialog.querySelector('.chat-sub').textContent = t.sub;
    dialog.querySelector('.chat-close').setAttribute('aria-label',t.close);
    dialog.querySelector('.chat-greeting').textContent = t.greeting;
    dialog.querySelector('label').textContent = t.label;
    dialog.querySelector('.chat-notice').textContent = t.notice;
    dialog.querySelector('.chat-human').textContent = t.human;
    input.placeholder = t.placeholder;send.textContent = t.send;retry.textContent = t.retry;
    toggle.querySelector('span').textContent = t.open;toggle.setAttribute('aria-label', t.open);
    suggestions.replaceChildren();
    for (const key of ['services','projects','consult']) {
      const button = document.createElement('button');button.type = 'button';button.textContent = t[key];button.disabled = pending;
      button.addEventListener('click', () => requestReply(copy()[key]));suggestions.append(button);
    }
    status.textContent = pending ? t.typing : errorKey ? t[errorKey] : '';
  }
  function bubble(message, role) {
    const element = document.createElement('p');element.className = `chat-bubble ${role}`;element.dir = 'auto';element.textContent = message;log.append(element);log.scrollTop = log.scrollHeight;
  }
  function busy(value) {
    pending = value;send.disabled = value;input.disabled = value;
    suggestions.querySelectorAll('button').forEach(button => button.disabled = value);
    dialog.setAttribute('aria-busy', String(value));
  }
  async function requestReply(raw, isRetry = false) {
    const message = raw.trim();
    if (!message || pending || message.length > 2000) return;
    if (!isRetry) bubble(message, 'user');
    input.value = '';failed = null;errorKey = null;retry.hidden = true;busy(true);status.textContent = copy().typing;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);
    try {
      const response = await fetch('/api/chat', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body:JSON.stringify({message,history:history.slice(-10)}), signal:controller.signal
      });
      if (response.status === 429) {errorKey = 'rate';throw new Error('rate');}
      if (!response.ok || !response.headers.get('content-type')?.includes('application/json')) throw new Error('unavailable');
      const data = await response.json();
      if (typeof data.response !== 'string' || !data.response.trim()) throw new Error('empty');
      bubble(data.response, 'assistant');
      history.push({role:'user',content:message},{role:'assistant',content:data.response});
      if (history.length > 10) history.splice(0,history.length-10);
      status.textContent = '';
    } catch (error) {
      errorKey = errorKey || (error.name === 'AbortError' ? 'timeout' : 'error');
      status.textContent = copy()[errorKey];failed = message;retry.hidden = false;
    } finally {
      clearTimeout(timeout);busy(false);if (dialog.open) input.focus();
    }
  }
  toggle.addEventListener('click', () => {
    localize();dialog.showModal();toggle.setAttribute('aria-expanded','true');input.focus();
  });
  dialog.querySelector('.chat-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => {toggle.setAttribute('aria-expanded','false');toggle.focus();});
  dialog.querySelector('form').addEventListener('submit', event => {event.preventDefault();requestReply(input.value);});
  retry.addEventListener('click', () => {if (failed) requestReply(failed, true);});
  new MutationObserver(localize).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
  localize();
})();
