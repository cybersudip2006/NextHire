/* ===========================================================
   NextHire Professional JavaScript
   Part 1
=========================================================== */

document.addEventListener("DOMContentLoaded", () => {

/* ==========================================
   MOBILE NAVBAR
========================================== */

const menuBtn = document.querySelector(".menu-toggle");
const nav = document.querySelector("nav");

if(menuBtn && nav){

menuBtn.addEventListener("click",()=>{

nav.classList.toggle("show");

menuBtn.innerHTML=
nav.classList.contains("show") ? "✕" : "☰";

});

document.querySelectorAll("nav a").forEach(link=>{

link.onclick=()=>{

nav.classList.remove("show");
menuBtn.innerHTML="☰";

};

});

document.addEventListener("click",(e)=>{

if(!nav.contains(e.target) &&
!menuBtn.contains(e.target)){

nav.classList.remove("show");
menuBtn.innerHTML="☰";

}

});

window.addEventListener("resize",()=>{

if(window.innerWidth>768){

nav.classList.remove("show");
menuBtn.innerHTML="☰";

}

});

}

/* ==========================================
   HERO TYPING ANIMATION
========================================== */

const typing=document.getElementById("typing-text");

const phrases=[

"Get an Interview",

"Get Hired",

"Land Your Dream Job",

"Beat ATS Filters",

"Build Your Career",

"Create ATS Friendly Resume",

"Stand Out From Recruiters"

];

let phrase=0;
let letter=0;
let deleting=false;

function typeAnimation(){

if(!typing) return;

const current=phrases[phrase];

if(!deleting){

typing.textContent=current.substring(0,letter+1);

letter++;

if(letter===current.length){

deleting=true;

setTimeout(typeAnimation,1800);

return;

}

}else{

typing.textContent=current.substring(0,letter-1);

letter--;

if(letter===0){

deleting=false;

phrase++;

if(phrase>=phrases.length)
phrase=0;

}

}

setTimeout(typeAnimation,deleting?45:90);

}

typeAnimation();

/* ==========================================
   RESUME COUNTER
========================================== */

const counter=document.getElementById("resume-counter");

if(counter){

let value=1000;

const target=1250;

const timer=setInterval(()=>{

value++;

counter.textContent=value+"+";

if(value>=target){

clearInterval(timer);

setTimeout(()=>{

counter.textContent="1250+";

},1500);

}

},40);

}

/* ==========================================
   PHONE VALIDATION
========================================== */

const countryData={

IN:{code:"+91",len:10},

US:{code:"+1",len:10},

UK:{code:"+44",len:10},

CA:{code:"+1",len:10},

AU:{code:"+61",len:9}

};

const country=document.getElementById("country_select");
const phone=document.getElementById("phone_input");
const hidden=document.getElementById("hidden_country_code");

if(country && phone && hidden){

function updatePhone(){

const data=countryData[country.value];

if(!data) return;

hidden.value=data.code;

phone.maxLength=data.len;

phone.placeholder=`Enter ${data.len} digit phone number`;

phone.value="";

}

updatePhone();

country.addEventListener("change",updatePhone);

}

/* ==========================================
   PROFILE PHOTO PREVIEW
========================================== */

const imageInput=document.getElementById("profile_photo");

const preview=document.getElementById("photo-preview");

if(imageInput && preview){

imageInput.addEventListener("change",function(){

const file=this.files[0];

if(!file) return;

const reader=new FileReader();

reader.onload=function(e){

preview.src=e.target.result;

preview.style.display="block";

};

reader.readAsDataURL(file);

});

}

/* ==========================================
   FILE NAME PREVIEW
========================================== */

document.querySelectorAll("input[type=file]").forEach(input=>{

input.addEventListener("change",function(){

if(!this.files.length) return;

let info=this.parentNode.querySelector(".file-preview");

if(!info){

info=document.createElement("p");

info.className="file-preview";

this.parentNode.appendChild(info);

}

info.innerHTML="📄 "+this.files[0].name;

});

});

/* ==========================================
   AUTO TEXTAREA HEIGHT
========================================== */

document.querySelectorAll("textarea").forEach(area=>{

function resize(){

area.style.height="auto";

area.style.height=area.scrollHeight+"px";

}

area.addEventListener("input",resize);

resize();

});

/* ==========================================
   FADE ANIMATION
========================================== */

const observer=new IntersectionObserver((entries)=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

entry.target.classList.add("fade");

}

});

},{
threshold:.15
});

document.querySelectorAll(

".card,.builder-card,.feature-card,.upload-card,.result-card,.counter,.suggestion-box"

).forEach(el=>observer.observe(el));

});
/* ==========================================
   LIVE RESUME PREVIEW
========================================== */

const bindPreview = (inputId, previewId, fallback = "") => {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);

    if (!input || !preview) return;

    const update = () => {
        preview.textContent = input.value.trim() || fallback;
    };

    input.addEventListener("input", update);
    update();
};

bindPreview("name", "preview-name", "Your Name");
bindPreview("email", "preview-email", "your@email.com");
bindPreview("phone_input", "preview-phone", "+91 XXXXXXXXXX");
bindPreview("address", "preview-address", "Your Address");
bindPreview("objective", "preview-objective", "Professional Summary");
bindPreview("skills", "preview-skills", "Python • Java • SQL");
bindPreview("edu_school", "preview-education", "Education");
bindPreview("exp_company", "preview-experience", "Experience");
bindPreview("project_name", "preview-projects", "Projects");

/* ==========================================
   CHARACTER COUNTERS
========================================== */

document.querySelectorAll("textarea,input[type='text']").forEach(field => {

    if (!field.maxLength || field.maxLength <= 0) return;

    const counter = document.createElement("small");

    counter.className = "char-counter";

    counter.style.display = "block";
    counter.style.marginTop = "5px";
    counter.style.color = "#64748b";

    field.parentNode.appendChild(counter);

    const updateCounter = () => {
        counter.textContent =
            `${field.value.length}/${field.maxLength}`;
    };

    field.addEventListener("input", updateCounter);

    updateCounter();

});

/* ==========================================
   AUTO SAVE FORM
========================================== */

const resumeForm = document.querySelector("form");

if (resumeForm) {

    const saveForm = () => {

        const formData = {};

        resumeForm.querySelectorAll("input, textarea, select")
            .forEach(el => {

                if (
                    el.type !== "password" &&
                    el.type !== "file"
                ) {

                    formData[el.name] = el.value;

                }

            });

        localStorage.setItem(
            "nexthire_resume",
            JSON.stringify(formData)
        );

    };

    resumeForm.querySelectorAll("input, textarea, select")
        .forEach(el => {

            el.addEventListener("input", saveForm);
            el.addEventListener("change", saveForm);

        });

}

/* ==========================================
   RESTORE SAVED FORM
========================================== */

const savedData =
    localStorage.getItem("nexthire_resume");

if (savedData && resumeForm) {

    try {

        const values = JSON.parse(savedData);

        Object.keys(values).forEach(key => {

            const field =
                resumeForm.querySelector(`[name="${key}"]`);

            if (field && field.type !== "file") {

                field.value = values[key];

                field.dispatchEvent(
                    new Event("input")
                );

            }

        });

    } catch (err) {

        console.log("No saved resume.");

    }

}

/* ==========================================
   CLEAR SAVED DATA AFTER DOWNLOAD
========================================== */

resumeForm?.addEventListener("submit", () => {

    setTimeout(() => {

        localStorage.removeItem("nexthire_resume");

    }, 3000);

});

/* ==========================================
   INPUT ANIMATION
========================================== */

document.querySelectorAll("input,textarea,select")
.forEach(el => {

    el.addEventListener("focus", () => {

        el.parentNode.classList.add("active-field");

    });

    el.addEventListener("blur", () => {

        el.parentNode.classList.remove("active-field");

    });

});

/* ==========================================
   SMOOTH BUTTON HOVER
========================================== */

document.querySelectorAll(".btn")
.forEach(btn => {

    btn.addEventListener("mouseenter", () => {

        btn.style.transform = "translateY(-3px) scale(1.02)";

    });

    btn.addEventListener("mouseleave", () => {

        btn.style.transform = "";

    });

});
/* ==========================================
   DYNAMIC SECTION SHOW / HIDE
========================================== */

const sectionMap = {

    include_education: "education-section",

    include_experience: "experience-section",

    include_projects: "project-section",

    include_skills: "skills-section",

    include_certifications: "certification-section",

    include_languages: "language-section",

    include_achievements: "achievement-section",

    include_publications: "publication-section",

    include_hobbies: "interest-section",

    include_references: "reference-section"

};

Object.keys(sectionMap).forEach(name=>{

    const checkbox=document.querySelector(`input[name="${name}"]`);

    const section=document.getElementById(sectionMap[name]);

    if(!checkbox || !section) return;

    function toggle(){

        section.style.display=
        checkbox.checked ? "block":"none";

    }

    toggle();

    checkbox.addEventListener("change",toggle);

});

/* ==========================================
   DUPLICATE CARD FUNCTION
========================================== */

function enableDuplicate(sectionId){

    const section=document.getElementById(sectionId);

    if(!section) return;

    const btn=section.querySelector(".add-btn");

    if(!btn) return;

    btn.addEventListener("click",()=>{

        const clone=section.cloneNode(true);

        clone.removeAttribute("id");

        clone.classList.add("duplicate-card");

        const add=clone.querySelector(".add-btn");

        if(add){

            add.remove();

        }

        const remove=document.createElement("button");

        remove.type="button";

        remove.className="btn";

        remove.style.marginTop="15px";

        remove.style.background="#dc2626";

        remove.innerHTML="🗑 Remove";

        remove.onclick=()=>{

            clone.remove();

        };

        clone.appendChild(remove);

        section.parentNode.insertBefore(

            clone,

            btn.parentNode.nextSibling

        );

    });

}

enableDuplicate("education-section");

enableDuplicate("experience-section");

enableDuplicate("project-section");

enableDuplicate("certification-section");

/* ==========================================
   TEMPLATE CARD SELECTION
========================================== */

document.querySelectorAll(".template-card")

.forEach(card=>{

    card.addEventListener("click",()=>{

        document.querySelectorAll(".template-card")

        .forEach(c=>c.classList.remove("selected"));

        card.classList.add("selected");

        const radio=card.querySelector("input");

        if(radio){

            radio.checked=true;

        }

    });

});

/* ==========================================
   SMOOTH SCROLL TO FIRST ERROR
========================================== */

const form=document.querySelector("form");

if(form){

form.addEventListener("submit",function(e){

const invalid=form.querySelector(":invalid");

if(invalid){

e.preventDefault();

invalid.focus({

preventScroll:true

});

invalid.scrollIntoView({

behavior:"smooth",

block:"center"

});

}

});

}

/* ==========================================
   HIGHLIGHT ACTIVE INPUT
========================================== */

document.querySelectorAll(

"input,textarea,select"

).forEach(input=>{

input.addEventListener("focus",()=>{

input.style.borderColor="#2563eb";

input.style.boxShadow="0 0 0 4px rgba(37,99,235,.15)";

});

input.addEventListener("blur",()=>{

input.style.borderColor="";

input.style.boxShadow="";

});

});

/* ==========================================
   FORM PROGRESS BAR
========================================== */

const progress=document.getElementById("form-progress");

if(progress && form){

const fields=form.querySelectorAll(

"input,textarea,select"

);

function updateProgress(){

let filled=0;

fields.forEach(field=>{

if(field.type==="checkbox") return;

if(field.type==="file") return;

if(field.value.trim()!==""){

filled++;

}

});

const percent=Math.round(

(filled/fields.length)*100

);

progress.style.width=percent+"%";

progress.innerHTML=percent+"%";

}

fields.forEach(field=>{

field.addEventListener("input",updateProgress);

});

updateProgress();

}

/* ==========================================
   SUCCESS ANIMATION
========================================== */

document.querySelectorAll(".btn")

.forEach(btn=>{

btn.addEventListener("click",()=>{

btn.classList.add("clicked");

setTimeout(()=>{

btn.classList.remove("clicked");

},250);

});

});
/* ==========================================
   DRAG & DROP PROFILE PHOTO
========================================== */

const uploadBox = document.querySelector(".image-upload");
const profileInput = document.getElementById("profile_photo");
const previewImage = document.getElementById("photo-preview");

if (uploadBox && profileInput) {

    uploadBox.addEventListener("click", () => profileInput.click());

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

        const reader = new FileReader();

        reader.onload = function(event){

            if(previewImage){

                previewImage.src = event.target.result;
                previewImage.style.display = "block";

            }

        };

        reader.readAsDataURL(e.dataTransfer.files[0]);

    });

}

/* ==========================================
   LIVE PREVIEW UPDATE
========================================== */

const previewMap = {

    name:["name","preview-name"],

    email:["email","preview-email"],

    objective:["objective","preview-objective"],

    skills:["skills","preview-skills"],

    edu_school:["edu_school","preview-education"],

    exp_company:["exp_company","preview-experience"],

    project_name:["project_name","preview-projects"]

};

Object.values(previewMap).forEach(item=>{

    const input=document.getElementById(item[0]);

    const preview=document.getElementById(item[1]);

    if(!input || !preview) return;

    const update=()=>{

        preview.textContent=input.value || preview.textContent;

    };

    input.addEventListener("input",update);

    update();

});

/* ==========================================
   BUTTON LOADING
========================================== */

document.querySelectorAll("form").forEach(form=>{

form.addEventListener("submit",()=>{

const btn=form.querySelector("button[type='submit']");

if(!btn) return;

btn.disabled=true;

btn.dataset.original=btn.innerHTML;

btn.innerHTML="⏳ Generating Resume...";

});

});

/* ==========================================
   BACK TO TOP BUTTON
========================================== */

const topBtn=document.createElement("button");

topBtn.innerHTML="⬆";

topBtn.className="back-top";

document.body.appendChild(topBtn);

window.addEventListener("scroll",()=>{

topBtn.style.display=

window.scrollY>500 ? "block":"none";

});

topBtn.onclick=()=>{

window.scrollTo({

top:0,

behavior:"smooth"

});

};

/* ==========================================
   BUTTON RIPPLE EFFECT
========================================== */

document.querySelectorAll(".btn").forEach(btn=>{

btn.addEventListener("click",function(e){

const ripple=document.createElement("span");

const rect=this.getBoundingClientRect();

const size=Math.max(rect.width,rect.height);

ripple.style.width=size+"px";
ripple.style.height=size+"px";

ripple.style.left=(e.clientX-rect.left-size/2)+"px";

ripple.style.top=(e.clientY-rect.top-size/2)+"px";

ripple.className="ripple";

this.appendChild(ripple);

setTimeout(()=>{

ripple.remove();

},600);

});

});

/* ==========================================
   FAKE LOADING BAR
========================================== */

const loader=document.getElementById("loading-bar");

if(loader){

let width=0;

const timer=setInterval(()=>{

width+=2;

loader.style.width=width+"%";

if(width>=100){

clearInterval(timer);

}

},30);

}

/* ==========================================
   COPY EMAIL
========================================== */

document.querySelectorAll(".copy-email").forEach(btn=>{

btn.addEventListener("click",()=>{

navigator.clipboard.writeText(btn.dataset.email);

btn.innerHTML="Copied!";

setTimeout(()=>{

btn.innerHTML="Copy";

},1500);

});

});

/* ==========================================
   CURRENT YEAR
========================================== */

const year=document.getElementById("current-year");

if(year){

year.innerHTML=new Date().getFullYear();

}

/* ==========================================
   PREVENT DOUBLE SUBMIT
========================================== */

let submitted=false;

document.querySelectorAll("form").forEach(form=>{

form.addEventListener("submit",e=>{

if(submitted){

e.preventDefault();

return;

}

submitted=true;

});

});
/* ======================================================
   DYNAMIC RESUME SECTIONS
====================================================== */

document.querySelectorAll(".section-toggle").forEach(toggle => {

    toggle.addEventListener("change", function(){

        const section =
        document.getElementById(this.dataset.section);

        if(!section) return;

        section.style.display =
        this.checked ? "block" : "none";

    });

});

/* ==========================================
   END
========================================== */
