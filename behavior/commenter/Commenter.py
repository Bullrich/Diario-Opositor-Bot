import logging


class Commenter:
    def __init__(self, signature):
        self.logger = logging.getLogger(__name__)
        self.signature = signature

    def format_comment(self, news):
        header = "## Noticias similares de otros diarios:\n\n"
        related_news = ''
        for new in news:
            related_news += ' - Diario ' + new[0] + ': '
            related_news += '[' + new[1]['text'].split('\n', 1)[0] + ']'
            related_news += '(' + new[1]['link'] + ')\n\n'
        return header + related_news + self.footer()

    def footer(self):
        bot_signature = "Diario Opositor Bot, distintas perspectivas de la misma noticia"
        link_al_source = "\n\n[Codigo fuente](https://github.com/Bullrich/Diario-Opositor-Bot)."

        return '---\n\n' + bot_signature + link_al_source + '\n\n' + self.signature
