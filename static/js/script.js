document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    if (chatForm) {
        chatForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const input = document.getElementById("user-input");
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: input.value })
            });
            const data = await response.json();
            alert(data.reply); // À remplacer par un affichage plus élégant
        });
    }
});