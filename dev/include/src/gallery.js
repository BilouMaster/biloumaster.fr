window.addEventListener('DOMContentLoaded', initGallery);
document.addEventListener('spa:load', initGallery);

function initGallery() {
  let tag = window.location.pathname.split('/tag/');
  if (tag.length > 1) {
    tag = tag[1];
    let css = '.gallery > a:not(.' + tag + ').gallery > a:not(.' + tag + '), section:not(.' + tag +'), #note {display: none} #current_tag {display: block}',
      head = document.head,
      style = document.createElement('style');
    head.appendChild(style);
    style.appendChild(document.createTextNode(css));
  } else {tag = false;};
  if (tag) {
    const el = document.body.querySelector('#tag_list a.' + tag),
      tagtitle = el.textContent,
      tagdesc = el.title;
    window.document.title = `${tagtitle} - ${window.document.title}`;
    document.body.querySelector('#current_tag span').textContent = tagtitle;
    document.body.querySelector('#page_title > h1').textContent = tagtitle;
    document.body.querySelector('#page_title > p').textContent = tagdesc;
    document.body.querySelector('header > nav > a:nth-child(2)').href = '../..';
    document.body.querySelectorAll('.gallery > a:not(.' + tag + ')').forEach(a => {
      a.nextSibling.nextSibling.remove();
      a.remove();
    });
    document.body.querySelectorAll('section:not(.' + tag + ')').forEach(s => {
      s.remove();
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