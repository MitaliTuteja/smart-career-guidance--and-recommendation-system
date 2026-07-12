document.addEventListener("DOMContentLoaded", function () {

    const chatBox = document.getElementById("chatBox");
    const userMessage = document.getElementById("userMessage");
    const sendBtn = document.getElementById("sendBtn");

    function addMessage(message, type){
        const div = document.createElement("div");
        div.className = type === "user" ? "user-message" : "bot-message";
        div.innerHTML = message;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function sendMessage(){
        const question = userMessage.value.trim();

        if(question === ""){
            return;
        }

        addMessage(question, "user");
        userMessage.value = "";

        const typingDiv = document.createElement("div");
        typingDiv.className = "bot-message typing";
        typingDiv.innerHTML = "AI Assistant is typing...";
        chatBox.appendChild(typingDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

        fetch("/ask-assistant", {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify({
               question: question,
               predictedCareer: localStorage.getItem("predictedCareer"),
               resumeATS: localStorage.getItem("resumeATS"),
               skillMatch: localStorage.getItem("skillMatch"),
               savedJobs: JSON.parse(localStorage.getItem("savedJobs") || "[]").length
            })
        })
        .then(response => response.json())
        .then(data => {
            setTimeout(() => {
                typingDiv.remove();
                addMessage(data.answer, "bot");
            }, 800);
        })
        .catch(error => {
            typingDiv.remove();
            addMessage("Sorry, something went wrong. Please try again.", "bot");
            console.error(error);
        });
    }

    sendBtn.addEventListener("click", sendMessage);

    userMessage.addEventListener("keypress", function(e){
        if(e.key === "Enter"){
            sendMessage();
        }
    });
});