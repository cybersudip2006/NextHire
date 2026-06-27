
/* ===========================================================
   NextHire Professional JavaScript
=========================================================== */

document.addEventListener("DOMContentLoaded", () => {
    const $ = (selector) => document.querySelector(selector);
    const $$ = (selector) => document.querySelectorAll(selector);

    /* MOBILE NAVBAR */
    const menuBtn = $(".menu-toggle");
    const nav = $("nav");

    if (menuBtn && nav) {
        menuBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            nav.classList.toggle("show");
            menuBtn.innerHTML = nav.classList.contains("show") ? "✕" : "☰";
        });

        $$("nav a").forEach(link => {
            link.addEventListener("click", () => {
                nav.classList.remove("show");
                menuBtn.innerHTML = "☰";
            });
        });

        document.addEventListener("click", (e) => {
            if (!nav.contains(e.target) && !menuBtn.contains(e.target)) {
                nav.classList.remove("show");
                menuBtn.innerHTML = "☰";
            }
        });

        window.addEventListener("resize", () => {
            if (window.innerWidth > 768) {
                nav.classList.remove("show");
                menuBtn.innerHTML = "☰";
            }
        });
    }

    /* HERO TYPING */
    const typing = $("#typing-text");
    const phrases = [
        "Get an Interview",
        "Get Hired",
        "Get Promoted",
        "Land Your Dream Job",
        "Beat ATS Filters",
        "Build Your Career"
    ];

    let phrase = 0;
    let letter = 0;
    let deleting = false;

    function typeAnimation() {
        if (!typing) return;

        const current = phrases[phrase];

        if (!deleting) {
            typing.textContent = current.substring(0, letter + 1);
            letter++;

            if (letter === current.length) {
                deleting = true;
                setTimeout(typeAnimation, 1700);
                return;
            }
        } else {
            typing.textContent = current.substring(0, letter - 1);
            letter--;

            if (letter === 0) {
                deleting = false;
                phrase = (phrase + 1) % phrases.length;
            }
        }

        setTimeout(typeAnimation, deleting ? 45 : 90);
    }

    typeAnimation();

    /* COUNTER */
    const counter = $("#resume-counter");
    if (counter) {
        let value = 1000;
        const target = 1250;
        counter.textContent = value;

        const timer = setInterval(() => {
            value++;
            counter.textContent = value;

            if (value >= target) {
                counter.textContent = target + "+";
                clearInterval(timer);
            }
        }, 35);
    }

    /* PHONE VALIDATION */
    const countryData = {
        IN: { code: "+91", len: 10 },
        US: { code: "+1", len: 10 },
        UK: { code: "+44", len: 10 },
        CA: { code: "+1", len: 10 },
        AU: { code: "+61", len: 9 }
    };

    const country = $("#country_select");
    const phone = $("#phone_input");
    const hidden = $("#hidden_country_code");

    if (country && phone && hidden) {
        function updatePhone() {
            const data = countryData[country.value];
            if (!data) return;

            hidden.value = data.code;
            phone.maxLength = data.len;
            phone.placeholder = `Enter ${data.len} digit phone number`;
        }

        updatePhone();
        country.addEventListener("change", updatePhone);
    }

    /* PROFILE PHOTO PREVIEW */
    const profileInput = $("#profile_photo");
    const previewImage = $("#photo-preview");
    const uploadBox = $(".image-upload");

    function showImagePreview(file) {
        if (!file || !previewImage) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            previewImage.src = event.target.result;
            previewImage.style.display = "block";
        };
        reader.readAsDataURL(file);
    }

    if (profileInput) {
        profileInput.addEventListener("change", function () {
            if (!this.files.length) return;
            showImagePreview(this.files[0]);

            let info = this.parentNode.querySelector(".file-preview");
            if (!info) {
                info = document.createElement("p");
                info.className = "file-preview";
                this.parentNode.appendChild(info);
            }
            info.innerHTML = "📄 " + this.files[0].name;
        });
    }

    if (uploadBox && profileInput) {
        uploadBox.addEventListener("dragover", (e) => {
            e.preventDefault();
            uploadBox.classList.add("dragging");
        });

        uploadBox.addEventListener("dragleave", () => {
            uploadBox.classList.remove("dragging");
        });

        uploadBox.addEventListener("drop", (e) => {
            e.preventDefault();
            uploadBox.classList.remove("dragging");

            if (!e.dataTransfer.files.length) return;
            profileInput.files = e.dataTransfer.files;
            showImagePreview(e.dataTransfer.files[0]);
        });
    }

    /* LIVE PREVIEW */
    function bindPreview(inputId, previewId, fallback = "") {
        const input = document.getElementById(inputId);
        const preview = document.getElementById(previewId);

        if (!input || !preview) return;

        const update = () => {
            preview.textContent = input.value.trim() || fallback;
        };

        input.addEventListener("input", update);
        update();
    }

    bindPreview("name", "preview-name", "Your Name");
    bindPreview("title", "preview-title", "Professional Title");
    bindPreview("email", "preview-email", "email@example.com");
    bindPreview("phone_input", "preview-phone", "+91 9876543210");
    bindPreview("address", "preview-address", "Your Address");
    bindPreview("objective", "preview-objective", "Your professional summary...");
    bindPreview("skills", "preview-skills", "Python • Flask • SQL");
    bindPreview("edu_school", "preview-education", "Education details...");
    bindPreview("exp_company", "preview-experience", "Experience...");
    bindPreview("project_name", "preview-projects", "Projects...");

    /* SECTION SHOW/HIDE */
    $$(".section-toggle").forEach(toggle => {
        const section = document.getElementById(toggle.dataset.section);

        function updateSection() {
            if (!section) return;
            section.style.display = toggle.checked ? "block" : "none";
        }

        toggle.addEventListener("change", updateSection);
        updateSection();
    });

    /* TEMPLATE SELECTION */
    $$(".template-card").forEach(card => {
        card.addEventListener("click", () => {
            $$(".template-card").forEach(c => c.classList.remove("selected"));
            card.classList.add("selected");

            const radio = card.querySelector("input[type='radio']");
            if (radio) radio.checked = true;
        });
    });

    /* ADD/REMOVE DYNAMIC ITEMS */
    function enableAdd(containerId, itemClass, buttonId) {
        const container = document.getElementById(containerId);
        const button = document.getElementById(buttonId);

        if (!container || !button) return;

        button.addEventListener("click", () => {
            const firstItem = container.querySelector("." + itemClass);
            if (!firstItem) return;

            const clone = firstItem.cloneNode(true);
            clone.querySelectorAll("input, textarea").forEach(field => field.value = "");

            const remove = document.createElement("button");
            remove.type = "button";
            remove.className = "btn remove-btn";
            remove.textContent = "🗑 Remove";
            remove.addEventListener("click", () => clone.remove());

            clone.appendChild(remove);
            container.appendChild(clone);
        });
    }

    enableAdd("education-container", "education-item", "add-education");
    enableAdd("experience-container", "experience-item", "add-experience");
    enableAdd("projects-container", "project-item", "add-project");
    enableAdd("certifications-container", "certification-item", "add-certificate");

    /* AUTO TEXTAREA HEIGHT */
    $$("textarea").forEach(area => {
        function resize() {
            area.style.height = "auto";
            area.style.height = area.scrollHeight + "px";
        }

        area.addEventListener("input", resize);
        resize();
    });

    /* CHARACTER COUNTERS */
    $$("textarea,input[type='text']").forEach(field => {
        if (!field.maxLength || field.maxLength <= 0) return;

        const counter = document.createElement("small");
        counter.className = "char-counter";
        counter.style.display = "block";
        counter.style.marginTop = "5px";
        counter.style.color = "#64748b";
        field.parentNode.appendChild(counter);

        const updateCounter = () => {
            counter.textContent = `${field.value.length}/${field.maxLength}`;
        };

        field.addEventListener("input", updateCounter);
        updateCounter();
    });

    /* FORM PROGRESS */
    const form = document.querySelector("form");
    const progress = $("#form-progress");
    const progressText = $("#progress-text");

    if (form && progress) {
        const fields = form.querySelectorAll("input, textarea, select");

        function updateProgress() {
            let total = 0;
            let filled = 0;

            fields.forEach(field => {
                if (field.type === "checkbox" || field.type === "radio" || field.type === "file" || field.type === "hidden") return;

                total++;
                if (field.value.trim() !== "") filled++;
            });

            const percent = total ? Math.round((filled / total) * 100) : 0;
            progress.style.width = percent + "%";
            progress.textContent = percent + "%";

            if (progressText) {
                progressText.textContent = percent + "% Completed";
            }
        }

        fields.forEach(field => {
            field.addEventListener("input", updateProgress);
            field.addEventListener("change", updateProgress);
        });

        updateProgress();
    }

    /* LOCAL STORAGE AUTOSAVE */
    const resumeForm = document.querySelector(".resume-builder-form");

    if (resumeForm) {
        const storageKey = "nexthire_resume";

        function saveForm() {
            const formData = {};

            resumeForm.querySelectorAll("input, textarea, select").forEach(el => {
                if (!el.name || el.type === "file") return;

                if (el.type === "checkbox" || el.type === "radio") {
                    formData[el.name] = el.checked;
                } else {
                    formData[el.name] = el.value;
                }
            });

            localStorage.setItem(storageKey, JSON.stringify(formData));
        }

        function restoreForm() {
            const saved = localStorage.getItem(storageKey);
            if (!saved) return;

            try {
                const values = JSON.parse(saved);

                Object.keys(values).forEach(name => {
                    const fields = resumeForm.querySelectorAll(`[name="${name}"]`);

                    fields.forEach(field => {
                        if (field.type === "file") return;

                        if (field.type === "checkbox" || field.type === "radio") {
                            field.checked = Boolean(values[name]);
                        } else {
                            field.value = values[name];
                        }

                        field.dispatchEvent(new Event("input"));
                        field.dispatchEvent(new Event("change"));
                    });
                });
            } catch (err) {
                console.log("Unable to restore saved resume.");
            }
        }

        restoreForm();

        resumeForm.querySelectorAll("input, textarea, select").forEach(el => {
            el.addEventListener("input", saveForm);
            el.addEventListener("change", saveForm);
        });

        resumeForm.addEventListener("submit", () => {
            setTimeout(() => localStorage.removeItem(storageKey), 3000);
        });
    }

    /* FILE UPLOAD PREVIEW FOR ATS */
    $$("input[type='file']").forEach(input => {
        input.addEventListener("change", function () {
            if (!this.files.length) return;

            let info = this.parentNode.querySelector(".file-preview");
            if (!info) {
                info = document.createElement("p");
                info.className = "file-preview";
                this.parentNode.appendChild(info);
            }

            info.innerHTML = "📄 " + this.files[0].name;
        });
    });

    /* BUTTON LOADING */
    $$("form").forEach(currentForm => {
        currentForm.addEventListener("submit", (e) => {
            const invalid = currentForm.querySelector(":invalid");

            if (invalid) {
                e.preventDefault();
                invalid.focus({ preventScroll: true });
                invalid.scrollIntoView({ behavior: "smooth", block: "center" });
                return;
            }

            const btn = currentForm.querySelector("button[type='submit']");
            if (!btn) return;

            btn.disabled = true;
            btn.dataset.original = btn.innerHTML;
            btn.innerHTML = "⏳ Processing...";
        });
    });

    /* FADE ANIMATION */
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) entry.target.classList.add("fade");
        });
    }, { threshold: .15 });

    $$(".card,.builder-card,.feature-card,.upload-card,.result-card,.results-card,.counter,.suggestion-box,.ai-card,.template-card")
        .forEach(el => observer.observe(el));

    /* BACK TO TOP */
    const topBtn = document.createElement("button");
    topBtn.innerHTML = "⬆";
    topBtn.className = "back-top";
    document.body.appendChild(topBtn);

    window.addEventListener("scroll", () => {
        topBtn.style.display = window.scrollY > 500 ? "block" : "none";
    });

    topBtn.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    /* RIPPLE */
    $$(".btn").forEach(btn => {
        btn.addEventListener("click", function (e) {
            const ripple = document.createElement("span");
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);

            ripple.style.width = size + "px";
            ripple.style.height = size + "px";
            ripple.style.left = (e.clientX - rect.left - size / 2) + "px";
            ripple.style.top = (e.clientY - rect.top - size / 2) + "px";
            ripple.className = "ripple";

            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });

    /* CURRENT YEAR */
    const year = $("#current-year");
    if (year) year.textContent = new Date().getFullYear();
});
