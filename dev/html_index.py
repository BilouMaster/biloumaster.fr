#intern
from templates import get_templates
from utils.clean import str_clean
from utils.indent import str_indent

def write_index():
    template = get_templates()
    content = '''<a class="navig" href="creations">
    <img src="/img/creations.svg" alt="logo creations">
    <h1>Bilou Créations</h1>
</a>'''
    footer = '''<p>Y'a pas grand chose, c'est normal, c'est en construction...</p>
<nav>
    <a href="https://twitter.com/biloumaster" rel="external" target="_blank" title="@biloumaster sur Twitter...">
        <img alt="Twitter" src="/img/twitter.svg"/>
    </a>
    <a href="https://www.facebook.com/biloumaster" rel="external" target="_blank" title="@biloumaster sur Facebook...">
        <img alt="Facebook" src="/img/facebook.svg"/>
    </a>
</nav>'''
    content = template['main'].format(
        nav                 = str_indent(template['header_nav_0'], 2),
        title               = "BilouMaster Joke's ouèb-site",
        meta_title          = "BilouMaster Joke's ouèb-site",
        description         = "J'ai tellement fait plein d'trucs qu'il me fallait un site ouèb pour entreposer tout ça.",
        meta_description    = "J'ai tellement fait plein d'trucs qu'il me fallait un site ouèb pour entreposer tout ça.",
        extralink           = '<link rel="stylesheet" href="/src/index.css">',
        content             = str_indent(content, 2),
        footer              = str_indent(footer, 2)
    )
    open('../index.html', 'w').write(str_clean(content))