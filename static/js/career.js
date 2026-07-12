document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("careerForm");

    form.addEventListener("submit", function (e) {

        e.preventDefault();

        const academic_score = document.getElementById("academic_score").value;
        const stream = document.getElementById("stream").value;
        const technical_skill = document.getElementById("technical_skill").value;
        const soft_skill = document.getElementById("soft_skill").value;
        const personality = document.getElementById("personality").value;
        const interest = document.getElementById("interest").value;
        const work_style = document.getElementById("work_style").value;

        fetch("/career-match", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                academic_score: academic_score,
                stream: stream,
                technical_skill: technical_skill,
                soft_skill: soft_skill,
                personality: personality,
                interest: interest,
                work_style: work_style
            })
        })
        .then(response => response.json())
        .then(data => {

            const resultBox = document.getElementById("recommendationCards");

            resultBox.innerHTML = "";

            if (data.recommendations.length > 0) {
                localStorage.setItem("predictedCareer", data.recommendations[0].career);
            }

            data.recommendations.forEach(function(item) {

                resultBox.innerHTML += `
                    <div class="career-card">
                    <div class="match-score">${item.match}% Match</div>

                    <h3>${item.career}</h3>

                    <p class="career-subtitle">Recommended based on your profile</p>

                    <div class="reason-box">
                    ${item.reason}
                    </div>

                <button class="details-btn">View Details</button>

                <button class="save-btn" onclick="saveCareer('${item.career}', '${item.match}')">
                   Save Career
                </button>
                </div>
                `;



            });

        })
        .catch(error => {
            console.error("Error:", error);
        });

    });

});

function saveCareer(career, match){
    let saved = JSON.parse(localStorage.getItem("savedCareers")) || [];

    saved.push({
        career: career,
        match: match,
        date: new Date().toLocaleDateString()
    });

    localStorage.setItem("savedCareers", JSON.stringify(saved));

    alert("Career saved successfully!");
}