const prev = document.body.querySelector('#arrows > a[rel="prev"]')
const next = document.body.querySelector('#arrows > a[rel="next"]')
const image = document.body.querySelector('.img_container img')

document.addEventListener("keydown", (event) => {
    switch (event.code) {
        case "ArrowLeft":
            if (prev) {
                event.preventDefault();
                prev.click();
            }
            break;

        case "ArrowRight":
            if (next) {
                event.preventDefault();
                next.click();
            }
            break;
    }
});