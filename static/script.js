const anonymousCheck = document.getElementById("anonymousCheck");
const personalDetails = document.getElementById("personalDetails");

if (anonymousCheck) {
  anonymousCheck.addEventListener("change", function () {
    if (this.checked) {
      personalDetails.style.opacity = "0";
      personalDetails.style.transform = "translateY(-10px)";

      setTimeout(() => {
        personalDetails.style.display = "none";
      }, 250);
    } else {
      personalDetails.style.display = "block";

      setTimeout(() => {
        personalDetails.style.opacity = "1";
        personalDetails.style.transform = "translateY(0)";
      }, 50);
    }
  });
}

// Scroll reveal animation
const revealElements = document.querySelectorAll(".card, .form-box, table");

const revealOnScroll = () => {
  revealElements.forEach((element) => {
    const top = element.getBoundingClientRect().top;
    const windowHeight = window.innerHeight;

    if (top < windowHeight - 80) {
      element.classList.add("active");
    }
  });
};

window.addEventListener("scroll", revealOnScroll);
window.addEventListener("load", revealOnScroll);