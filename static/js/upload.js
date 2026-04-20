const form = document.querySelector("form");
const modal = document.getElementById("successModal");
const closeBtn = document.getElementById("closeModal");

form.addEventListener("submit", function (e) {
    // Basic validation
    const title = form.title.value.trim();
    const description = form.description.value.trim();
    const tech_stack = form.tech_stack.value.trim();
    const github_link = form.github_link.value.trim();
    const live_link = form.live_link.value.trim();

    if (title && description && department) {
        modal.classList.add("active");
        form.reset();
    } else {
        alert("Please fill all required fields.");
    }
});

closeBtn.addEventListener("click", () => {
    modal.classList.remove("active");
});