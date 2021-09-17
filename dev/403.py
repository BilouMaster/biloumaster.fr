#intern
from utils.clean import str_clean

file = open('templates/main.html', 'r')
template = file.read()
file.close()
content = template.format(
    nav                 = '<nav><a href="/"><img id="logo" src="/img/biloumaster.svg" alt="logo BilouMaster"></a></nav>',
    title               = "",
    meta_title          = "Bilou Restricted Area",
    description         = "Aïe...",
    meta_description    = "Accès interdit...",
    extralink           = '<link rel="stylesheet" href="/src/404.css">',
    content             = '<p><span>403</span><br>Access for Biden</p>',
    footer              = ''
)
open('../html/403.html', 'w').write(str_clean(content))