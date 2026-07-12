document.addEventListener("DOMContentLoaded", function () {

    const savedJobsBox = document.getElementById("savedJobsBox");

    let savedJobs = JSON.parse(localStorage.getItem("savedJobs")) || [];

    if (savedJobs.length === 0) {

        savedJobsBox.innerHTML = `
            <div class="empty-box">
                <h2>No Saved Jobs</h2>
                <p>Save jobs from the Job Recommendation page.</p>
            </div>
        `;

        return;
    }

    renderJobs();

    function renderJobs() {

        savedJobsBox.innerHTML = "";

        savedJobs.forEach((job, index) => {

            savedJobsBox.innerHTML += `

                <div class="saved-card">

                    <h2>${job.title}</h2>

                    <div class="company">${job.company}</div>

                    <div class="job-info">
                        <span>${job.location}</span>
                        <span>${job.salary}</span>
                    </div>

                    <div class="match">
                        ⭐ ${job.match}% Match
                    </div>

                    <div class="button-group">

                        <button class="open-btn"
                            onclick="openCompany('${job.company}')">

                            Apply

                        </button>

                        <button class="remove-btn"
                            onclick="removeJob(${index})">

                            Remove

                        </button>

                    </div>

                </div>

            `;
        });

    }

    window.removeJob = function(index){

        savedJobs.splice(index,1);

        localStorage.setItem(
            "savedJobs",
            JSON.stringify(savedJobs)
        );

        location.reload();

    }

    window.openCompany = function(company){

        let url="";

        switch(company.toLowerCase()){

            case "google":
                url="https://careers.google.com/jobs/results/";
                break;

            case "microsoft":
                url="https://jobs.careers.microsoft.com/";
                break;

            case "amazon":
                url="https://www.amazon.jobs/";
                break;

            case "infosys":
                url="https://career.infosys.com/";
                break;

            case "tcs":
                url="https://www.tcs.com/careers";
                break;

            case "accenture":
                url="https://www.accenture.com/in-en/careers";
                break;

            default:
                url="https://www.google.com/search?q="+company+" careers";

        }

        window.open(url,"_blank");

    }

});