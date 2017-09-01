def format_comment(news):
    header = "## Noticias similares de otros diarios:\n\n"
    related_news = ''
    for new in news:
        related_news += ' - Diario ' + new[0] + ': '
        related_news += '[' + new[1]['text'].split('\n', 1)[0] + ']'
        related_news += '(' + new[1]['link'] + ')\n\n'
    return header + related_news + footer()


signature = ''


def set_signature(new_signature):
    global signature
    signature = new_signature


def footer():
    bot_signature = "Diario Opositor Bot, distintas perspectivas de la misma noticia"
    link_al_source = "\n\n[Codigo fuente](https://github.com/Bullrich/Diario-Opositor-Bot). "

    return '---\n\n' + bot_signature + link_al_source + '\n\n' + signature
