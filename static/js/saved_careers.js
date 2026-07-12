document.addEventListener("DOMContentLoaded", function () {
    const box = document.getElementById("savedCareersBox");
    const saved = JSON.parse(localStorage.getItem("savedCareers")) || [];

    if (saved.length === 0) {
        box.innerHTML = `<p>No saved careers yet.</p>`;
        return;
    }

    box.innerHTML = saved.map((item, index) => `
        <div class="saved-card">
            <h3>${item.career}</h3>
            <p>${item.match}% Match</p>
            <small>Saved on: ${item.date}</small>

            <button onclick="removeCareer(${index})">Remove</button>
        </div>
    `).join("");
});

function removeCareer(index){
    let saved = JSON.parse(localStorage.getItem("savedCareers")) || [];
    saved.splice(index, 1);
    localStorage.setItem("savedCareers", JSON.stringify(saved));
    location.reload();
}