(() => {
 const root=document.documentElement,button=document.getElementById('theme-toggle');
 function sync(){
  const light=root.dataset.theme==='light',ar=root.lang==='ar';
  button.textContent=light?'☾':'☀';
  const label=ar?(light?'تفعيل الوضع الداكن':'تفعيل الوضع الفاتح'):(light?'Switch to dark theme':'Switch to light theme');
  button.setAttribute('aria-label',label);button.title=label;
  button.setAttribute('aria-pressed',String(!light));
  document.querySelector('meta[name="theme-color"]').content=light?'#faf8f4':'#090b0e';
  document.querySelector('meta[name="color-scheme"]').content=light?'light':'dark';
 }
 button.addEventListener('click',()=>{
  root.dataset.theme=root.dataset.theme==='light'?'dark':'light';
  try{localStorage.setItem('zakaa-theme',root.dataset.theme)}catch(e){}
  sync();
 });
 new MutationObserver(sync).observe(root,{attributes:true,attributeFilter:['lang']});
 window.addEventListener('storage',event=>{
  if(event.key==='zakaa-theme'){root.dataset.theme=event.newValue==='dark'?'dark':'light';sync();}
 });
 sync();
})();
