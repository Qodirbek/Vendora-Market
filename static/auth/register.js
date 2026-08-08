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
const phoneInput = document.getElementById("phone_input") || document.querySelector('input[name="phone"]');

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
// PASSWORD STRENGTH INDICATOR
// =====================================
const passwordInput = document.getElementById("password");

if (passwordInput) {
    passwordInput.addEventListener("input", function () {
        let strength = 0;
        let value = this.value;

        if (value.length >= 6) strength++;
        if (/[A-Z]/.test(value)) strength++;
        if (/[0-9]/.test(value)) strength++;
        if (/[^A-Za-z0-9]/.test(value)) strength++;

        let bar = document.querySelector(".password-strength div");

        if (bar) {
            bar.style.width = (strength * 25) + "%";
        }
    });
}

// =====================================
// CONFIRM PASSWORD CHECK
// =====================================
const confirmPasswordInput = document.getElementById("confirm_password");

if (confirmPasswordInput && passwordInput) {
    confirmPasswordInput.addEventListener("input", function () {
        if (passwordInput.value !== this.value) {
            this.style.borderColor = "#ef4444";
        } else {
            this.style.borderColor = "#10b981";
        }
    });
}

// =====================================
// REGISTER FORM VALIDATION
// =====================================
const registerForm = document.getElementById("register-form") || document.querySelector("form");

if (registerForm) {
    registerForm.addEventListener("submit", function (e) {
        // Agar Google OAuth orqali yuborilayotgan bo'lsa, lokal tekshiruvlarni o'tkazib yuboramiz
        const firebaseToken = document.getElementById("firebase_id_token");
        if (firebaseToken && firebaseToken.value.trim() !== "") {
            return;
        }

        let nameInput = document.querySelector('input[name="name"]');
        if (nameInput && nameInput.value.trim().length < 3) {
            e.preventDefault();
            showError("Ism kamida 3 ta harf bo'lishi kerak");
            return false;
        }

        let pass = passwordInput ? passwordInput.value : "";
        let confirm = confirmPasswordInput ? confirmPasswordInput.value : "";

        if (pass !== confirm) {
            e.preventDefault();
            showError("Parollar bir xil emas!");
            return false;
        }

        if (phoneInput) {
            let phone = phoneInput.value.replace(/\D/g, "");
            if (phone.length !== 9) {
                e.preventDefault();
                showError("Telefon raqam noto'g'ri (9 xonali bo'lishi kerak)");
                return false;
            }
        }

        const btn = document.getElementById("btn-register-submit") || document.querySelector(".register-btn");
        if (btn) {
            btn.innerHTML = "⏳ Yaratilmoqda...";
            btn.disabled = true;
        }
    });
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
// CAPSLOCK CHECK
// =====================================
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
document.addEventListener("DOMContentLoaded", () => {
    const nameInput = document.querySelector('input[name="name"]');
    if (nameInput) {
        nameInput.focus();
    }
});
