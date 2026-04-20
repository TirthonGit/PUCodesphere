const searchInput = document.getElementById("searchInput");
const cards = document.querySelectorAll(".project-card");

searchInput.addEventListener("keyup", function () {
    const searchValue = this.value.toLowerCase();

    cards.forEach(card => {
        const text = card.innerText.toLowerCase();
        if (text.includes(searchValue)) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
});