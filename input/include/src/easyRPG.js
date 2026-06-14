window.document.addEventListener('isPlaying', zoomEasyRPG, false);
window.document.addEventListener('exitFS', exitFS, false);
const easyRPG = document.getElementById("easyRPG");
function zoomEasyRPG() {
    const immersiveCheck = setInterval(immersive, 300);
    easyRPG.scrollIntoView({behavior: "smooth", block: "start"});
    easyRPG.classList.add("playing");
}
function exitFS() {
    easyRPG.scrollIntoView({behavior: "instant", block: "start"});
}
function immersive() {
    if (Math.abs(easyRPG.getBoundingClientRect().y) < 200) {
        document.documentElement.classList.add("immersive");
        easyRPG.scrollIntoView({behavior: "smooth", block: "start"});
        easyRPG.focus();
    } else {
        document.documentElement.classList.remove("immersive");
    }
}