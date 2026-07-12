document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("resumeForm");
    const resultBox = document.getElementById("resumeResult");
    const resumeInput = document.getElementById("resumeFile");
    const uploadStatus = document.getElementById("uploadStatus");
    const analyzeBtn = document.getElementById("analyzeBtn");

    resumeInput.addEventListener("change", function () {
        if (resumeInput.files.length > 0) {
            uploadStatus.innerHTML = `
                <div class="upload-success">
                    <strong>Uploaded Resume</strong><br>
                    ${resumeInput.files[0].name}<br>
                    <span>✓ Successfully Selected</span>
                </div>
            `;
        } else {
            uploadStatus.innerHTML = "";
        }
    });

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const file = resumeInput.files[0];

        if (!file) {
            alert("Please upload a resume first.");
            return;
        }

        analyzeBtn.innerHTML = `<span class="spinner"></span> Analyzing...`;
        analyzeBtn.disabled = true;

        const formData = new FormData();
        formData.append("resume", file);

        fetch("/analyze-resume", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {

            setTimeout(() => {

                analyzeBtn.innerHTML = "Analyze Resume";
                analyzeBtn.disabled = false;

                if (data.error) {
                    resultBox.innerHTML = `<p>${data.error}</p>`;
                    return;
                }

                localStorage.setItem("resumeATS", data.ats_score);

                let atsClass = "";

                if (data.ats_score >= 95) {
                    atsClass = "ats-green";
                } else if (data.ats_score >= 70) {
                    atsClass = "ats-blue";
                } else if (data.ats_score >= 50) {
                    atsClass = "ats-orange";
                } else {
                    atsClass = "ats-red";
                }

                uploadStatus.innerHTML = `
                    <div class="upload-success">
                        <strong>Uploaded Resume</strong><br>
                        ${file.name}<br>
                        <span>✓ Successfully Analyzed</span>
                    </div>
                `;

                resultBox.innerHTML = `
                    <div class="stats-grid">
                        <div class="stat-card">

                            <h2 class="${atsClass}">
                                 ${data.ats_score}%
                            </h2>

                        <div class="ats-badge ${atsClass}">
                           ${
                                data.ats_score >= 95
                                    ? "Excellent Resume"
                                    : data.ats_score >= 70
                                    ? "Good Resume"
                                    : data.ats_score >= 50
                                    ? "Needs Improvement"
                                    : "Poor ATS Score"
                            }
                        </div>

                        <p>ATS Score</p>

                    </div>

                        <div class="stat-card">
                            <h2>${data.skills_found}</h2>
                            <p>Skills Found</p>
                        </div>

                        <div class="stat-card">
                            <h2>${data.missing_count}</h2>
                            <p>Missing Skills</p>
                        </div>

                        <div class="stat-card">
                            <h2>${data.career_match}%</h2>
                            <p>Career Match</p>
                        </div>
                    </div>

                    <div class="resume-grid">
                        <div class="result-card">
                            <h2>Detected Skills</h2>
                            <div class="tag-box">
                                ${data.detected_skills.length ? data.detected_skills.map(skill => `
                                    <span>${skill}</span>
                                `).join("") : "<span>No skills detected</span>"}
                            </div>
                        </div>

                        <div class="result-card">
                           <h2>Missing Skills</h2>

                           <div class="priority-box">
                              ${data.missing_skills.length ? data.missing_skills.map((skill, index) => `
                               <div class="priority-row">
                                    <span>${skill}</span>
                                    <small class="${index === 0 ? 'high-priority' : 'medium-priority'}">
                                       ${index === 0 ? 'High Priority' : 'Medium Priority'}
                                    </small>
                                </div>
                              `).join("") : "<span>No major missing skills</span>"}
                            </div>
                        </div>
                    </div>

                    <div class="result-card">
                        <h2>AI Recommendations</h2>
                        <ul class="recommend-list">
                            ${data.recommendations.map(item => `<li>${item}</li>`).join("")}
                        </ul>
                    </div>

                    <div class="career-path-card">
                        <h2>Recommended Career Path</h2>

                        <h1>${data.predicted_career}</h1>

                        <p>
                           ${data.recommendation_text}
                         </p>
                    </div>
                `;

            }, 2000);
        })
        .catch(error => {
            console.error("Error:", error);
            analyzeBtn.innerHTML = "Analyze Resume";
            analyzeBtn.disabled = false;
            resultBox.innerHTML = `<p>Something went wrong while analyzing resume.</p>`;
        });
    });
});