const topicInput = document.getElementById("topicInput");
const runButton = document.getElementById("runButton");
const buttonLoader = document.getElementById("buttonLoader");
const statusText = document.getElementById("statusText");
const reportText = document.getElementById("reportText");
const searchText = document.getElementById("searchText");
const scrapeText = document.getElementById("scrapeText");
const feedbackText = document.getElementById("feedbackText");

function setLoading(isLoading) {
    runButton.disabled = isLoading;
    buttonLoader.classList.toggle("hidden", !isLoading);
    runButton.classList.toggle("loading", isLoading);
    statusText.innerText = isLoading ? "Launching research..." : "Ready to start.";
}

function formatOutput(text) {
    if (!text) return "No content available.";
    const escaped = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
    const linkPattern = /(https?:\/\/[^\s]+)/g;
    return escaped
        .replace(linkPattern, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>')
        .replace(/\n{2,}/g, "</p><p>")
        .replace(/\n/g, "<br/>");
}

async function postResearch(topic) {
    setLoading(true);
    statusText.innerText = "Running pipeline... this may take a moment.";
    reportText.innerHTML = "<p>Waiting for report output...</p>";
    searchText.innerHTML = "<p>Searching the web...</p>";
    scrapeText.innerHTML = "<p>Collecting page insights...</p>";
    feedbackText.innerHTML = "<p>Analyzing results...</p>";

    try {
        const response = await fetch("/api/research", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => null);
            throw new Error(errorData?.detail || `Server error ${response.status}`);
        }

        const data = await response.json();
        statusText.innerText = "Research completed successfully.";
        reportText.innerHTML = formatOutput(data.final_report ?? data.report ?? "No final report returned.");
        searchText.innerHTML = formatOutput(data.search_result ?? data.search ?? "No search result returned.");
        scrapeText.innerHTML = formatOutput(data.scraped_content ?? data.scrape ?? "No scraped content returned.");
        feedbackText.innerHTML = formatOutput(data.feedback ?? "No critic feedback returned.");
    } catch (error) {
        statusText.innerText = `Error: ${error.message}`;
        reportText.innerHTML = "<p>Unable to render report.</p>";
        searchText.innerHTML = "<p>No search preview available.</p>";
        scrapeText.innerHTML = "<p>No scraped content available.</p>";
        feedbackText.innerHTML = "<p>Feedback unavailable.</p>";
    } finally {
        setLoading(false);
    }
}

runButton.addEventListener("click", () => {
    const topic = topicInput.value.trim();
    if (!topic) {
        statusText.innerText = "Please enter a research topic to continue.";
        topicInput.focus();
        return;
    }
    postResearch(topic);
});

window.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && document.activeElement === topicInput) {
        runButton.click();
    }
});
