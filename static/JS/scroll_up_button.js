var topBtn = document.getElementById("topBtn");

function toggleArrow() {
    topBtn.innerHTML = window.scrollY > 20 ? "↑" : "↓";
}

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: "smooth" });
}

function scrollToBottom() {
    window.scrollTo({ top: document.documentElement.scrollHeight, behavior: "smooth" });
}

window.addEventListener("scroll", toggleArrow);
topBtn.addEventListener("click", function () {
    if (topBtn.innerHTML === "↑") {
        scrollToTop();
    } else {
        scrollToBottom();
    }
});