const angle = 1 * Math.PI / 180

function psyche_origin() {
    let logo = document.getElementById('logo').getBoundingClientRect();
    let root_style = document.documentElement.style;
    let psyche_left
    let psyche_top
    if (window.getComputedStyle(document.querySelector('body > header')).position == 'sticky') {
        psyche_left = Math.round((logo.left + logo.right) / 2) + 'px';
        psyche_top = Math.round((logo.top + logo.bottom) / 2) + 'px';
    } else {
        let buddy = document.body.getBoundingClientRect();
        let offset = Math.round((buddy.right - buddy.left) * Math.sin(angle)) + 'px';
        psyche_left = Math.round((logo.left + logo.right) / 2 - buddy.left) + 'px';
        psyche_top = Math.round((logo.top + logo.bottom) / 2 - buddy.top) + 'px';
        root_style.setProperty('--biloufade_offset', offset);
    }
    root_style.setProperty('--biloupsyche_left', psyche_left);
    root_style.setProperty('--biloupsyche_top', psyche_top);
}

function zoom_img(img) {
    fig = document.getElementsByTagName('figure')[0]
    if (fig.classList.contains('zoomed')) {
        fig.classList.remove('zoomed');
    } else {
        fig.classList.add('zoomed');
    }
}

window.addEventListener('resize', psyche_origin);

/*function docReady(fn) {
    if (document.readyState === "complete" || document.readyState === "interactive") {
        fn;
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}*/
/*function reduc_coef() {
    if (document.documentElement.clientWidth < 720)
        return;
    let w = 720;
    let h = document.documentElement.clientHeight;
    let rcw = w / (w + h * Math.sin(angle));
    let rch = h / (h + w * Math.sin(angle));
    document.documentElement.style.setProperty('--bilourcw', rcw);
    document.documentElement.style.setProperty('--bilourch', rch);
}*/
/*docReady(function() {
    setTimeout(psyche_origin, 1);
})*/
/*document.addEventListener("DOMContentLoaded", function(){*/