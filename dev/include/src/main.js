document.addEventListener('readystatechange', psyche_origin);
window.addEventListener('resize', psyche_origin);
window.addEventListener('scroll', trippy, { passive: true });

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

function trippy() {
    document.body.classList.toggle('not-trippy', document.documentElement.scrollTop > 300);
}

// http://www.javascriptkit.com/dhtmltutors/sticky-hover-issue-solutions.shtml
(function(){
    var isTouch = false //var to indicate current input type (is touch versus no touch) 
    var isTouchTimer 
    var curRootClass = '' //var indicating current document root class ("can-touch" or "")
    function addtouchclass(e){
        clearTimeout(isTouchTimer)
        isTouch = true
        if (curRootClass != 'can-touch'){ //add "can-touch' class if it's not already present
            curRootClass = 'can-touch'
            document.documentElement.classList.add(curRootClass)
        }
        isTouchTimer = setTimeout(function(){isTouch = false}, 500) //maintain "istouch" state for 500ms so removetouchclass doesn't get fired immediately following a touch event
    }
    function removetouchclass(e){
        if (!isTouch && curRootClass == 'can-touch'){ //remove 'can-touch' class if not triggered by a touch event and class is present
            isTouch = false
            curRootClass = ''
            document.documentElement.classList.remove('can-touch')
        }
    }
    document.addEventListener('touchstart', addtouchclass, false) //this event only gets called when input type is touch
    document.addEventListener('mouseover', removetouchclass, false) //this event gets called when input type is everything from touch to mouse/ trackpad
})();

document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("totop");
    if (!btn) return;
    btn.addEventListener("click", () => {
        window.scrollTo({top: 0, left: 0, behavior: "smooth"});
    });
});