const angle = 0.5 * Math.PI / 180

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

window.addEventListener("scroll", function() {
    if (document.documentElement.scrollTop > 300) {
        document.getElementById("totop").style.display = 'block';
    } else {
        document.getElementById("totop").style.display = 'none';
    }
}, { passive: true });

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