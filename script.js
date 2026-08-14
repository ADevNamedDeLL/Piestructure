const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll(".feature-card, .step, .usage-panel, .closing").forEach((el) => {
  el.classList.add("reveal");
  observer.observe(el);
});

const terminal = document.querySelector(".terminal");
if (terminal && window.matchMedia("(pointer:fine)").matches) {
  terminal.addEventListener("mousemove", (e) => {
    const r = terminal.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    terminal.style.transform = `rotateY(${x * -4}deg) rotateX(${y * 3}deg)`;
  });
  terminal.addEventListener("mouseleave", () => {
    terminal.style.transform = "rotateY(0deg) rotateX(0deg)";
  });
}
