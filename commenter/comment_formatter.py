import os

def format_comment(news):
    header = "## Noticias similares de otros diarios:\n\n"
    noticias_relacionadas = ''
    for new in news:
        noticias_relacionadas += ' - Diario ' + new[0] + ': '
        noticias_relacionadas += '[' + new[1]['text'].split('\n', 1)[0] + ']'
        noticias_relacionadas += '(' + new[1]['link'] + ')\n\n'
    return header + noticias_relacionadas + footer()


signature = os.environ.get('bot_firma') if os.environ.get('bot_firma') is not None else ""


def footer():
    bot_signature = "Diario Opositor Bot, distintas perspectivas de la misma noticia"
    link_al_source = "\n\n[Codigo fuente](https://github.com/Bullrich/Diario-Opositor-Bot). "

    return '---\n\n' + bot_signature + link_al_source + '\n\n' + signature
