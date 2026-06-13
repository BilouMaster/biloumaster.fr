import config

base = {
  "@context": "https://schema.org",
  "@graph": [{
    "@type": "WebSite",
    "@id": f"{config.url}/#website",
    "name": config.sitename,
    "url": config.url
  }, {
    "@type": "Person",
    "@id": f"{config.url}/#person",
    "name": config.author,
    "url": f"{config.url}/joke",
    "image": f"{config.url}/img/logo.png",
    "address": config.address,
    "sameAs": config.sameAs
  }]
}

list = {
  "Jeu": {
    "@context": "https://schema.org",
    "@type": "VideoGame",
    "name": "",
    "description": "",
    "datePublished": "",
    "url": "",
    "author": {
      "@id": f"{config.url}/#person"
    }
  },
  "Album": {
    "@context": "https://schema.org",
    "@type": "MusicAlbum",
    "@id": "#album",
    "name": "",
    "byArtist": {
      "@id": f"{config.url}/#person"
    }
  },
  "Track": [{
    "@context": "https://schema.org",
    "@type": "MusicComposition",
    "name": "",
    "composer": {
      "@id": f"{config.url}/#person"
    },
    "url": ""
  },
  {
    "@context": "https://schema.org",
    "@type": "MusicRecording",
    "name": "",
    "inAlbum": {
      "@id": "#album"
    }
  }],
  "Gallery": {
    "@context": "https://schema.org",
    "@type": "ImageGallery",
    "@id": "#gallery",
    "name": "",
    "url": "",
    "description": "",
    "temporalCoverage": "/",
    "author": {
      "@id": f"{config.url}/#person"
    },
    "isPartOf": {
      "@id": f"{config.url}/#website"
    },
  },
  "Image": {
    "@context": "https://schema.org",
    "@type": "VisualArtwork",
    "@id": "#artwork",
    "name": "",
    "image": "",
    "description": "",
    "dateCreated": "",
    "artform": "",
    "keywords": [],
    "creator": {
      "@id": f"{config.url}/#person"
    },
    "isPartOf": {
      "@id": "#gallery"
    }
  }
}