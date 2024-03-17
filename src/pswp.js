import PhotoSwipeLightbox from '/pswp/photoswipe-lightbox.esm.min.js';
import PhotoSwipe from '/pswp/photoswipe.esm.min.js';

const fullscreenAPI = getFullscreenAPI();
// const shareSVG      = '<svg aria-hidden="true" class="pswp__icn" viewBox="0 0 32 32" width="32" height="32"><use class="pswp__icn-shadow" xlink:href="#pswp__icn-share"/><path id="pswp__icn-share" d="m25.333 2a4.6667 4.6667 0 0 0-4.6667 4.6667 4.6667 4.6667 0 0 0 0.10938 0.97526l-10.596 5.2979a4.6667 4.6667 0 0 0-3.5137-1.6064 4.6667 4.6667 0 0 0-4.6667 4.6667 4.6667 4.6667 0 0 0 4.6667 4.6667 4.6667 4.6667 0 0 0 3.5159-1.6042l10.589 5.2956a4.6667 4.6667 0 0 0-0.10482 0.97526 4.6667 4.6667 0 0 0 4.6667 4.6667 4.6667 4.6667 0 0 0 4.6667-4.6667 4.6667 4.6667 0 0 0-4.6667-4.6667 4.6667 4.6667 0 0 0-3.516 1.6042l-10.589-5.2956a4.6667 4.6667 0 0 0 0.10482-0.97526 4.6667 4.6667 0 0 0-0.10938-0.97298l10.596-5.2979a4.6667 4.6667 0 0 0 3.5137 1.6042 4.6667 4.6667 0 0 0 4.6667-4.6667 4.6667 4.6667 0 0 0-4.6667-4.6667z"/></svg>'
const fullscreenSVG = '<svg aria-hidden="true" class="pswp__icn" viewBox="0 0 32 32" width="32" height="32"><use class="pswp__icn-shadow" xlink:href="#pswp__icn-fullscreen-exit"/><use class="pswp__icn-shadow" xlink:href="#pswp__icn-fullscreen-request"/><path d="M8 8v6.047h2.834v-3.213h3.213V8h-3.213zm9.953 0v2.834h3.213v3.213H24V8h-2.834zM8 17.953V24h6.047v-2.834h-3.213v-3.213zm13.166 0v3.213h-3.213V24H24v-6.047z" id="pswp__icn-fullscreen-request"/><path d="M11.213 8v3.213H8v2.834h6.047V8zm6.74 0v6.047H24v-2.834h-3.213V8zM8 17.953v2.834h3.213V24h2.834v-6.047h-2.834zm9.953 0V24h2.834v-3.213H24v-2.834h-3.213z" id="pswp__icn-fullscreen-exit" style="display:none"/></svg>';
const arrowPrevSVG  = '<svg aria-hidden="true" class="pswp__icn" viewBox="0 0 32 32" width="32" height="32"><use class="pswp__icn-shadow" xlink:href="#pswp__icn-arrow"/><g id="pswp__icn-arrow"><path d="m13.954 31.466c3.4105-3.9122 1.5044-6.2452-4.2804-9.6874-5.785-3.4424-6.1055-8.2702 0-11.592 6.1053-3.322 8.3219-5.8972 4.2804-9.6874-2.0207-1.8952-4.7613 1.9728-7.7468 5.472-2.9854 3.499-6.2157 6.6292-6.2076 10.011 0.015311 3.382 3.2225 6.623 6.2828 10.137 3.0603 3.5144 5.9664 7.302 7.6716 5.346z" /><path d="m19.875 16a3.875 3.875 0 0 1-3.8593 3.875 3.875 3.875 0 0 1-3.8905-3.8437 3.875 3.875 0 0 1 3.8279-3.906 3.875 3.875 0 0 1 3.9215 3.8121"/></g></svg>';
const arrowNextSVG = arrowPrevSVG;

let options = {
  gallery: 'body',
  children: '.gallery > a',
  thumbSelector: '.gallery > a',
  pswpModule: PhotoSwipe,
  showAnimationDuration: 333,
  hideAnimationDuration: 180,
  bgOpacity: 0.8,
  spacing: 0.05,
  paddingTop: 100,
  paddingBottom: 150,
  preload: [4, 4],
  loop: false,
  zoom: false,
  counter: false,
  wheelToZoom: true,
  returnFocus: true,
  closeTitle: 'Fermer',
  arrowPrevTitle: 'Précédent',
  arrowNextTitle: 'Suivant',
  arrowPrevSVG: arrowPrevSVG,
  arrowNextSVG: arrowNextSVG,
  errorMsg: 'Mince, il y a un petit souci avec cette image...',
  easing: 'cubic-bezier(0.4, 1, 0.6, 0.9)',
  tapAction: (point, originalEvent) => {
    if (!document.elementFromPoint(point.x, point.y).classList.contains('pswp__no-toggle')) {
      pswp.element.classList.toggle('pswp--ui-visible');
    }
  },
  initialZoomLevel: (zoomLevelObject) => {
    return Math.min(4, zoomLevelObject.panAreaSize.x / zoomLevelObject.elementSize.x, zoomLevelObject.panAreaSize.y / zoomLevelObject.elementSize.y);
  },
  maxZoomLevel: (zoomLevelObject) => {
    return Math.max(1, 4 * Math.min(4, zoomLevelObject.panAreaSize.x / zoomLevelObject.elementSize.x, zoomLevelObject.panAreaSize.y / zoomLevelObject.elementSize.y));
  }
};

const lightbox = new PhotoSwipeLightbox(options);

lightbox.addFilter('domItemData', (itemData, element, linkEl) => {
  if (linkEl) {
    const sizeAttr = linkEl.style.getPropertyValue('--r');
    itemData.src = '/img/gallery/' + linkEl.dataset.name + '.webp';
    itemData.w = itemData.width = Number(sizeAttr.split('/')[0]);
    itemData.h = itemData.height = Number(sizeAttr.split('/')[1]);
    itemData.msrc = linkEl.style.backgroundImage.split('"')[1];
    itemData.thumbCropped = false;
  }
  return itemData;
});

lightbox.addFilter('thumbBounds', (thumbBounds, itemData, index) => {
  const thumbRect = itemData.element.getBoundingClientRect();
  const realWidth = itemData.w*thumbRect.height/itemData.h;
  return {
    x: thumbRect.left + (thumbRect.width - realWidth)/2,
    y: thumbRect.top,
    w: realWidth
  };
});

// from @rbndelrio https://github.com/dimsemenov/PhotoSwipe/issues/1765#issuecomment-934010548 (thank you!)
const customGoTo = (index, animate = false) => {
  const ctx = lightbox.pswp;
  index = ctx.getLoopedIndex(index);
  const indexChanged = ctx.mainScroll.moveIndexBy(index - ctx.potentialIndex, animate);

  if (indexChanged) {
    ctx.dispatch('afterGoto');
  }
}
lightbox.on('uiRegister', () => {
  lightbox.pswp.next = () => customGoTo(lightbox.pswp.potentialIndex + 1, true);
  lightbox.pswp.prev = () => customGoTo(lightbox.pswp.potentialIndex - 1, true);
});
//

lightbox.on('uiRegister', function() {
  if (fullscreenAPI) {
    lightbox.pswp.ui.registerElement({
      name: 'fullscreen-button',
      title: 'Plein écran (activer/désactiver)',
      order: 9,
      isButton: true,
      html: fullscreenSVG,
      onClick: () => {
        toggleFullscreen();
      }
    });
  }
  // from @arnowelzel https://github.com/arnowelzel/photoswipe-fullscreen/ (thank you!)
  pswp.events.add(document, 'keydown', (e) => {
    if (e.keyCode == 70) { // 'f'
      toggleFullscreen();
      e.preventDefault();
    }
    //
    if (e.keyCode == 38 || e.keyCode == 40) { // 'haut ou bas'
      pswp.close();
      e.preventDefault();
    }
  });
  lightbox.pswp.ui.registerElement({
    name: 'title',
    order: 10,
    isButton: false,
    appendTo: 'root',
    html: '',
    onInit: (el, pswp) => {
      lightbox.pswp.on('change', () => {
        const currSlideElement = pswp.currSlide.data.element;
        let html = '';
        let title = currSlideElement.querySelector('h3');
        let date = currSlideElement.querySelector('time');
        if (title) {
          html = '<h1>« ' + title.innerHTML + ' »</h1>';
        };
        if (date) {
          html += '<time>' + date.textContent + '</time>';
        }
        el.innerHTML = html;
      });
    }
  });
  lightbox.pswp.ui.registerElement({
    name: 'description',
    order: 11,
    isButton: false,
    appendTo: 'root',
    html: '',
    onInit: (el, pswp) => {
      lightbox.pswp.on('change', () => {
        const currSlideElement = lightbox.pswp.currSlide.data.element;
        let html = '';
        let desc = currSlideElement.querySelector('p');
        if (desc) {
          html = '<div class="caption_container"><div class="caption avatar"><p>' + desc.innerHTML + '</p></div></div>';
        };
        let tags = currSlideElement.nextSibling.nextSibling.outerHTML;
        if (tags) {
          html += tags;
        };
        el.innerHTML = html;
        el.addEventListener('wheel', mouseScroll);
        el.addEventListener('touchstart', startTouchScroll);
        el.addEventListener('touchmove', touchScroll);
      });
    }
  });
});

var touchScrollY, currScroll;

function startTouchScroll(e) {
  touchScrollY = e.touches[0].pageY;
  currScroll = e.target.scrollTop;
}
function touchScroll(e) {
  var deltaY = touchScrollY - e.touches[0].pageY;
  e.target.scrollTo(0, currScroll + deltaY);
}
function mouseScroll(e) {
  let mst = e.target.scrollHeight - e.target.clientHeight;
  if (mst != 0) {
    pswp.options.wheelToZoom = false;
    e.target.scrollBy(0, e.deltaY/10);
    setTimeout(function() {pswp.options.wheelToZoom = true;}, 100);
  }
}

lightbox.on('imageSizeChange', ({ height }) => {
  if (height > window.innerHeight - 240) {
    pswp.element.classList.remove('pswp--ui-visible');
  } else {
    pswp.element.classList.add('pswp--ui-visible');
  }
  if (height > 100) {
    pswp.element.classList.remove('pswp--share-hidden');
  } else {
    pswp.element.classList.add('pswp--share-hidden');
  }
});

let noHistoryBack = false;
let noHistoryPush = false;
let noHistoryReplace = false;
let noPopState = false;
let lastIndex = 0;
let title_origin = document.title;
if (history.scrollRestoration) {
  history.scrollRestoration = "manual";
}

lightbox.on('close', () => {
  // document.documentElement.style.overflow = 'visible';
  // document.documentElement.style.paddingRight = 0;
  if (!noHistoryBack) {
    // console.log("close - back");
    noPopState = true;
    history.back();
    document.title = title_origin;
    lightbox.pswp.currSlide.data.element.scrollIntoView({behavior: "instant", block: "center"});
  };
  noHistoryBack = false;
  document.body.classList.remove('blur');
  if (fullscreenAPI && fullscreenAPI.isFullscreen()) {
    fullscreenAPI.exit();
  };
});

lightbox.on('afterInit', () => {
  // let olw = document.documentElement.clientWidth;
  // document.documentElement.style.overflow = 'hidden';
  // document.documentElement.style.paddingRight = document.documentElement.clientWidth - olw + 'px';
  if (!noHistoryPush) {
    // console.log("init - push");
    document.title = (lightbox.pswp.currSlide.data.element.title || 'Sans Titre') +  ' - ' + title_origin;
    history.pushState(null, "", lightbox.pswp.currSlide.data.element.href.split('#')[0]);
  };
  noHistoryPush = false;
  document.body.classList.add('blur');
});

const shareSVG = '<svg class="pswp__no-toggle" viewBox="0 0 32 32" width="32" height="32" fill="var(--biloubgc)"><path d="m25.333 2a4.6667 4.6667 0 0 0-4.6667 4.6667 4.6667 4.6667 0 0 0 0.10938 0.97526l-10.596 5.2979a4.6667 4.6667 0 0 0-3.5137-1.6064 4.6667 4.6667 0 0 0-4.6667 4.6667 4.6667 4.6667 0 0 0 4.6667 4.6667 4.6667 4.6667 0 0 0 3.5159-1.6042l10.589 5.2956a4.6667 4.6667 0 0 0-0.10482 0.97526 4.6667 4.6667 0 0 0 4.6667 4.6667 4.6667 4.6667 0 0 0 4.6667-4.6667 4.6667 4.6667 0 0 0-4.6667-4.6667 4.6667 4.6667 0 0 0-3.516 1.6042l-10.589-5.2956a4.6667 4.6667 0 0 0 0.10482-0.97526 4.6667 4.6667 0 0 0-0.10938-0.97298l10.596-5.2979a4.6667 4.6667 0 0 0 3.5137 1.6042 4.6667 4.6667 0 0 0 4.6667-4.6667 4.6667 4.6667 0 0 0-4.6667-4.6667z"/></svg>'

lightbox.on('contentAppend', ({ content }) => {
  // content.slide.container.querySelector('.pswp__img--placeholder').style.backgroundColor = content.data.element.style.backgroundColor;
  let share_button = document.createElement('button');
  share_button.classList.add('bubble-style', 'pswp__hide-on-close', 'pswp__button--share-button', 'pswp__no-toggle');
  share_button.title = 'Partager';
  share_button.innerHTML = shareSVG;
  share_button.onclick = (event) => {
    const currSlideElement = lightbox.pswp.currSlide.data.element;
    try {
      navigator.share({
        title: '« ' + currSlideElement.querySelector('h3').textContent + ' » (' + currSlideElement.querySelector('time').textContent + ') par BilouMaster Joke',
        text: '',
        url: String(currSlideElement.href)
      });
    } catch {
      try {
        navigator.clipboard.writeText(String(currSlideElement.href));
        alert("URL copiée dans le presse-papier !\n(Oui, c'est une façon indémodable de partager une page sur Internet...)");
      } catch {
        alert("Désolé, votre navigateur ne prend pas en charge le bouton...\nMais vous pouvez copier-coller l'URL, c'est pareil...")
      }
    }
  }
  content.slide.container.appendChild(share_button);
});

lightbox.on('beforeOpen', () => {
  noHistoryReplace = true;
});

lightbox.on('change', () => {
  if (!noHistoryReplace) {
    // console.log("change - replace");
    document.title = (lightbox.pswp.currSlide.data.element.title || 'Sans Titre') +  ' - ' +  title_origin;
    history.replaceState(null, "", lightbox.pswp.currSlide.data.element.href.split('#')[0]);
  };
  noHistoryReplace = false;
  setTimeout(() => {
    lightbox.pswp.currSlide.data.element.scrollIntoView({behavior: "smooth", block: "center"});
    lastIndex = lightbox.pswp.currIndex;
  }, 50);
});

onpopstate = () => {
  if (!noPopState) {
    if (lightbox.pswp && lightbox.pswp.isOpen) {
      // console.log("postate - close");
      noHistoryBack = true;
      lightbox.pswp.close();
    } else {
      // console.log("postate - open");
      noHistoryPush = true;
      noHistoryReplace = true;
      lightbox.loadAndOpen(lastIndex);
    }
  }
  noPopState = false;
};

function toggleFullscreen() {
  if (fullscreenAPI) {
    if (fullscreenAPI.isFullscreen()) {
      fullscreenAPI.exit();
      setTimeout(function() {
        document.getElementById('pswp__icn-fullscreen-exit').style.display = 'none';
        document.getElementById('pswp__icn-fullscreen-request').style.display = 'inline';
      }, 300);
    } else {
      fullscreenAPI.request(document.querySelector(`.pswp`));
      setTimeout(function() {
        document.getElementById('pswp__icn-fullscreen-exit').style.display = 'inline';
        document.getElementById('pswp__icn-fullscreen-request').style.display = 'none';
      }, 300);
    };
  };
};

function getFullscreenAPI() {
  let api;
  let enterFS;
  let exitFS;
  let elementFS;
  let changeEvent;
  let errorEvent;
  if (document.documentElement.requestFullscreen) {
    enterFS = 'requestFullscreen';
    exitFS = 'exitFullscreen';
    elementFS = 'fullscreenElement';
    changeEvent = 'fullscreenchange';
    errorEvent = 'fullscreenerror';
  } else if (document.documentElement.webkitRequestFullscreen) {
    enterFS = 'webkitRequestFullscreen';
    exitFS = 'webkitExitFullscreen';
    elementFS = 'webkitFullscreenElement';
    changeEvent = 'webkitfullscreenchange';
    errorEvent = 'webkitfullscreenerror';
  };
  if (enterFS) {
    api = {
      request: function (el) {
        if (enterFS === 'webkitRequestFullscreen') {
          el[enterFS](Element.ALLOW_KEYBOARD_INPUT);
        } else {
          el[enterFS]();
        };
      },
      exit: function () {
        return document[exitFS]();
      },
      isFullscreen: function () {
        return document[elementFS];
      },
      change: changeEvent,
      error: errorEvent
    };
  };
  return api;
};

if (document.getElementById('tag_list')) {
  options = {
    dataSource: [{html: get_tag_list()}],
    pswpModule: PhotoSwipe,
    pswpCSS: '/pswp/photoswipe.css',
    bgOpacity: 0.8,
    tapAction: 'close',
    doubleTapAction: 'close',
    bgClickAction: 'close',
    zoom: false
  };
  
  const tag_list = new PhotoSwipeLightbox(options);
  
  tag_list.on('afterInit', () => {
    document.body.classList.add('blur')
  });
  
  tag_list.on('close', () => {
    document.body.classList.remove('blur')
  });
  
  function get_tag_list() {
    return document.getElementById('tag_list').outerHTML;
  };
  
  function open_tag_list() {
    tag_list.loadAndOpen(0);
  };
  
  tag_list.init();
  document.querySelector('#show_tag_list').addEventListener('click', open_tag_list)
}

lightbox.init();