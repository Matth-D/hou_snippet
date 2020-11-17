"""Executable for h_snippet.

:Author: Matthieu Druaud
"""


from program import ui

widgets = []


def start():
    win = ui.HSnippet()
    widgets.append(win)
    win.show()

