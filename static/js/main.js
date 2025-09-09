console.log("[main.js] loaded v8");
"use strict";

/* ============================================================
   1) RU PHONE MASK (delegated, independent)
   ============================================================ */
(function ruPhoneMaskBoot() {
  const SELECTOR = 'input[name="phone_number"]';
  const onlyDigits = (s) => String(s || "").replace(/\D/g, "");

  function toNational10(d) {
    if (d.startsWith("8")) d = "7" + d.slice(1);
    if (d.startsWith("7")) return d.slice(1).slice(0, 10);
    if (d.startsWith("9")) return d.slice(0, 10);
    if (d.length >= 10)    return d.slice(-10);
    return d.slice(0, 10);
  }

  function formatView(raw) {
    const nat = toNational10(onlyDigits(raw));
    let v = "+7";
    if (nat.length > 0) v += " (" + nat.slice(0, Math.min(3, nat.length));
    if (nat.length >= 3) v += ")";
    if (nat.length > 3)  v += " " + nat.slice(3, Math.min(6, nat.length));
    if (nat.length > 6)  v += "-" + nat.slice(6, Math.min(8, nat.length));
    if (nat.length > 8)  v += "-" + nat.slice(8, Math.min(10, nat.length));
    return { nat, view: v, e164: nat ? ("+7" + nat) : "+7" };
  }

  function setCaretEnd(el){ try{ const L = el.value.length; el.setSelectionRange(L, L); }catch{} }

  function attach(el) {
    if (!el || el.dataset.maskAttached) return;
    el.dataset.maskAttached = "1";
    if (!el.placeholder) el.placeholder = "+7 (___) ___-__-__";
    if (!el.maxLength)   el.maxLength   = 18;

    el.addEventListener("focus", () => {
      if (!el.value.trim()) { el.value = "+7 ("; setCaretEnd(el); }
    });

    el.addEventListener("input", () => {
      const { view } = formatView(el.value);
      el.value = view;
      requestAnimationFrame(() => setCaretEnd(el));
    });

    el.addEventListener("paste", (e) => {
      e.preventDefault();
      const t = (e.clipboardData || window.clipboardData).getData("text") || "";
      el.value = formatView(t).view;
      requestAnimationFrame(() => setCaretEnd(el));
    });

    el.addEventListener("keydown", (e) => {
      if (e.key === "Backspace" && el.selectionStart <= 4 && el.selectionEnd <= 4) {
        e.preventDefault();
      }
    });

    el.addEventListener("blur", () => {
      if (!formatView(el.value).nat) el.value = "";
    });
  }

  function boot() {
    document.querySelectorAll(SELECTOR).forEach(attach);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  document.addEventListener("focusin", (e) => {
    if (e.target && e.target.matches(SELECTOR)) attach(e.target);
  });

  window.__normalizeRuPhone   = (v) => formatView(v).e164;
  window.__isRuPhoneComplete  = (v) => formatView(v).nat.length === 10;
})();

/* ============================================================
   2) Helpers
   ============================================================ */
const $  = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

function showToast(msg, ok = true) {
  let n = $("#toast");
  if (!n) {
    n = document.createElement("div");
    n.id = "toast";
    n.setAttribute("role", "status");
    n.setAttribute("aria-live", "polite");
    Object.assign(n.style, {
      position: "fixed",
      left: "50%",
      top: "16px",
      transform: "translateX(-50%)",
      zIndex: 3000,
      padding: "10px 14px",
      borderRadius: "10px",
      color: "#fff",
      fontWeight: 700,
      boxShadow: "0 10px 28px rgba(0,0,0,.18)",
    });
    document.body.appendChild(n);
  }
  n.style.background = ok ? "#16a34a" : "#ef4444";
  n.textContent = msg;
  n.style.opacity = "1";
  setTimeout(() => {
    n.style.transition = "opacity .4s";
    n.style.opacity = "0";
  }, 2200);
}

function showFieldError(input, msg) {
  if (!input) return;
  input.classList.add("is-invalid");
  input.setAttribute("aria-invalid", "true");
  let n = input.parentElement.querySelector(".field-error");
  if (!n) {
    n = document.createElement("div");
    n.className = "field-error";
    input.parentElement.appendChild(n);
  }
  n.textContent = msg;
}

function clearErrors(form) {
  form.querySelectorAll(".is-invalid").forEach((i) => {
    i.classList.remove("is-invalid");
    i.removeAttribute("aria-invalid");
  });
  form.querySelectorAll(".field-error").forEach((n) => n.remove());
}

async function postJSON(url, data) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  const text = await res.text();
  let json;
  try { json = text ? JSON.parse(text) : {}; }
  catch { json = { detail: text || "Ошибка" }; }
  if (!res.ok) {
    const err = new Error("HTTP " + res.status);
    err.status = res.status;
    err.payload = json;
    throw err;
  }
  return json;
}

/* ============================================================
   3) Appointment form (safe consent + default age)
   ============================================================ */
(function appointmentForm() {
  const form = document.getElementById("appointment-form");
  if (!form) return;

  const ENDPOINT = "/api/v1/appointments/create";

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

  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearErrors(form);

    let ok = true;

    if (!el.first_name.value.trim()) { showFieldError(el.first_name, "Введите имя"); ok = false; }
    if (!el.last_name.value.trim())  { showFieldError(el.last_name, "Введите фамилию"); ok = false; }

    // AGE: если не выбрано — подставим по умолчанию (NOT NULL в БД)
    let ageVal = (el.age && el.age.value) ? el.age.value : "26-35";
    if (el.age && !el.age.value) el.age.value = ageVal;

    // Телефон
    if (!window.__isRuPhoneComplete(el.phone_number.value)) {
      showFieldError(el.phone_number, "Введите номер полностью");
      ok = false;
    }

    // Email при наличии
    const email = (el.email.value || "").trim();
    if (email && !EMAIL_RE.test(email)) { showFieldError(el.email, "Неверный email"); ok = false; }

    // Сообщение ограничим
    if (el.message && el.message.value.length > 1000) {
      showFieldError(el.message, "Сообщение слишком длинное");
      ok = false;
    }

    // Согласие — безопасная проверка, без падений
    if (el.privacy_consent && !el.privacy_consent.checked) {
      showFieldError(el.privacy_consent, "Нужно согласиться с политикой");
      ok = false;
    }

    if (!ok) return;

    const phoneE164   = window.__normalizeRuPhone(el.phone_number.value);
    const baseMsg     = (el.message && el.message.value ? el.message.value : "").trim();
    const extra       = [];
    if (el.preferred_time && el.preferred_time.value) extra.push(`Время: ${el.preferred_time.value}`);
    const finalMessage = [baseMsg, extra.join("; ")].filter(Boolean).join("\n") || null;

    const payload = {
      first_name:      el.first_name.value.trim(),
      last_name:       el.last_name.value.trim(),
      phone_number:    phoneE164,
      email:           email || null,
      age:             ageVal,
      message:         finalMessage,
      privacy_consent: el.privacy_consent ? (el.privacy_consent.checked === true) : true
    };

    el.submitBtn && (el.submitBtn.disabled = true);
    try {
      await postJSON(ENDPOINT, payload);
      showToast("Заявка отправлена!");
      form.reset();
    } catch (err) {
      console.warn("Ошибка отправки:", err.payload || err);
      const msg = (err.payload && (err.payload.detail || err.payload.message)) || "Не удалось отправить заявку";
      showToast(msg, false);
    } finally {
      el.submitBtn && (el.submitBtn.disabled = false);
    }
  });
})();

// На всякий случай снимем disabled и проверим клик
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.querySelector('#appointment-form button[type="submit"]');
  if (btn) {
    btn.disabled = false;
    btn.addEventListener('click', () => console.log('Submit: click'));
  }
});
