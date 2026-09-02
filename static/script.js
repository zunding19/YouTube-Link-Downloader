const urlInput =
    document.getElementById("urlInput");

const downloadButton =
    document.getElementById("downloadButton");

const statusText =
    document.getElementById("status");


downloadButton.addEventListener(
    "click",
    async () => {

        const url =
            urlInput.value.trim();


        if (!url) {

            statusText.textContent =
                "Please enter a YouTube URL.";

            return;
        }


        downloadButton.disabled = true;

        downloadButton.textContent =
            "Downloading...";

        statusText.textContent =
            "Preparing video. This may take a moment...";


        try {

            const response =
                await fetch(
                    "/download",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            url: url
                        })
                    }
                );


            if (!response.ok) {

                let message =
                    "Unable to download video.";

                try {

                    const error =
                        await response.json();

                    if (error.detail) {
                        message =
                            error.detail;
                    }

                } catch (error) {
                }


                statusText.textContent =
                    message;

                return;
            }


            const blob =
                await response.blob();


            const downloadUrl =
                window.URL.createObjectURL(
                    blob
                );


            const link =
                document.createElement("a");


            link.href =
                downloadUrl;

            link.download =
                "youtube-video.mp4";


            document.body.appendChild(
                link
            );


            link.click();

            link.remove();


            window.URL.revokeObjectURL(
                downloadUrl
            );


            statusText.textContent =
                "Download started!";


        } catch (error) {

            console.error(error);

            statusText.textContent =
                "Could not connect to the server.";

        } finally {

            downloadButton.disabled =
                false;

            downloadButton.textContent =
                "Download";

        }

    }
);