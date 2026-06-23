document.addEventListener('DOMContentLoaded', main_init);
document.addEventListener('spa:load', main_init);
window.addEventListener('scroll', trippy, { passive: true });

function main_init() {
    totop();
    const bgObserver = new IntersectionObserver((entries) => {
    for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        const el = entry.target;
        const bg = el.dataset.bg;
        if (bg) {
        el.style.backgroundImage = `url("${bg}")`;
        el.removeAttribute("data-bg");
        }
        bgObserver.unobserve(el);
    }
    }, {
        rootMargin: "200px"
    });
    document.querySelectorAll("*[data-bg]").forEach(el => {
        bgObserver.observe(el);
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

function totop() {
    const btn = document.getElementById("totop");
    if (!btn) return;
    btn.addEventListener("click", () => {
        window.scrollTo({top: 0, left: 0, behavior: "smooth"});
    });
}