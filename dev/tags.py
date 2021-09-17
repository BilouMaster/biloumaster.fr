fr = {
    'pencil': 'Crayon',
    'colorpencil': 'Crayon de couleur',
    'watercolor': 'Aquarelle',
    'woman':'Femme',
    'girl':'Fille',
    'jester':'Bouffon',
    'impressionism':'Impressionnisme',
    'expressionism':'Expressionnisme',
    'psychedelism':'Psychédélisme',
    'surrealism':'Surréalisme',
    'abstract':'Abstrait',
    'depression':'Dépression',
    'grayscale':'Noir et blanc',
    'portrait':'Portrait',
    'saphism':'Saphisme',
    'nude':'Nu',
    'oilpastel':'Pastel à huile',
    'softpastel':'Pastel sec',
    'acrylic':'Acrylique',
    'painting':'Peinture',
    'charcoal':'Fusain',
    'cute':'Mignon',
    'anxiety':'Anxiété',
    'painting':'Peinture',
    'blackpaper':'Papier noir',
    'sepia':'Crayon sépia',
    'sanguine':'Crayon sanguine',
    'whitepencil':'Crayon blanc',
    'blackpencil':'Crayon noir',
    'drawing':'Dessin',
    'mushroom':'Champignon',
    'music':'Musique',
    'monster':'Monstre',
    'bic':'Stylo bic',
    'pen':'Stylo',
    'feltpen':'Feutre',
    "digital":'Numérique',
    'lre':'Le Ruban Écarlate',
    'decadence':'Décadence',
    'bogossstory':'BogossStory',
    'selfportrait':'Auto-portrait',
    'chinaink':'Encre de Chine'
}
desc_fr = {
    'pencil': "Dessins au crayon de bois, crayon gris, crayon à papier ou peu importe comment vous appellez ça... Notez que je ne suis pas fana des critériums.",
    'colorpencil': "Dessins au crayon de couleur, comme à l'école primaire.",
    'watercolor': "Peintures à l'aquarelle.",
    'woman':'Dessins et peintures de femmes.',
    'girl':'Dessins et peintures de jeunes femmes.',
    'jester':"Je fais plein de bouffons parce que j'en suis un.",
    'impressionism':'Impressionnisme... ou pas.',
    'expressionism':"Dessins et peintures exprimant des émotions et sentiments",
    'psychedelism':"Le psychédélisme c'est pas juste des contrastes forts et des couleurs barrées, c'est aussi un jeu pour les sens, et du mouvement dans la composition.",
    'surrealism':'Surréalisme... ou pas.',
    'abstract':'Dessins et peintures relativement abstraits',
    'depression':'Je suis bipolaire... La dépression, ça me connaît.',
    'grayscale':"Dessins et peintures pour ceux qui n'aiment pas les couleurs, ou qui sont daltoniens",
    'portrait':"Des portraits de gens, ou d'imagination",
    'saphism':"Oui, on peut représenter des lesbiennes sans qu'elles se galochent ou tripotent.",
    'nude':"Dessins et peintures de nus.",
    'oilpastel':'Dessins au pastel à huile',
    'softpastel':'Dessins au pastel sec',
    'acrylic':'Peintures acryliques sur papier',
    'painting':'Peintures sur papier ou carton toile',
    'charcoal':'Dessins au fusain',
    'cute':'Des trucs mignons à base de cuteness',
    'anxiety':'Des trucs anxieux',
    'blackpaper':'Dessins sur papier noir',
    'sepia':'Dessins au crayon sépia',
    'sanguine':'Dessins au crayon sanguine',
    'whitepencil':'Dessins au crayon blanc',
    'blackpencil':'Dessins au crayon bien noir qui casse',
    'drawing':'Des dessins par millier',
    'mushroom':'Des champignons, oui, mais des champignons bilouteux !',
    'music':"Dessins autours d'une passion : la musique",
    'monster':"Quand j'étais petit, j'aimais bien les monstres...",
    'bic':'Dessins au stylo BIC normal, quatre couleur ou noir...',
    'digital':'Dessins et peintures numériques, réalisés avec Photoshop, Illustrator, Krita, ou InkScape',
    'joke':"Joke... Bah c'est moi, mon avatar, un bouffon facétieux, que je représente dans tous mes états.",
    'pen':"Dessins au stylo à bille, stylo à encre gel, stylo feutre... Je teste tout.",
    'lre':"Artworks de mon projet de point & click",
    'decadence':'Artworks de mon projet de RPG',
    'bogossstory':'Artworks de BogossStory, mon projet débile',
    'selfportrait':'Plus ou moins...',
    'observation':"Dessins d'observation",
    'chinaink':"Dessins à l'encre de Chine",
    'stupeflip':'Le Stupeflip CROU ne MOURRA JAMAIS !!',
    'stopart':"Le Stop-Art est un genre que j'ai inventé en mélangeant plein de notions comme la programmation, les mathématiques, le dessin technique, la calligraphie, l'heuristique et la cryptographie... En gros."
}

def str_tag_fr(tag: str) -> str:
    global fr
    if tag in fr:
        return fr[tag]
    else:
        return tag.capitalize()

def str_tag_desc_fr(tag: str) -> str:
    global fr
    if tag in desc_fr:
        return desc_fr[tag]
    else:
        return  'Éléments correspondants au mot-clé «' + tag.capitalize() + '»'

def str_tags(tags: str, path: str) -> str:
    if tags:
        if type(tags) == str:
            tags = tags.split(';')
        if type(tags) == set:
            tags = list(tags - {''})
        tags.sort(key=lambda k: str_tag_fr(k))
        return '<aside class="tags">' + ''.join(map(lambda k: '<a href="' + path + k + '" rel="tag" class="' + k + '" title="' + str_tag_desc_fr(k) + '">' + str_tag_fr(k) + '</a>', tags)) + '</aside>'
    else:
        return '<!--no tags-->'

def str_current_tag(tags: set) -> str:
    if tags:
        return '<p id="current_tag" style="display:none;">Galerie filtrée avec le mot-clé «' + ''.join(map(lambda k: '<span class="' + k + '" title="' + str_tag_desc_fr(k) + '">' + str_tag_fr(k) + '</span>', tags)) + '», <a href="..">cliquez ici</a> pour voir la galerie entière.</p>'
    else:
        return '<!--no tags-->'

def str_lowercase(s: str) -> str:
    return s[0].lower() + s[1:]

def str_tag_list(tags: str) -> str:
    if tags:
        tags = tags.split(';')
        tags.sort(key=lambda k: str_tag_fr(k))
        return ', '.join(map(lambda k: str_lowercase(str_tag_fr(k)), tags))
    else:
        return ''

def str_tag_classes(tags: str) -> str:
    if tags:
        tags = tags.split(';')
        return ' '.join(tags)
    else:
        return ''