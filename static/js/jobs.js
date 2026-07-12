document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("jobForm");
    const jobsResult = document.getElementById("jobsResult");
    const careerDropdown = document.getElementById("target_career");

    const savedCareer = localStorage.getItem("predictedCareer");

    if (savedCareer) {
        careerDropdown.value = savedCareer;
        loadJobs(savedCareer);
    }

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const target_career = careerDropdown.value;
        loadJobs(target_career);
    });

    function loadJobs(target_career) {
        fetch("/recommend-jobs", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                target_career: target_career
            })
        })
        .then(response => response.json())
        .then(data => {

            jobsResult.innerHTML = "";

            data.jobs.forEach(job => {

                jobsResult.innerHTML += `
                    <div class="job-card">

                        <div class="job-title">${job.title}</div>

                        <div class="company">${job.company}</div>

                        <div class="info">
                            <span>💰 ${job.salary}</span>
                            <span>📍 ${job.location}</span>
                        </div>

                        <div class="match">
                            ★★★★★ ${job.match}% Match
                        </div>

                        <h4>Required Skills</h4>

                        <div class="skills">
                            ${job.skills.map(skill => `<span>${skill}</span>`).join("")}
                        </div>

                        <div class="button-group">
                            <button class="apply-btn" onclick="applyJob('${job.title}', '${job.company}')">
                               🔗 Apply on Company Website
                            </button>

                            <button class="save-btn" onclick="saveJob('${job.title}', '${job.company}', '${job.salary}', '${job.location}', '${job.match}')">
                                Save Job
                            </button>
                        </div>

                    </div>
                `;

            });

        })
        .catch(error => {
            console.error("Error:", error);
            jobsResult.innerHTML = `<p>Unable to load job recommendations.</p>`;
        });
    }

});

function applyJob(title, company) {

    let url = "";

    switch (company.toLowerCase()) {

        case "google":
            url = "https://careers.google.com/jobs/results/";
            break;

        case "microsoft":
            url = "https://jobs.careers.microsoft.com/";
            break;

        case "amazon":
            url = "https://www.amazon.jobs/";
            break;

        case "infosys":
            url = "https://career.infosys.com/";
            break;

        case "tcs":
            url = "https://www.tcs.com/careers";
            break;

        case "wipro":
            url = "https://careers.wipro.com/";
            break;

        case "accenture":
            url = "https://www.accenture.com/in-en/careers";
            break;

        case "cognizant":
            url = "https://careers.cognizant.com/";
            break;

        default:
            url = "https://www.google.com/search?q=" +
                  encodeURIComponent(company + " Careers");
    }

    window.open(url, "_blank");

}

function saveJob(title, company, salary, location, match) {

    let savedJobs = JSON.parse(localStorage.getItem("savedJobs")) || [];

    savedJobs.push({
        title: title,
        company: company,
        salary: salary,
        location: location,
        match: match,
        date: new Date().toLocaleDateString()
    });

    localStorage.setItem("savedJobs", JSON.stringify(savedJobs));

    alert("Job saved successfully!");
}