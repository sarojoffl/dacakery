document.addEventListener("DOMContentLoaded", () => {
  const counters = document.querySelectorAll(".counter");
  const speed = 200;

  const animateCounter = (counter) => {
    counter.classList.add("animate"); // for CSS effect if any

    const countNum = counter.querySelector(".count-num");
    if (!countNum) return;

    const updateCount = () => {
      const target = +counter.getAttribute("data-target");
      const current = +countNum.innerText || 0;
      const increment = Math.ceil(target / speed);

      if (current < target) {
        countNum.innerText = current + increment > target ? target : current + increment;
        setTimeout(updateCount, 10);
      } else {
        countNum.innerText = target;
      }
    };

    updateCount();
  };

  const observer = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.5,
    }
  );

  counters.forEach((counter) => {
    observer.observe(counter);
  });
});
