document.addEventListener("DOMContentLoaded", () => {

    const sidebar = document.getElementById("chatbotSidebar");
    const openBtn = document.getElementById("openSidebarBtn");
    const headerLogo = document.getElementById("headerLogo");

    const homePage = document.getElementById("homePage");
    const searchScreen = document.getElementById("searchScreen");
    const chatView = document.getElementById("chatView");
    const recentPage = document.getElementById("recentPage");

    const queryInput = document.getElementById("queryInput");
    const alarmInput = document.getElementById("alarmInput");
    const chatInput = document.getElementById("chatInput");
    const resultTab = document.getElementById("resultTab");

    /* ---------------- Utilities ---------------- */
    function resetConversation() {
        queryInput.value = "";
        alarmInput.value = "";
        chatInput.value = "";
        resultTab.innerHTML = "";
    }

    function saveToRecent(text) {
        let recents = JSON.parse(localStorage.getItem("recentChats")) || [];

        recents = recents.filter(item => item.text !== text);

        recents.unshift({
            text,
            time: new Date().toLocaleTimeString()
        });

        localStorage.setItem("recentChats", JSON.stringify(recents.slice(0, 10)));
    }

    function loadRecentChats() {
        const list = document.getElementById("recentChatsList");
        list.innerHTML = "";

        const recents = JSON.parse(localStorage.getItem("recentChats")) || [];

        if (!recents.length) {
            list.innerHTML = "<p>No recent conversations</p>";
            return;
        }

        recents.forEach(item => {
            const div = document.createElement("div");
            div.className = "recent-chat-item";
            div.innerHTML = `<strong>${item.text}</strong><p>${item.time}</p>`;
            div.onclick = () => openRecentChat(item.text);
            list.appendChild(div);
        });
    }

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
    headerLogo.style.display = "none";   // 👈 hide logo
};

window.closeSidebar = () => {
    sidebar.classList.add("is-hidden");
    headerLogo.style.display = "";       // 👈 restore default
};


    /* ---------------- Navigation ---------------- */
    window.goHome = () => {
        enableHomeMode();
        homePage.style.display = "flex";
        searchScreen.style.display = "none";
        chatView.style.display = "none";
        recentPage.style.display = "none";
        resetConversation();
    };

    window.startConversationFromHome = () => {
        resetConversation();
        disableHomeMode();
        homePage.style.display = "none";
        searchScreen.style.display = "flex";
        chatView.style.display = "none";
        recentPage.style.display = "none";
    };

    /* ---------------- Chat ---------------- */
    window.startChat = () => {
        const userText = alarmInput.value.trim() || queryInput.value.trim();
        if (!userText) return;

        saveToRecent(userText);

        disableHomeMode();
        homePage.style.display = "none";
        searchScreen.style.display = "none";
        recentPage.style.display = "none";
        chatView.style.display = "flex";

        addMessage(userText, "user");
        fakeBot(userText);

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

   chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();

        // ✅ Only send message if chat screen is visible
        if (chatView.style.display === "flex") {
            sendMessage();
        }
    }
});


    function addMessage(text, type) {
        const div = document.createElement("div");
        div.className = `chat ${type}`;
        div.textContent = text;
        resultTab.appendChild(div);
        resultTab.scrollTop = resultTab.scrollHeight;
    }

    async function fakeBot(text) {
        const typing = document.createElement("div");
        typing.className = "chat bot";
        typing.textContent = "Loading...";
        resultTab.appendChild(typing);

        const res = await fetch("http://127.0.0.1:22169/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: text })
        });

        const data = await res.json();
        typing.textContent = data.answer;
    }

    /* ---------------- Recent ---------------- */
    window.showRecent = () => {
        disableHomeMode();
        homePage.style.display = "none";
        searchScreen.style.display = "none";
        chatView.style.display = "none";
        recentPage.style.display = "flex";
        loadRecentChats();
    };

    window.openRecentChat = (text) => {
        resetConversation();
        disableHomeMode();
        recentPage.style.display = "none";
        chatView.style.display = "flex";
        addMessage(text, "user");
        fakeBot(text);
    };

    enableHomeMode();
});

window.clearRecentChats = () => {
    if (!confirm("Clear all recent conversations?")) return;

    // Clear storage
    localStorage.removeItem("recentChats");

    // Refresh recent UI immediately
    loadRecentChats();

    // Optional: force reflow for safety (helps in some browsers)
    const list = document.getElementById("recentChatsList");
    list.scrollTop = 0;
};

[queryInput, alarmInput].forEach(input => {
    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            startChat();
        }
    });
});
