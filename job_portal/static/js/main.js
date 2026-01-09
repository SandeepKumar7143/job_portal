// Simple animation on scroll
window.addEventListener("scroll", () => {
    document.querySelectorAll(".step-box").forEach(box => {
        const position = box.getBoundingClientRect().top;
        if (position < window.innerHeight - 100) {
            box.style.transform = "translateY(0)";
            box.style.opacity = "1";
        }
    });
});
