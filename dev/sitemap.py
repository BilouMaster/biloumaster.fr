from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import config


def generate_sitemap(website):
    urlset = Element(
        "urlset",
        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9",
    )
    for page in website:
        if not page:
            continue
        if page.included:
            continue
        if page.name in ['301','403','404','410','500','503']:
            continue
        url = SubElement(urlset, "url")
        SubElement(url, "loc").text = page.canon_url['fr']
    pretty_xml = minidom.parseString(
        tostring(urlset, encoding="utf-8")
    ).toprettyxml(indent="  ")

    with open(f'{config.output}/sitemap.xml', "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write("\n".join(pretty_xml.split("\n")[1:]))

def generate_robottxt():
    with open(f'{config.output}/robot.txt', "w", encoding="utf-8") as f:
        f.write(f"""User-agent: *
Allow: /

Sitemap: {config.url}/sitemap.xml""")