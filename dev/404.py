#intern
from utils.clean import str_clean

file = open('templates/main.html', 'r')
template = file.read()
file.close()
content = template.format(
    nav                 = '<nav><a href="/"><img id="logo" src="/img/biloumaster.svg" alt="logo BilouMaster"></a></nav>',
    title               = "",
    meta_title          = "Bilou Fail 404",
    description         = "Aïe...",
    meta_description    = "Cette page n'existe pas...",
    extralink           = '<link rel="stylesheet" href="/src/404.css">',
    content             = '<p><span>404</span><br>PAJ NOT FOUND</p>',
    footer              = ''
)
open('../html/404.html', 'w').write(str_clean(content))