document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("roadmapForm");
    const resultBox = document.getElementById("roadmapResult");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const target_career = document.getElementById("target_career").value;

        fetch("/generate-roadmap", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ target_career })
        })
        .then(response => response.json())
        .then(data => {

            if (data.error) {
                resultBox.innerHTML = `<p>${data.error}</p>`;
                return;
            }

            resultBox.innerHTML = `
                <div class="summary-grid">
                    <div class="summary-card">
                        <h2>${data.readiness_score}%</h2>
                        <p>Career Readiness</p>
                    </div>

                    <div class="summary-card">
                        <h2>${data.courses.length}</h2>
                        <p>Courses</p>
                    </div>

                    <div class="summary-card">
                        <h2>${data.certifications.length}</h2>
                        <p>Certifications</p>
                    </div>

                    <div class="summary-card">
                        <h2>${data.projects.length}</h2>
                        <p>Projects</p>
                    </div>
                </div>

                <div class="roadmap-card">
                    <h2>${data.career} Career Roadmap</h2>

                    <div class="roadmap-item completed">
                        <span></span>
                        <div>
                            <h3>${data.required_technical} Fundamentals</h3>
                            <p>Completed / Core Skill</p>
                        </div>
                    </div>

                    <div class="roadmap-item progress">
                        <span></span>
                        <div>
                            <h3>${data.interest}</h3>
                            <p>In Progress</p>
                        </div>
                    </div>

                    <div class="roadmap-item upcoming">
                        <span></span>
                        <div>
                            <h3>${data.required_soft}</h3>
                            <p>Upcoming Soft Skill Development</p>
                        </div>
                    </div>

                    <div class="roadmap-item upcoming">
                        <span></span>
                        <div>
                            <h3>Portfolio & Interview Preparation</h3>
                            <p>Upcoming</p>
                        </div>
                    </div>
                </div>

                <h2 class="resource-title">Recommended Learning Resources</h2>

                <div class="resource-grid">
                    ${data.courses.map(course => `
                        <div class="resource-card">
                            <h3>${course}</h3>
                            <p>Online Learning</p>
                            <button>Start Course</button>
                        </div>
                    `).join("")}
                </div>
            `;
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
});