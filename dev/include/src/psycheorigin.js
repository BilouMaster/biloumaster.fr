document.addEventListener('readystatechange', psyche_origin);
document.addEventListener('spa:load', psyche_origin);
window.addEventListener('resize', psyche_origin);
let tick = false;

function psyche_origin() {
    if (tick) return;
    tick = true;

    requestAnimationFrame(() => {
        let logo = document.getElementById('logo').getBoundingClientRect();
        let header = document.getElementsByTagName('header')[0].getBoundingClientRect();
        const angle = 1 * Math.PI / 180;
        const root_style = document.documentElement.style;
        root_style.setProperty('--biloufade_offset', Math.round((header.right - header.left) * Math.sin(angle)) + 'px');
        root_style.setProperty('--biloupsyche_left', Math.round((logo.left + logo.right) / 2 - header.left) + 'px');
        root_style.setProperty('--biloupsyche_top', Math.round((logo.top + logo.bottom) / 2 - header.top) + 'px');
        tick = false;
    });
}