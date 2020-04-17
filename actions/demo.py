from .dump.dump_messages import dump_messages
from .render_to_html import render_to_html


def demo():
    """Демо: выгрузить один диалог и отрисовать [устарел]"""
    dump_messages(True)
    render_to_html()
