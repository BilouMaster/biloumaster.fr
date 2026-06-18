document.addEventListener("keydown", (event) => {
    const prev = document.body.querySelector('#arrows > a[rel="prev"]')
    const next = document.body.querySelector('#arrows > a[rel="next"]')

    switch (event.code) {
        case "ArrowLeft":
            if (prev) {
                prev.click();
            }
            break;

        case "ArrowRight":
            if (next) {
                next.click();
            }
            break;
    }
});