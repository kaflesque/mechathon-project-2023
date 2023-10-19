document.addEventListener("DOMContentLoaded", function () {
    const cameraFeed = document.getElementById("camera-feed");
    const fullscreenButton = document.getElementById("fullscreen-button");
    const cameraContainer = document.querySelector(".camera-container");
    function toggleFullscreen() {
        if (!document.fullscreenElement) {
            if (cameraContainer.requestFullscreen) {
                document.querySelector("#camera-feed").style.height = "100%";
                document.querySelector("#camera-feed").style.width = "100%";
                cameraContainer.requestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
                document.querySelector("#camera-feed").style.height = "250px";
                document.querySelector("#camera-feed").style.width = "300px";
            }
        }
    }
    fullscreenButton.addEventListener("click", toggleFullscreen);
});
