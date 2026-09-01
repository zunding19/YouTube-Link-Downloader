const urlInput = document.getElementById("urlInput");

const downloadButton =
    document.getElementById("downloadButton");

const statusText =
    document.getElementById("status");


downloadButton.addEventListener("click", async () => {

    const url = urlInput.value;


    if (!url) {

        statusText.textContent =
            "Please enter a YouTube URL.";

        return;

    }


    statusText.textContent =
        "Downloading...";


    const response = await fetch("/download", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            url: url
        })

    });


    const data = await response.json();


    if (response.ok) {

        statusText.textContent =
            data.message;

    } else {

        statusText.textContent =
            data.detail;

    }

});