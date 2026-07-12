document.addEventListener("DOMContentLoaded", function () {
    const predictedCareer = localStorage.getItem("predictedCareer") || "Not Predicted";
    const resumeATS = localStorage.getItem("resumeATS") || "--";
    const skillMatch = localStorage.getItem("skillMatch") || "--";
    const savedJobs = JSON.parse(localStorage.getItem("savedJobs")) || [];

    document.getElementById("dashCareer").innerText = predictedCareer;
    document.getElementById("dashATS").innerText = resumeATS === "--" ? "--%" : resumeATS + "%";
    document.getElementById("dashSkill").innerText = skillMatch === "--" ? "--%" : skillMatch + "%";
    document.getElementById("dashJobs").innerText = savedJobs.length;

    document.getElementById("latestCareer").innerText = predictedCareer;
    document.getElementById("latestATS").innerText = resumeATS === "--" ? "--%" : resumeATS + "%";
    document.getElementById("latestSkill").innerText = skillMatch === "--" ? "--%" : skillMatch + "%";
    document.getElementById("latestJobs").innerText = savedJobs.length;
});