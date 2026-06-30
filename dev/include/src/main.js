window.addEventListener('scroll', trippy, { passive: true });
function trippy() {
    document.body.classList.toggle('not-trippy', document.documentElement.scrollTop > 300);
}

totop();
function totop() {
    const btn = document.getElementById("totop");
    if (!btn) return;
    btn.addEventListener("click", () => {
        window.scrollTo({top: 0, left: 0, behavior: "smooth"});
    });
}

const lazyBackgrounds = new IntersectionObserver((entries, observer) => {
  for (const entry of entries) {
    if (!entry.isIntersecting) continue;
    const el = entry.target;
    const url = el.dataset.bg;
    loadBackground(el, url);
    observer.unobserve(el);
  }
}, {rootMargin: "500px 0px"});
document.querySelectorAll("[data-bg]").forEach(el => {
  lazyBackgrounds.observe(el);
});

const bgCache = new Map();

function loadBackground(el, url) {
  if (bgCache.has(url)) {
    el.style.backgroundImage = url("${url}");
    return;
  }
  const img = new Image();
  img.decoding = "async";
  img.onload = () => {
    bgCache.set(url, true);
    el.style.backgroundImage = `url("${url}")`;
    img.onload = null;
  };
  img.onerror = () => {
    console.warn("Image failed to load:", url);
  };
  img.src = url;
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

document.querySelectorAll('#gallery section').forEach(section => {
  section.addEventListener('click', toggleSelf);
});

const lazyThumbs = new IntersectionObserver((entries, observer) => {
  for (const entry of entries) {
    if (!entry.isIntersecting) continue;
    const thumb = entry.target;
    const url = `/img/gallery/thumbnail/${thumb.dataset.name}_thumbnail.webp`;
    loadThumb(thumb, url);
    observer.unobserve(thumb);
  }
}, {rootMargin: "1000px 0px"});
document.querySelectorAll('.gallery a').forEach(el => {
  lazyThumbs.observe(el);
});

const thumbCache = new Map();

function loadThumb(el, url) {
  if (thumbCache.has(url)) {
    el.style.backgroundImage = url("${url}");
    return;
  }
  const img = new Image();
  img.decoding = "async";
  img.onload = () => {
    thumbCache.set(url, true);
    el.style.backgroundImage = `url("${url}")`;
    img.onload = null;
  };
  img.onerror = () => {
    console.warn("Failed to load thumbnail:", url);
  };
  img.src = url;
}

filterTag();

function filterTag() {
  let loc = window.location.toString();
  let splitted = loc.split('/tag/');
  if (splitted.length <= 1) {
    return;
  }
  let tag = splitted[1];
  let css = `.tag:not(.${tag}), #note {display: none} #current_tag {display: block}`,
    head = document.head,
    style = document.createElement('style');
  head.appendChild(style);
  style.appendChild(document.createTextNode(css));
  const el = document.body.querySelector('#tag_list a.' + tag),
    tagtitle = el.textContent,
    tagdesc = el.title;
  window.document.title = `${tagtitle} - ${window.document.title}`;
  head.querySelector('meta[name="description"]').setAttribute('content', tagdesc);
  head.querySelector('meta[property="og:title"]').setAttribute('content', window.document.title);
  head.querySelector('meta[property="og:description"]').setAttribute('content', tagdesc);
  head.querySelector('meta[property="og:url"]').setAttribute('content', loc);
  head.querySelector('meta[name="twitter:title"]').setAttribute('content', window.document.title);
  head.querySelector('meta[name="twitter:description"]').setAttribute('content', tagdesc);
  head.querySelector('link[rel="canonical"]').setAttribute('href', loc);
  const jsonLdScript = head.querySelector('script[type="application/ld+json"]');
  const data = JSON.parse(jsonLdScript.textContent);
  const imageGallery = data['@graph'].find(item => item['@type'] === 'ImageGallery');
  imageGallery['@id'] = loc + "#gallery";
  imageGallery.url = loc;
  imageGallery.name = `Galerie "${imageGallery.name}", filtrée avec le mot-clé "${tagtitle}"`;
  imageGallery.description = tagdesc;
  const webPage = data['@graph'].find(item => item['@type'] === 'WebPage');
  webPage['@id'] = loc + "#page";
  webPage.name = window.document.title;
  webPage.url = loc;
  webPage.mainEntity = {"@id": loc + "#gallery"}
  const breadcrumb = data['@graph'].find(item => item['@type'] === 'BreadcrumbList');
  breadcrumb['@id'] = loc + "#breadcrumb";
  breadcrumb.itemListElement.at(-1).item = splitted[0];
  breadcrumb.itemListElement.push({
      "@type": "ListItem",
      "position": breadcrumb.itemListElement.length + 1,
      "name": 'Mot-clé : ' + tagtitle
    });
  jsonLdScript.textContent = JSON.stringify(data, null, 2);
  document.body.querySelector('#current_tag span').textContent = tagtitle;
  const title = document.getElementById('main_title');
  title.textContent = tagtitle;
  title.dataset.text = tagtitle;
  document.body.querySelector('#page_title > p').innerHTML = tagdesc.replace('\n', '<br>');
  document.body.querySelector('header > nav > a:nth-child(2)').href = '../..';
  document.body.querySelectorAll('.tag:not(.' + tag + ')').forEach(a => { a.remove(); });
  document.body.querySelectorAll('.'+tag).forEach(t => {
    t.classList.add('current');
  });
}

function enlarge(el) {
  const m = document.body;
  m.classList.toggle('enlarged');
  psyche_origin();
  if (focusel) {
    focusel.scrollIntoView({behavior: "instant", block: "center"});
  }
  if (m.classList.contains('enlarged')) {
    el.textContent = '🐛';
    el.title = 'calmer la page';
    el.ariaLabel = "Basculer l'affichage de la page en largeur normale";
  } else {
    el.textContent = '🍆';
    el.title = 'élargir la page 👄';
    el.ariaLabel = "Basculer l'affichage de la page en pleine largeur";
  }
}

function toggleSections(el) {
  const m = document.body;
  m.classList.toggle('folded');
  if (el.getBoundingClientRect().top + window.pageYOffset > 180) {
    el.scrollIntoView({behavior: "instant", block: "start"});
    window.scrollBy({top:-25, behavior:"smooth"});
  }
}

function toggleSelf(el) {
  if (el.target.tagName === 'DIV') {
    toggleSections(el.target.children[0]);
  }
  if (el.target.tagName === 'H2') {
    toggleSections(el.target);
  }
}

let focusel;
let ticking = false;
let isResizing = false;
let oldwidth = window.innerWidth;

function updateFocusEl() {
  if (isResizing) return;
  if (ticking) return;
  ticking = true;
  requestAnimationFrame(() => {
    if (isResizing) {
      ticking = false;
      return;
    }
    focusel = document.elementFromPoint(window.innerWidth / 2, window.innerHeight / 2) || focusel;
    ticking = false;
  });
}

window.addEventListener('resize', () => {
  isResizing = true;
  if (focusel && oldwidth != window.innerWidth) {
    focusel.scrollIntoView({behavior: "instant", block: "center"});
    oldwidth = window.innerWidth;
  }
  clearTimeout(window.__resizeTimer);
  window.__resizeTimer = setTimeout(() => {
    isResizing = false;
  }, 200);
});

window.addEventListener('scroll', updateFocusEl, { passive: true });