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
        "Preparing download...";


    try {

        const response = await fetch("/download", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                url: url
            })

        });


        if (!response.ok) {

            const error = await response.json();

            statusText.textContent =
                error.detail;

            return;
        }


        const blob = await response.blob();


        const downloadUrl =
            window.URL.createObjectURL(blob);


        const link =
            document.createElement("a");


        link.href = downloadUrl;

        link.download = "youtube-video.mp4";


        document.body.appendChild(link);

        link.click();


        link.remove();

        window.URL.revokeObjectURL(downloadUrl);


        statusText.textContent =
            "Download started!";


    } catch (error) {

        statusText.textContent =
            "Something went wrong.";

    }

});