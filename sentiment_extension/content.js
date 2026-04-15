document.addEventListener("mouseup", async () => {
  const selectedText = window.getSelection().toString().trim();
  if (selectedText.length > 0) {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/sentiment/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: selectedText }),
      });

      const data = await response.json();
      if (data.sentiment) showPopup(data.sentiment);
    } catch (err) {
      console.error("Error fetching sentiment:", err);
    }
  }
});

function showPopup(sentiment) {
  // --- Popup box ---
  const popup = document.createElement("div");
  popup.innerText = `Sentiment: ${sentiment}`;
  popup.style.position = "fixed";
  popup.style.bottom = "20px";
  popup.style.right = "20px";
  popup.style.backgroundColor =
    sentiment === "Positive" ? "#d4edda" : "#f8d7da";
  popup.style.color = sentiment === "Positive" ? "#155724" : "#721c24";
  popup.style.padding = "14px 24px";
  popup.style.borderRadius = "12px";
  popup.style.boxShadow = "0 0 12px rgba(0,0,0,0.3)";
  popup.style.zIndex = "9999";
  popup.style.fontWeight = "bold";
  popup.style.fontSize = "16px";
  popup.style.transition = "opacity 0.5s";
  document.body.appendChild(popup);

  // --- Floating emojis ---
  const emojis =
    sentiment === "Positive"
      ? ["😊", "🌸", "💖", "✨", "👍"]
      : ["😔", "💭", "👎", "💧", "😢"];
  for (let i = 0; i < 10; i++) {
    createEmoji(emojis[Math.floor(Math.random() * emojis.length)]);
  }

  // Remove popup after 5 seconds
  setTimeout(() => {
    popup.style.opacity = "0";
    setTimeout(() => popup.remove(), 500);
  }, 5000);
}

function createEmoji(emoji) {
  const el = document.createElement("div");
  el.textContent = emoji;
  el.style.position = "fixed";
  el.style.bottom = "0";
  el.style.left = Math.random() * window.innerWidth + "px";
  el.style.fontSize = Math.random() * 24 + 24 + "px";
  el.style.opacity = "0.9";
  el.style.zIndex = "9999";
  document.body.appendChild(el);

  const duration = 4000 + Math.random() * 2000;
  const finalY = window.innerHeight - 200 - Math.random() * 200;
  const animation = el.animate(
    [
      { transform: "translateY(0)", opacity: 1 },
      { transform: `translateY(-${finalY}px)`, opacity: 0 },
    ],
    { duration, easing: "ease-out" }
  );

  animation.onfinish = () => el.remove();
}
