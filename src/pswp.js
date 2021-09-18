import PhotoSwipeLightbox from '/pswp/photoswipe-lightbox.esm.js';

const fullscreenAPI = getFullscreenAPI();
const fullscreenSVG = '<svg aria-hidden="true" class="pswp__icn" viewBox="0 0 32 32" width="32" height="32"><use class="pswp__icn-shadow" xlink:href="#pswp__icn-fullscreen-exit"/><use class="pswp__icn-shadow" xlink:href="#pswp__icn-fullscreen-request"/><path d="M8 8v6.047h2.834v-3.213h3.213V8h-3.213zm9.953 0v2.834h3.213v3.213H24V8h-2.834zM8 17.953V24h6.047v-2.834h-3.213v-3.213zm13.166 0v3.213h-3.213V24H24v-6.047z" id="pswp__icn-fullscreen-request"/><path d="M11.213 8v3.213H8v2.834h6.047V8zm6.74 0v6.047H24v-2.834h-3.213V8zM8 17.953v2.834h3.213V24h2.834v-6.047h-2.834zm9.953 0V24h2.834v-3.213H24v-2.834h-3.213z" id="pswp__icn-fullscreen-exit" style="display:none"/></svg>';

let options = {
  gallerySelector: 'body',
  childSelector: '.thumb',
  pswpModule: '/pswp/photoswipe.esm.js',
  bgOpacity: 0.8,
  spacing: 0.05,
  paddingTop: 72,
  paddingBottom: 72,
  preload: [2, 2],
  loop: false,
  zoom: false
};

const lightbox = new PhotoSwipeLightbox(options);

lightbox.on('uiRegister', function() {
  if (fullscreenAPI) {
    lightbox.pswp.ui.registerElement({
      name: 'fullscreen-button',
      title: 'Toggle fullscreen',
      order: 9,
      isButton: true,
      html: fullscreenSVG,
      onClick: (event, el) => {
        toggleFullscreen();
      }
    });
  };
  lightbox.pswp.ui.registerElement({
    name: 'title',
    order: 10,
    isButton: false,
    appendTo: 'root',
    html: '',
    onInit: (el, pswp) => {
      lightbox.pswp.on('change', () => {
        const currSlideElement = lightbox.pswp.currSlide.data.element;
        let html = '';
        let title = currSlideElement.title;
        let date = currSlideElement.dataset.date;
        if (title) {
          html = '<h1>« ' + title + ' »</h1>';
        };
        if (date) {
          html += '<date>' + date + '</date>';
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
        let desc = currSlideElement.dataset.desc;
        if (desc) {
          html = '<div class="caption_container"><div class="caption avatar">' + desc + '</div></div>';
        };
        let tags = currSlideElement.nextSibling.nextSibling.outerHTML;
        if (tags) {
          html += tags;
        };
        el.innerHTML = html;
      });
    }
  });
});

lightbox.on('close', () => {
  document.body.classList.remove('blur')
  if (fullscreenAPI && fullscreenAPI.isFullscreen()) {
    fullscreenAPI.exit();
  };
});

lightbox.on('afterInit', () => {
  document.body.classList.add('blur')
});

lightbox.on('change', () => {
  setTimeout(() => {lightbox.pswp.currSlide.data.element.scrollIntoView({behavior: "smooth", block: "center"})}, 333);
});

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

options = {
  dataSource: [{html: get_tag_list()}],
  pswpModule: '/pswp/photoswipe.esm.js',
  pswpCSS: '/pswp/photoswipe.css',
  bgOpacity: 0.8,
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

lightbox.init();
tag_list.init();

document.querySelector('#show_tag_list').addEventListener('click', open_tag_list)