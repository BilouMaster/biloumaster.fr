var lastTrack;
var vizuexists = false;

function pl_note(text) {
    let n = document.getElementById('pl-note');
    n.classList.remove('show');
    n.innerText = text;
    void n.offsetWidth;
    n.classList.add('show');
}

function pl_random() {
    setTimeout(function() {
        let pl = document.getElementById('player');
        pl.classList.remove('linear');
        pl.classList.add('random');
        pl_note("Ordre aléatoire");
    }, 100);
}

function pl_loop() {
    setTimeout(function() {
        let pl = document.getElementById('player');
        pl.classList.remove('random');
        pl.classList.add('loop');
        pl_note("Lecture en boucle");
        document.getElementById('pl-audio').setAttribute('loop', true);
    }, 100);
}

function pl_linear() {
    setTimeout(function() {
        let pl = document.getElementById('player');
        pl.classList.remove('loop');
        pl.classList.add('linear');
        pl_note("Ordre par défaut");
        document.getElementById('pl-audio').removeAttribute('loop');
    }, 100);
}

function pl_play() {
    setTimeout(function() {
        const audioElem = document.getElementById('pl-audio');
        audioElem.play();
        let pl = document.getElementById('player');
        pl.classList.remove('pause');
        pl.classList.add('play');
    }, 150);
}

function pl_pause() {
    setTimeout(function() {
        const audioElem = document.getElementById('pl-audio');
        audioElem.pause();
        let pl = document.getElementById('player');
        pl.classList.remove('play');
        pl.classList.add('pause');
        if ('mediaSession' in navigator) {
            navigator.mediaSession.playbackState = "paused";
        }
    }, 50);
}

function mod(n, m) {
    return ((n % m) + m) % m;
}

function pl_next() {
    const tracks = Array.prototype.slice.call(document.getElementsByClassName('track'));
    const pl = document.getElementById('player');
    if (pl.classList.contains('random')) {
        tr_play(tracks[Math.floor(Math.random() * tracks.length)]);
    } else {
        tr_play(tracks[(tracks.indexOf(lastTrack) + 1) % tracks.length]);
    }
}

function pl_prev() {
    const tracks = Array.prototype.slice.call(document.getElementsByClassName('track'));
    const pl = document.getElementById('player');
    if (pl.classList.contains('random')) {
        tr_play(tracks[Math.floor(Math.random() * tracks.length)]);
    } else {
        tr_play(tracks[mod(tracks.indexOf(lastTrack) - 1, tracks.length)]);
    }
}

function toggleSections(el) {
    const m = document.querySelector('main');
    m.classList.toggle('folded');
    el.parentNode.scrollIntoView({behavior: "instant", block: "start"});
}

function tr_play(el = lastTrack) {
    const audioElem = document.getElementById('pl-audio');
    if (!vizuexists) {
        new visualiser(audioElem);
        vizuexists = true;
    }
    audioElem.src = "/mp3/" + el.getAttribute('data-filename') + ".mp3";
    const title = el.childNodes[3].innerText;
    const album = el.parentNode.parentNode.childNodes[1].innerText;
    const artwork = el.parentNode.parentNode.childNodes[5].src;
    document.querySelector('#player .pl-title').innerText = title;
    document.querySelector('#player .pl-album').innerText = album;
    document.querySelector('#player .pl-head').style.backgroundImage = 'url("' + artwork + '")';
    const pl = document.getElementById('player');
    if (!pl.classList.contains('active')) {
        pl.classList.add('active');
    }
    pl.classList.remove('pause');
    pl.classList.add('play');
    audioElem.play();
    if (lastTrack) {
        lastTrack.classList.remove('playing');
    }
    el.classList.add('playing');
    lastTrack = el;
    if ('mediaSession' in navigator) {
        navigator.mediaSession.metadata = new MediaMetadata({
          title: title,
          artist: 'BilouMaster Joke',
          album: album,
          artwork: [{ src: artwork, type: 'image/jpeg' }]
        });
        navigator.mediaSession.setActionHandler('play', pl_play);
        navigator.mediaSession.setActionHandler('pause', pl_pause);
        navigator.mediaSession.setActionHandler('previoustrack', pl_prev);
        navigator.mediaSession.setActionHandler('nexttrack', pl_next);
        navigator.mediaSession.setActionHandler('seekto', (details) => {
            if (details.fastSeek && 'fastSeek' in audioElem) {
                audioElem.fastSeek(details.seekTime);
                return;
            }
            audioElem.currentTime = details.seekTime;
        });
        navigator.mediaSession.playbackState = "playing";
    }
}

function mmss(sec) {
    return ("00" + Math.floor(sec / 60)).slice(-2) + ":" + ("00" + Math.floor(sec % 60)).slice(-2);
}

var timeChanging = false;
function pl_time(el) {
    document.querySelector('.pl-bar .pl-current-time').innerText = mmss(el.currentTime);
    if (timeChanging == false) {
        if (isNaN(el.duration)) {
            document.querySelector('.pl-bar input').value = 0;
        } else {
            document.querySelector('.pl-bar input').value = el.currentTime * 100 / el.duration;
        }
    }
}

function pl_timeChange(el) {
    const audioEl = document.getElementById('pl-audio');
    audioEl.currentTime = Math.floor(el.value * audioEl.duration / 100);
}

function pl_change_volume(el) {
    document.getElementById('pl-audio').volume = el.value;
    var r, g, b, f = el.value;
    if (f < 0.5) {
        r = 31 + (214 - 31) * f * 2;
        g = 30 + (184 - 30) * f * 2;
        b = 36 + (163 - 36) * f * 2;
    } else {
        r = 214 + (159 - 214) * (f - 0.5) * 2;
        g = 184 + (235 - 184) * (f - 0.5) * 2;
        b = 163 + (163 - 163) * (f - 0.5) * 2;
    }
    el.style.setProperty('--r-track-lfc', 'rgba('+r+','+g+','+b+',.5)')
    if (el.value == 0.0) {
        document.querySelector('.pl-volume').classList = "pl-volume nosound";
    } else if (el.value <= 0.5) {
        document.querySelector('.pl-volume').classList = "pl-volume midlevel";
    } else {
        document.querySelector('.pl-volume').classList = "pl-volume";
    }
}

function pl_duration(el) {
    document.querySelector('#player .pl-time').innerText = mmss(el.duration);
}

class visualiser {
    constructor(audioElem) {
        this.audioContext = new AudioContext();
        this.src = this.audioContext.createMediaElementSource(audioElem);
        const analyser = this.audioContext.createAnalyser();
        const canvas = document.getElementById('pl-vizu');
        const ctx = canvas.getContext('2d');
        this.src.connect(analyser);
        analyser.connect(this.audioContext.destination);
        analyser.fftSize = 2**8;
        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        let barHeight;
        let bar;
        const bg = document.querySelector('#player .pl-head');

        function renderFrame() {
            requestAnimationFrame(renderFrame);
            if (isNaN(audioElem.duration)) {
                bg.style.backgroundPositionY = '0%';
            } else {
                bg.style.backgroundPositionY = audioElem.currentTime * 100 / audioElem.duration + '%';
            }
            bar = 1;
            analyser.getByteFrequencyData(dataArray);
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            canvas.width = canvas.offsetWidth;
            canvas.height = canvas.offsetHeight;
            const barWidth = (canvas.width / bufferLength) * 1.2;
            // 31, 30, 36
            // 214, 184, 231
            // 159, 235, 163
            for (let i = 0; i < bufferLength; i++) {
                const f = dataArray[i] / 255;
                var r, g, b;
                barHeight = f * canvas.height;
                if (f < 0.5) {
                    r = 31 + (214 - 31) * f * 2;
                    g = 30 + (184 - 30) * f * 2;
                    b = 36 + (163 - 36) * f * 2;
                } else {
                    r = 214 + (159 - 214) * (f - 0.5) * 2;
                    g = 184 + (235 - 184) * (f - 0.5) * 2;
                    b = 163 + (163 - 163) * (f - 0.5) * 2;
                }
                ctx.fillStyle = `rgba(${r}, ${g}, ${b}, .5)`;
                ctx.fillRect(bar, canvas.height - barHeight, barWidth, barHeight);
                bar += barWidth + 1;
            }
        }

        renderFrame();
    }
}