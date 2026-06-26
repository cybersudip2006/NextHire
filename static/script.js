// Typing Animation Logic
const phrases = ["Get an Interview", "Get Hired", "Get Promoted", "Land Your Dream Job"];
let currentPhrase = 0; let letterIndex = 0; let isDeleting = false;
const typingElement = document.getElementById("typing-text");

function type() {
    if(!typingElement) return;
    const fullText = phrases[currentPhrase];
    
    if (isDeleting) {
        typingElement.innerText = fullText.substring(0, letterIndex - 1);
        letterIndex--;
    } else {
        typingElement.innerText = fullText.substring(0, letterIndex + 1);
        letterIndex++;
    }

    let typeSpeed = isDeleting ? 40 : 100;
    
    if (!isDeleting && letterIndex === fullText.length) {
        typeSpeed = 2000; // Pause at end of phrase
        isDeleting = true;
    } else if (isDeleting && letterIndex === 0) {
        isDeleting = false; 
        currentPhrase = (currentPhrase + 1) % phrases.length; 
        typeSpeed = 500; // Pause before next phrase
    }
    setTimeout(type, typeSpeed);
}

// Resume Counter Logic (1000 to 1200+)
const counterElement = document.getElementById("resume-counter");
function runCounter() {
    if(!counterElement) return;
    let count = 1000;
    const target = 1200;
    const interval = setInterval(() => {
        if(count >= target) {
            counterElement.innerText = target + "+";
            clearInterval(interval);
        } else {
            count += 3; // Speed increment
            counterElement.innerText = count;
        }
    }, 20);
}

document.addEventListener("DOMContentLoaded", () => {
    type();
    runCounter();
});

// Dynamic Phone & Country Code Validation
const countryData = {
    "IN": { code: "+91", len: 10 },
    "US": { code: "+1", len: 10 },
    "UK": { code: "+44", len: 10 }
};

const countrySelect = document.getElementById("country_select");
const phoneInput = document.getElementById("phone_input");
const hiddenCodeInput = document.getElementById("hidden_country_code");

if(countrySelect && phoneInput) {
    countrySelect.addEventListener("change", function() {
        const data = countryData[this.value];
        hiddenCodeInput.value = data.code;
        phoneInput.maxLength = data.len;
        phoneInput.placeholder = `Enter ${data.len} digits`;
        phoneInput.value = ""; // Clear on country change
    });
}