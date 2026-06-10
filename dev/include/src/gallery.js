window.addEventListener('DOMContentLoaded', () => {
  if (tag) {
    const el = document.body.querySelector('#tag_list a.' + tag),
      tagtitle = el.innerHTML,
      tagdesc = el.title;
    window.document.title += ' - ' + tagtitle;
    document.body.querySelector('#current_tag span').innerHTML = tagtitle;
    document.body.querySelector('#page_title > h1').innerHTML = tagtitle;
    document.body.querySelector('#page_title > p').innerHTML = tagdesc;
    document.body.querySelector('header > nav > a:nth-child(2)').href = '../..';
    document.body.querySelectorAll('.gallery > a:not(.' + tag + ')').forEach(a => {
      a.nextSibling.nextSibling.outerHTML = '';
      a.outerHTML = '';
    });
    document.body.querySelectorAll('section:not(.' + tag + ')').forEach(s => {
      s.outerHTML = '';
    });
    document.body.querySelectorAll('.'+tag).forEach(t => {
      t.classList.add('current');
    });
  };
  const lazyThumbs = new IntersectionObserver((entries, lazyThumbs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        let thumb = entry.target;
        thumb.style.backgroundImage = "url('/img/gallery/thumbnail/" + thumb.dataset.name + "_thumbnail.webp')";
        lazyThumbs.unobserve(thumb);
      }
    });
  }, {rootMargin: "1000px 0px"});
  document.querySelectorAll('.gallery a').forEach(thumb => {
    lazyThumbs.observe(thumb);
  });
  document.querySelectorAll('#gallery section').forEach(section => {
    section.addEventListener('click', toggleSelf);
  });
});

function enlarge(el) {
  const m = document.body;
  m.classList.toggle('enlarged');
  psyche_origin()
  if (focusel) {
    focusel.scrollIntoView({behavior: "instant", block: "center"});
  }
  if (m.classList.contains('enlarged')) {
    el.innerHTML = '🐛'
    el.title = 'calmer la page'
  } else {
    el.innerHTML = '🍆'
    el.title = 'élargir la page 👄'
  }
}

function toggleSections(el) {
  const m = document.body;
  m.classList.toggle('folded');
  if (el.getBoundingClientRect().top + window.pageYOffset > 180) {
    el.scrollIntoView({behavior: "instant", block: "start"});
    window.scrollBy({top:-25, behavior:"smooth"})
  }
}

function toggleSelf(el) {
  if (el.target.tagName == 'DIV') {
    toggleSections(el.target.children[0]);
  }
  if (el.target.tagName == 'H2') {
    toggleSections(el.target);
  }
}

let focusel;
let olwwidth = window.innerWidth;
window.addEventListener('resize', () => {
  if (focusel && window.innerWidth != olwwidth) {
    focusel.scrollIntoView({behavior: "instant", block: "center"});
  }
  olwwidth = window.innerWidth;
});
setInterval(function () {
  focusel = document.elementFromPoint(window.innerWidth/2, window.innerHeight/2) || focusel;
}, 500);

var tag = window.location.pathname.split('/tag/');
if (tag.length > 1) {
  tag = tag[1];
  var css = '.gallery > a:not(.' + tag + ').gallery > a:not(.' + tag + '), section:not(.' + tag +'), #note {display: none} #current_tag {display: block}',
    head = document.head,
    style = document.createElement('style');
  head.appendChild(style);
  style.appendChild(document.createTextNode(css));
} else {tag = false;};