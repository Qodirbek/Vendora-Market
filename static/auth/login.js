// =====================================
// PASSWORD SHOW / HIDE
// =====================================
function togglePassword(id) {
    const targetId = id || "password";
    const passwordInput = document.getElementById(targetId);

    if (!passwordInput) return;

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}

// =====================================
// PHONE FORMAT (+998 90 123 45 67)
// =====================================
const phoneInput = document.querySelector('input[name="phone"]');

if (phoneInput) {
    phoneInput.addEventListener("input", function () {
        let value = this.value.replace(/\D/g, "");

        // 998 bilan boshlansa olib tashlash
        if (value.startsWith("998")) {
            value = value.substring(3);
        }

        // Faqat 9 ta raqam kiritishga ruxsat
        value = value.substring(0, 9);

        let result = "";

        if (value.length > 0) {
            result = value.substring(0, 2);
        }
        if (value.length >= 3) {
            result += " " + value.substring(2, 5);
        }
        if (value.length >= 6) {
            result += " " + value.substring(5, 7);
        }
        if (value.length >= 8) {
            result += " " + value.substring(7, 9);
        }

        this.value = result;
    });
}

// =====================================
// PHONE VALIDATION
// =====================================
function checkPhone() {
    if (!phoneInput) return true;

    let phone = phoneInput.value.replace(/\D/g, "");

    if (phone.length !== 9) {
        showError("Telefon raqam noto'g'ri (9 ta raqam bo'lishi kerak)");
        return false;
    }

    return true;
}

// =====================================
// ERROR MESSAGE DISPLAY
// =====================================
function showError(text) {
    let box = document.querySelector(".js-error");

    if (!box) {
        box = document.createElement("div");
        box.className = "alert danger js-error";

        const card = document.querySelector(".auth-card");
        if (card) {
            card.prepend(box);
        }
    }

    box.innerHTML = text;
    box.classList.add("shake");

    setTimeout(() => {
        box.classList.remove("shake");
    }, 500);
}

// =====================================
// FORM SUBMIT INTERCEPTOR
// =====================================
const loginForm = document.querySelector("form");

if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
        // Agar Google Login yoki OTP orqali yuborilayotgan bo'lsa, telefon tekshiruvini o'tkazib yuboramiz
        const loginType = document.getElementById("login_type");
        if (loginType && (loginType.value === "google" || loginType.value === "otp")) {
            return;
        }

        if (!checkPhone()) {
            e.preventDefault();
            return;
        }

        const btn = document.querySelector(".login-btn");
        if (btn) {
            btn.innerHTML = "⏳ Tekshirilmoqda...";
            btn.disabled = true;
        }
    });
}

// =====================================
// CAPS LOCK CHECK
// =====================================
const passwordInput = document.getElementById("password");

if (passwordInput) {
    passwordInput.addEventListener("keyup", function (e) {
        if (e.getModifierState && e.getModifierState("CapsLock")) {
            showError("⚠️ CapsLock yoqilgan");
        }
    });
}

// =====================================
// AUTO FOCUS
// =====================================
window.addEventListener("load", () => {
    if (phoneInput) {
        phoneInput.focus();
    }
});
