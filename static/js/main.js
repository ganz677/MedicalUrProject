/* MedClinic — main.js (STATIC HEADER VERSION + Appointment Form) */

// ---------- Helpers ----------
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

// ---------- Fixed header offset ----------
(function headerOffset(){
  const header = $('.site-header');
  if (!header) return;
  const root = document.documentElement;

  function apply(){
    const h = header.getBoundingClientRect().height;
    root.style.setProperty('--header-offset', `${h}px`);
  }

  apply();
  window.addEventListener('load', apply);
  let to;
  window.addEventListener('resize', () => {
    clearTimeout(to);
    to = setTimeout(apply, 120);
  });
})();

// ---------- Disable compact mode ----------
(function compactHeader(){
  const header = $('.site-header');
  if (!header) return;
  header.classList.remove('is-compact');
})();

// ---------- Burger / Mobile menu ----------
(function mobileMenu(){
  const burger = $('#burger');
  const menu = $('#mobileMenu');
  if (!burger || !menu) return;

  const open = () => {
    menu.hidden = false;
    document.body.classList.add('no-scroll');
    burger.setAttribute('aria-expanded', 'true');
  };
  const close = () => {
    menu.hidden = true;
    document.body.classList.remove('no-scroll');
    burger.setAttribute('aria-expanded', 'false');
  };

  burger.addEventListener('click', () => (menu.hidden ? open() : close()));
  menu.addEventListener('click', (e) => { if (e.target === menu) close(); });
  window.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });

  $$('.mobile-nav .nav-link, .mobile-nav .btn-cta', menu).forEach(a => {
    a.addEventListener('click', () => close());
  });
})();

// ---------- Smooth anchor scroll ----------
(function smoothAnchors(){
  const header = $('.site-header');
  const getHeaderH = () => (header ? header.getBoundingClientRect().height : 0);

  function scrollToId(id) {
    const el = document.getElementById(id);
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const y = window.scrollY + rect.top - (getHeaderH() + 16);
    window.scrollTo({ top: y, behavior: 'smooth' });
  }

  $$('.main-nav .nav-link, .mobile-nav .nav-link, a.btn-cta[href^="#"]').forEach(a => {
    const h = a.getAttribute('href') || '';
    if (!h.startsWith('#') || h.length < 2) return;
    a.addEventListener('click', (e) => {
      e.preventDefault();
      const id = h.slice(1);
      scrollToId(id);
      history.replaceState(null, '', h);
    });
  });
})();

// ---------- Active link on scroll ----------
(function activeLinkOnScroll(){
  const header = $('.site-header');
  const links = $$('.main-nav .nav-link, .mobile-nav .nav-link');
  if (!header || links.length === 0) return;

  const map = {};
  links.forEach(a => {
    const h = a.getAttribute('href') || '';
    if (h.startsWith('#')) (map[h] ||= []).push(a);
  });

  const clearActive = () => links.forEach(a => a.classList.remove('active'));
  const setActive = (id) => {
    clearActive();
    (map[`#${id}`] || []).forEach(a => a.classList.add('active'));
  };

  const getHeaderH = () => header.getBoundingClientRect().height;
  const sections = $$('main > section[id]');
  let io;
  function initObserver(){
    if (io) io.disconnect();
    io = new IntersectionObserver((entries)=>{
      entries.forEach(e => { if (e.isIntersecting) setActive(e.target.id); });
    },{
      root: null,
      rootMargin: `-${getHeaderH()+20}px 0px -50% 0px`,
      threshold: 0.1
    });
    sections.forEach(s => io.observe(s));
  }
  initObserver();
  window.addEventListener('resize', () => {
    clearTimeout(window.__ioTO);
    window.__ioTO = setTimeout(initObserver, 150);
  });

  window.addEventListener('load', ()=>{
    const id = location.hash.slice(1);
    if (id) setActive(id);
  });
})();

// ---------- Status badge ----------
(function statusBadge(){
  const dot = $('#statusDot');
  const text = $('#statusText');
  if (!dot || !text) return;

  function isOpen(date = new Date()){
    const day = date.getDay(); // 0-вс, 1-пн … 6-сб
    const h = date.getHours();
    const openDay = day >= 1 && day <= 6;
    const openTime = h >= 9 && h < 20;
    return openDay && openTime;
  }
  function render(){
    const open = isOpen();
    dot.style.background = open ? '#22c55e' : '#ef4444';
    dot.style.boxShadow = open ? '0 0 0 3px rgba(34,197,94,0.18)' : '0 0 0 3px rgba(239,68,68,0.18)';
    text.textContent = open ? 'Открыто' : 'Закрыто';
  }
  render();
  setInterval(render, 60 * 1000);
})();

// ---------- Cookie banner ----------
(function cookieBanner(){
  const banner = $('#cookie-banner');
  if (!banner) return;
  const accept = $('#cookie-accept');
  const decline = $('#cookie-decline');

  const KEY = 'mc_cookie_choice';

  const hide = () => banner.classList.add('is-hidden');
  const show = () => banner.classList.remove('is-hidden');

  try{
    const choice = localStorage.getItem(KEY);
    if (!choice) show();
  }catch(_){}

  accept?.addEventListener('click', () => {
    try{ localStorage.setItem(KEY, 'accepted'); }catch(_){}
    hide();
  });
  decline?.addEventListener('click', () => {
    try{ localStorage.setItem(KEY, 'declined'); }catch(_){}
    hide();
  });
})();

// ---------- Progressive reveal for cards ----------
(function revealCards(){
  document.documentElement.classList.add('js-ready');
  const els = $$('.about-card, .advantages-card');
  const io = new IntersectionObserver((entries)=>{
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('is-visible'); });
  },{ threshold: .2 });
  els.forEach(el => io.observe(el));
})();

// ---------- Appointment form ----------
(function appointmentForm(){
  const form = $('#appointment-form');
  if (!form) return;

  const ENDPOINT = '/api/v1/appointments/create';

  const el = {
    first_name: form.querySelector('[name="first_name"]'),
    last_name: form.querySelector('[name="last_name"]'),
    phone_number: form.querySelector('[name="phone_number"]'),
    email: form.querySelector('[name="email"]'),
    age: form.querySelector('[name="age"]'),
    preferred_time: form.querySelector('[name="preferred_time"]'),
    message: form.querySelector('[name="message"]'),
    privacy_consent: form.querySelector('[name="privacy_consent"]'),
    submitBtn: form.querySelector('button[type="submit"]'),
  };

  const PHONE_RE = /^\+?\d[\d\-\s\(\)]{9,}$/;
  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  const showFieldError = (input, msg)=>{
    if (!input) return;
    input.classList.add('is-invalid');
    let n = input.parentElement.querySelector('.field-error');
    if (!n) {
      n = document.createElement('div');
      n.className='field-error';
      input.parentElement.appendChild(n);
    }
    n.textContent = msg;
  };
  const clearErrors = ()=>{
    form.querySelectorAll('.is-invalid').forEach(i=>i.classList.remove('is-invalid'));
    form.querySelectorAll('.field-error').forEach(n=>n.remove());
  };

  const normalizePhone = v=>{
    const d = (v||'').replace(/[^\d+]/g,'');
    if(/^8\d{10}$/.test(d))   return '+7'+d.slice(1);
    if(/^\+7\d{10}$/.test(d)) return d;
    if(/^\d{11}$/.test(d))    return '+'+d;
    return d;
  };

  const toast = (msg, ok=true)=>{
    let n = document.getElementById('toast'); if(!n){
      n = document.createElement('div'); n.id='toast';
      Object.assign(n.style,{position:'fixed',left:'50%',top:'16px',transform:'translateX(-50%)',
        zIndex:3000,padding:'10px 14px',borderRadius:'10px',color:'#fff',fontWeight:700,
        boxShadow:'0 10px 28px rgba(0,0,0,.18)'});
      document.body.appendChild(n);
    }
    n.style.background = ok ? '#16a34a' : '#ef4444';
    n.textContent = msg; n.style.opacity='1';
    setTimeout(()=>{ n.style.transition='opacity .4s'; n.style.opacity='0'; }, 2200);
  };

  async function postJSON(url, data){
    const res = await fetch(url, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(data)
    });
    const text = await res.text();
    let json; try{ json = text ? JSON.parse(text) : {}; }catch{ json = { detail: text||'Ошибка' }; }
    if(!res.ok){ const err = new Error('HTTP '+res.status); err.status=res.status; err.payload=json; throw err; }
    return json;
  }

  function validate(){
    clearErrors();
    let ok = true;

    if(!el.first_name.value.trim()){ showFieldError(el.first_name,'Введите имя'); ok=false; }
    if(!el.last_name.value.trim()){ showFieldError(el.last_name,'Введите фамилию'); ok=false; }

    el.phone_number.value = normalizePhone(el.phone_number.value);
    if(!PHONE_RE.test(el.phone_number.value)){ showFieldError(el.phone_number,'Неверный телефон'); ok=false; }

    const email = el.email.value.trim();
    if(email && !EMAIL_RE.test(email)){ showFieldError(el.email,'Неверный email'); ok=false; }

    if(!el.age.value){ showFieldError(el.age,'Выберите возраст'); ok=false; }
    if(!el.preferred_time.value){ showFieldError(el.preferred_time,'Выберите время'); ok=false; }

    if(el.message && el.message.value.length > 1000){
      showFieldError(el.message,'Сообщение слишком длинное'); ok=false;
    }

    if(!el.privacy_consent.checked){
      showFieldError(el.privacy_consent, 'Нужно согласиться с политикой');
      ok=false;
    }

    return ok;
  }

  form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    if(!validate()) return;

    const payload = {
      first_name:     el.first_name.value.trim(),
      last_name:      el.last_name.value.trim(),
      phone_number:   el.phone_number.value.trim(),
      email:          el.email.value.trim() || null,   // вместо '' — null
      age:            el.age.value,
      preferred_time: el.preferred_time.value,
      message:        (el.message?.value ?? '').trim() || null,
      privacy_consent: true                            // всегда true, т.к. по ТЗ запись невозможна без согласия
    };

    el.submitBtn.disabled = true;
    try{
      await postJSON(ENDPOINT, payload);
      toast('Заявка отправлена!');
      form.reset();
    }catch(err){
      console.warn('Ошибка отправки:', err.payload || err);
      const msg =
        (err.payload && (err.payload.detail || err.payload.message)) ||
        'Не удалось отправить заявку';
      toast(msg, false);
    }finally{
      el.submitBtn.disabled = false;
    }
  });
})();
