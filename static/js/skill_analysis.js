document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("skillGapForm");
    const resultBox = document.getElementById("skillGapResult");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const target_career = document.getElementById("target_career").value;
        const current_technical_skill = document.getElementById("current_technical_skill").value;
        const current_soft_skill = document.getElementById("current_soft_skill").value;

        fetch("/analyze-skill-gap", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                target_career,
                current_technical_skill,
                current_soft_skill
            })
        })
        .then(response => response.json())
        .then(data => {

            if (data.error) {
                resultBox.innerHTML = `<p>${data.error}</p>`;
                return;
            }

            // Save Skill Match for Dashboard
            localStorage.setItem("skillMatch", data.match_score);

            resultBox.innerHTML = `

                <div class="skill-stats-grid">

                    <div class="score-card big-score">
                        <h3>Overall Match Score</h3>

                        <div class="circle-score">
                            <span>${data.match_score}%</span>
                        </div>

                    </div>

                    <div class="score-card">
                        <h2>${data.matched_count}</h2>
                        <p>Matched Skills</p>
                    </div>

                    <div class="score-card">
                        <h2>${data.missing_count}</h2>
                        <p>Missing Skills</p>
                    </div>

                    <div class="score-card">
                        <h2>${data.learning_count}</h2>
                        <p>Learning Skills</p>
                    </div>

                </div>


                <div class="analysis-grid">

                    <div class="analysis-card">

                        <h2>Skill Overview</h2>

                        ${data.skill_overview.map(item => `
                            <div class="skill-row">
                                <span>${item.skill}</span>

                                <strong class="${item.status.replaceAll(" ", "-").toLowerCase()}">

                                    ${item.status}

                                </strong>

                            </div>
                        `).join("")}

                    </div>


                    <div class="analysis-card">

                        <h2>Skill Match Analysis</h2>

                        <div class="radar-box">

                            <canvas id="skillRadarChart"></canvas>

                        </div>

                    </div>

                </div>



                <div class="comparison-card">

                    <h2>Skill Comparison Overview</h2>

                    ${data.skill_overview.map(item => {

                        let percent =
                            item.status === "Good" ? 85 :
                            item.status === "Moderate" ? 65 :
                            item.status === "Required Skill" ? 75 :
                            item.status === "Required Soft Skill" ? 70 :
                            45;

                        return `

                            <div class="progress-row">

                                <span>${item.skill}</span>

                                <div class="progress-track">

                                    <div class="progress-fill"
                                    style="width:${percent}%">

                                    </div>

                                </div>

                                <b>${percent}%</b>

                            </div>

                        `;

                    }).join("")}

                </div>


                <div class="bottom-grid">

                    <div class="analysis-card">

                        <h2>Missing Skills</h2>

                        <div class="tag-box">

                            ${data.missing_skills.length
                                ? data.missing_skills.map(skill => `
                                    <span>${skill}</span>
                                `).join("")
                                : "<span>No major skill gap</span>"}

                        </div>

                    </div>


                    <div class="analysis-card">

                        <h2>AI Recommendation</h2>

                        <p>${data.recommendation}</p>

                        <button class="plan-btn"
                        onclick="window.location.href='/learning-roadmap'">

                            Generate Learning Plan

                        </button>

                    </div>

                </div>

            `;

            // ==========================
            // CHART.JS RADAR CHART
            // ==========================

            const ctx = document.getElementById("skillRadarChart");

            new Chart(ctx, {

                type: "radar",

                data: {

                    labels: data.skill_overview.map(item => item.skill),

                    datasets: [

                        {

                            label: "Your Skills",

                            data: data.skill_overview.map(item =>
                                item.status === "Good" ? 85 :
                                item.status === "Moderate" ? 65 :
                                45
                            ),

                            borderColor: "#22d3ee",

                            backgroundColor: "rgba(34,211,238,0.25)",

                            pointBackgroundColor: "#22d3ee"

                        },

                        {

                            label: "Industry Requirement",

                            data: data.skill_overview.map(() => 90),

                            borderColor: "#7c3aed",

                            backgroundColor: "rgba(124,58,237,0.25)",

                            pointBackgroundColor: "#7c3aed"

                        }

                    ]

                },

                options: {

                    responsive: true,

                    plugins: {

                        legend: {

                            labels: {

                                color: "#ffffff"

                            }

                        }

                    },

                    scales: {

                        r: {

                            min: 0,

                            max: 100,

                            ticks: {

                                display: false

                            },

                            grid: {

                                color: "rgba(255,255,255,0.12)"

                            },

                            angleLines: {

                                color: "rgba(255,255,255,0.12)"

                            },

                            pointLabels: {

                                color: "#ffffff",

                                font: {

                                    size: 12

                                }

                            }

                        }

                    }

                }

            });

        })

        .catch(error => console.log(error));

    });

});