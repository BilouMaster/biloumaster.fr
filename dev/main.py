from html_navig import process_navig
from html_index import write_index
from html_games import write_games
from html_joke import write_joke
from html_compositions import write_compositions
import html_403
import html_404

write_joke()
process_navig('creations', ['tradi', 'digi', 'pixelart', 'sculpture'])
write_compositions()
write_index()
write_games()