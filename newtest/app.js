document.addEventListener("DOMContentLoaded", () => {

    const sidebar = document.getElementById("chatbotSidebar");
    const openBtn = document.getElementById("openSidebarBtn");
    const headerLogo = document.getElementById("headerLogo");

    const homePage = document.getElementById("homePage");
    const searchScreen = document.getElementById("searchScreen");
    const chatView = document.getElementById("chatView");

    const queryInput = document.getElementById("queryInput");
    const alarmInput = document.getElementById("alarmInput");
    const chatInput = document.getElementById("chatInput");
    const resultTab = document.getElementById("resultTab");

    /* ---------------- HOME MODE ---------------- */
    function enableHomeMode() {
        document.body.classList.add("home-active");
        sidebar.classList.add("is-hidden");
        openBtn.classList.remove("show");
        headerLogo.classList.remove("show");
    }

    function disableHomeMode() {
        document.body.classList.remove("home-active");
        openBtn.classList.add("show");
        headerLogo.classList.add("show");
    }

    /* ---------------- Sidebar ---------------- */
    window.openSidebar = () => {
        sidebar.classList.remove("is-hidden");
        openBtn.classList.remove("show");
        headerLogo.classList.remove("show");
    };

    window.closeSidebar = () => {
        sidebar.classList.add("is-hidden");
        openBtn.classList.add("show");
        headerLogo.classList.add("show");
    };

    /* ---------------- Navigation ---------------- */
window.goHome = () => {
    enableHomeMode();

    homePage.style.display = "flex";
    searchScreen.style.display = "none";
    chatView.style.display = "none";
    recentPage.style.display = "none";

    // Clear inputs & chat
    queryInput.value = "";
    alarmInput.value = "";
    chatInput.value = "";
    resultTab.innerHTML = "";

    sidebar.classList.add("is-hidden");
};



window.startConversationFromHome = () => {
    disableHomeMode();

    homePage.style.display = "none";
    searchScreen.style.display = "flex";
    chatView.style.display = "none";
    recentPage.style.display = "none";
};

    /* ---------------- Chat ---------------- */
window.startChat = () => {
    const q = queryInput.value.trim();
    const a = alarmInput.value.trim();
    if (!q && !a) return;

    disableHomeMode();

    homePage.style.display = "none";
    searchScreen.style.display = "none";
    recentPage.style.display = "none";
    chatView.style.display = "flex";

    addMessage(q || `Alarm Code: ${a}`, "user");
    fakeBot(a || q);

    queryInput.value = "";
    alarmInput.value = "";
};


    window.sendMessage = () => {
        const text = chatInput.value.trim();
        if (!text) return;

        addMessage(text, "user");
        chatInput.value = "";
        fakeBot(text);
    };

    /* ✅ Enter key support (ONLY ONCE) */
    chatInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    function addMessage(text, type) {
        const div = document.createElement("div");
        div.className = `chat ${type}`;
        div.textContent = text;
        resultTab.appendChild(div);
        resultTab.scrollTop = resultTab.scrollHeight;
    }

window.callBackend = async function (userText) {
    try {
        const response = await fetch("http://127.0.0.1:22169/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: userText })
        });

        const data = await response.json();
        return data.answer;
    } catch (err) {
        console.error(err);
        return "Server error. Please try again.";
    }
};

window.fakeBot = async function (text) {
    const typingDiv = document.createElement("div");
    typingDiv.className = "chat bot";
    typingDiv.textContent = "Typing...";
    resultTab.appendChild(typingDiv);
    resultTab.scrollTop = resultTab.scrollHeight;

    const reply = await window.callBackend(text);
    typingDiv.textContent = reply;
};


    /* ---------------- Recent ---------------- */
window.showRecent = () => {
    disableHomeMode();

    // Show ONLY recent page
    homePage.style.display = "none";
    searchScreen.style.display = "none";
    chatView.style.display = "none";
    recentPage.style.display = "flex";

    // Sidebar visible
    sidebar.classList.remove("is-hidden");
    openBtn.classList.add("show");
};



    /* Init */
    enableHomeMode();
});