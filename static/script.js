/* ===========================================================
   NextHire Professional JavaScript
=========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    /* ===============================
       MOBILE MENU
    =============================== */

    const menuBtn = document.querySelector(".menu-toggle");
    const nav = document.querySelector("nav");

    if (menuBtn && nav) {

        menuBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            nav.classList.toggle("show");

            if (nav.classList.contains("show")) {
                menuBtn.innerHTML = "✕";
            } else {
                menuBtn.innerHTML = "☰";
            }
        });

        document.querySelectorAll("nav a").forEach(link => {
            link.addEventListener("click", () => {
                nav.classList.remove("show");
                menuBtn.innerHTML = "☰";
            });
        });

        document.addEventListener("click", function (e) {
            if (!nav.contains(e.target) && !menuBtn.contains(e.target)) {
                nav.classList.remove("show");
                menuBtn.innerHTML = "☰";
            }
        });

        window.addEventListener("resize", function () {
            if (window.innerWidth > 768) {
                nav.classList.remove("show");
                menuBtn.innerHTML = "☰";
            }
        });

    }

    /* ===============================
       TYPING ANIMATION
    =============================== */

    const typingElement = document.getElementById("typing-text");

    if (typingElement) {

        const phrases = [
            "Get Hired",
            "Build Your Resume",
            "Beat ATS Systems",
            "Land Your Dream Job"
        ];

        let phraseIndex = 0;
        let letterIndex = 0;
        let deleting = false;

        function typeEffect() {

            const current = phrases[phraseIndex];

            if (!deleting) {

                typingElement.textContent =
                    current.substring(0, letterIndex + 1);

                letterIndex++;

                if (letterIndex === current.length) {

                    deleting = true;

                    setTimeout(typeEffect, 1700);

                    return;
                }

            } else {

                typingElement.textContent =
                    current.substring(0, letterIndex - 1);

                letterIndex--;

                if (letterIndex === 0) {

                    deleting = false;

                    phraseIndex++;

                    if (phraseIndex >= phrases.length)
                        phraseIndex = 0;
                }

            }

            setTimeout(typeEffect, deleting ? 45 : 95);

        }

        typeEffect();

    }

    /* ===============================
       COUNTER
    =============================== */

    const counter = document.getElementById("resume-counter");

    if (counter) {

        let value = 1000;

        const target = 1200;

        const timer = setInterval(() => {

            value += 2;

            counter.textContent = value + "+";

            if (value >= target) {

                counter.textContent = target + "+";

                clearInterval(timer);

            }

        }, 18);

    }

    /* ===============================
       PHONE VALIDATION
    =============================== */

    const countryData = {

        IN: {
            code: "+91",
            len: 10
        },

        US: {
            code: "+1",
            len: 10
        },

        UK: {
            code: "+44",
            len: 10
        }

    };

    const countrySelect = document.getElementById("country_select");
    const phoneInput = document.getElementById("phone_input");
    const hiddenCode = document.getElementById("hidden_country_code");

    if (countrySelect && phoneInput && hiddenCode) {

        function updatePhone() {

            const data = countryData[countrySelect.value];

            if (!data) return;

            hiddenCode.value = data.code;

            phoneInput.maxLength = data.len;

            phoneInput.placeholder =
                `Enter ${data.len} digit phone number`;

            phoneInput.value = "";

        }

        updatePhone();

        countrySelect.addEventListener("change", updatePhone);

    }

    /* ===============================
       FILE NAME PREVIEW
    =============================== */

    const fileInput = document.querySelector("input[type='file']");

    if (fileInput) {

        fileInput.addEventListener("change", function () {

            if (!this.files.length) return;

            const info = document.createElement("p");

            info.className = "file-preview";

            info.innerHTML =
                "📄 " + this.files[0].name;

            const old =
                document.querySelector(".file-preview");

            if (old)
                old.remove();

            this.parentNode.appendChild(info);

        });

    }

    /* ===============================
       BUTTON LOADING
    =============================== */

    document.querySelectorAll("form").forEach(form => {

        form.addEventListener("submit", function () {

            const btn =
                form.querySelector("button,input[type=submit]");

            if (!btn) return;

            btn.dataset.original =
                btn.innerHTML || btn.value;

            if (btn.tagName === "BUTTON")
                btn.innerHTML = "Processing...";
            else
                btn.value = "Processing...";

            btn.disabled = true;

        });

    });

    /* ===============================
       FADE IN ANIMATION
    =============================== */

    const observer = new IntersectionObserver(entries => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("fade");

            }

        });

    }, {
        threshold: .15
    });

    document.querySelectorAll(".card,.feature-card,.counter,.upload-card,.suggestion-box,.result-card,.form-container")
        .forEach(el => observer.observe(el));

});
