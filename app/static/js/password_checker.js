const passwordInput = document.getElementById("passwordInput");
const showPassword = document.getElementById("showPassword");

const strengthText = document.getElementById("strengthText");
const strengthBar = document.getElementById("strengthBar");
const passwordMessage = document.getElementById("passwordMessage");

const requirements = {
    length: document.getElementById("lengthCheck"),
    uppercase: document.getElementById("uppercaseCheck"),
    lowercase: document.getElementById("lowercaseCheck"),
    number: document.getElementById("numberCheck"),
    special: document.getElementById("specialCheck")
};


function updateRequirement(element, passed) {
    element.classList.toggle("requirement-passed", passed);
    element.classList.toggle("requirement-failed", !passed);

    const originalText = element.textContent.replace(/^[✓✗]\s*/, "");

    element.textContent = `${passed ? "✓" : "✗"} ${originalText}`;
}


function checkPassword() {

    const password = passwordInput.value;

    if (!password) {
        strengthText.textContent = "Not checked";
        strengthBar.style.width = "0%";
        passwordMessage.textContent = "";

        Object.values(requirements).forEach(element => {
            element.classList.remove(
                "requirement-passed",
                "requirement-failed"
            );

            element.textContent = element.textContent.replace(/^[✓✗]\s*/, "");
        });

        return;
    }

    const checks = {
        length: password.length >= 8,
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        number: /[0-9]/.test(password),
        special: /[^A-Za-z0-9]/.test(password)
    };

    Object.keys(checks).forEach(key => {
        updateRequirement(requirements[key], checks[key]);
    });

    const score = Object.values(checks).filter(Boolean).length;

    let strength;
    let percentage;

    if (score <= 2) {
        strength = "Weak";
        percentage = 25;
    } else if (score <= 4) {
        strength = "Medium";
        percentage = 65;
    } else {
        strength = "Strong";
        percentage = 100;
    }

    strengthText.textContent = strength;
    strengthBar.style.width = `${percentage}%`;

    passwordMessage.textContent =
        strength === "Weak"
            ? "Your password needs improvement."
            : strength === "Medium"
                ? "Good start! Consider meeting all requirements."
                : "All listed requirements are satisfied.";

    passwordMessage.className =
        strength === "Weak"
            ? "text-danger mt-3"
            : strength === "Medium"
                ? "text-warning mt-3"
                : "text-success mt-3";

}


passwordInput.addEventListener("input", checkPassword);


showPassword.addEventListener("change", function () {
    passwordInput.type = this.checked ? "text" : "password";
});