const urlInput = document.getElementById("urlInput");
const checkUrlButton = document.getElementById("checkUrlButton");
const urlResult = document.getElementById("urlResult");


function analyzeURL() {

    const rawURL = urlInput.value.trim();

    urlResult.replaceChildren();

    if (!rawURL) {
        urlResult.textContent = "Please enter a URL.";
        urlResult.className = "alert alert-warning mt-4";
        return;
    }

    let parsedURL;

    try {
        parsedURL = new URL(rawURL);
    } catch {
        urlResult.textContent =
            "Invalid URL. Include a valid domain, such as https://example.com.";

        urlResult.className = "alert alert-danger mt-4";
        return;
    }

    const hostname = parsedURL.hostname.toLowerCase();

    const indicators = [];

    if (!["http:", "https:"].includes(parsedURL.protocol)) {
        indicators.push("URL uses an unusual or unsupported protocol.");
    }

    if (parsedURL.protocol === "http:") {
        indicators.push("URL does not use HTTPS encryption.");
    }

    if (rawURL.includes("@")) {
        indicators.push("URL contains an @ symbol, which can obscure the destination.");
    }

    if (rawURL.length > 100) {
        indicators.push("URL is unusually long.");
    }

    if (hostname.split(".").length > 4) {
        indicators.push("Domain contains several subdomains.");
    }

    if (/^\d{1,3}(\.\d{1,3}){3}$/.test(hostname)) {
        indicators.push("URL uses an IP address instead of a domain name.");
    }

    if (hostname.startsWith("xn--") || hostname.includes(".xn--")) {
        indicators.push("Domain contains an internationalized/punycode label.");
    }

    const shorteners = [
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "is.gd",
        "cutt.ly",
        "shorturl.at"
    ];

    if (shorteners.includes(hostname)) {
        indicators.push("URL uses a known URL shortening service.");
    }

    if (parsedURL.port && !["80", "443"].includes(parsedURL.port)) {
        indicators.push("URL uses a non-standard web port.");
    }

    const suspiciousWords = [
        "login",
        "verify",
        "account",
        "update",
        "password",
        "secure",
        "banking"
    ];

    const urlContent = (
        hostname + parsedURL.pathname + parsedURL.search
    ).toLowerCase();

    if (suspiciousWords.some(word => urlContent.includes(word))) {
        indicators.push("URL contains words sometimes used in phishing lures.");
    }

    let heading;
    let resultClass;

    if (indicators.length >= 3) {
        heading = "Multiple suspicious indicators found";
        resultClass = "danger";
    } else if (indicators.length > 0) {
        heading = "Some suspicious indicators found";
        resultClass = "warning";
    } else {
        heading = "No basic suspicious indicators detected";
        resultClass = "success";
    }

    const headingElement = document.createElement("h5");
    headingElement.textContent = heading;

    const list = document.createElement("ul");

    indicators.forEach(indicator => {
        const item = document.createElement("li");
        item.textContent = indicator;
        list.appendChild(item);
    });

    if (indicators.length === 0) {
        const item = document.createElement("li");
        item.textContent =
            "This basic check did not identify any of its listed warning signs.";
        list.appendChild(item);
    }

    const note = document.createElement("p");
    note.className = "mb-0 mt-3";
    note.textContent =
        "This result is not a safety verdict. A phishing website can have none of these indicators, and a legitimate URL can trigger warnings.";

    urlResult.className = `alert alert-${resultClass} mt-4`;
    urlResult.append(headingElement, list, note);

}


checkUrlButton.addEventListener("click", analyzeURL);

urlInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        analyzeURL();
    }
});