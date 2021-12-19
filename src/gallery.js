window.addEventListener('DOMContentLoaded', () => {
  if (tag) {
    var el = document.body.querySelector('#tag_list a.' + tag);
    tagfr = el.innerHTML;
    tagdesc = el.title;
    window.document.title += ' - ' + tagfr;
    document.body.querySelector('#current_tag span').innerHTML = tagfr;
    document.body.querySelector('header > hgroup > h1').innerHTML += ' - ' + tagfr;
    document.body.querySelector('header > hgroup > h2').innerHTML = tagdesc;
    document.body.querySelectorAll('.thumb:not(.' + tag + ')').forEach(img => {
      img.outerHTML = '';
    });
    document.body.querySelectorAll('section:not(.' + tag + ')').forEach(s => {
      s.outerHTML = '';
    });
  };
  const lazyThumbs = new IntersectionObserver((entries, lazyThumbs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        let thumb = entry.target;
        thumb.src = thumb.dataset.src;
        lazyThumbs.unobserve(thumb);
      };
    });
  }, {rootMargin: "1000px 0px"});
  document.querySelectorAll('.thumb img').forEach(thumb => {
    lazyThumbs.observe(thumb);
  });
});

function toggleSections(el) {
  let m = document.querySelector('main');
  m.classList.toggle('folded');
  el.scrollIntoView({behavior: "instant", block: "start"});
};

function trippyZone() {
  if (window.scrollY > 320) {
    document.body.classList.add('not-trippy');
  } else if (document.body.classList.contains('not-trippy')) {
    document.body.classList.remove('not-trippy');
  };
};
document.addEventListener('scroll', trippyZone);

var tag = window.location.pathname.split('/tag/');
if (tag.length > 1) {
  tag = tag[1];
  var css = '.thumb:not(.' + tag + '), section:not(.' + tag +') { display: none; } #current_tag {display: block}',
    head = document.head,
    style = document.createElement('style');
  head.appendChild(style);
  style.appendChild(document.createTextNode(css));
} else {tag = false;};