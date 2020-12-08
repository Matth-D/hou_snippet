import os

snippet_folder = r"C:\Users\Matthieu\.h_snippet\snippets_received"

SEP = "$#!--%"


def get_snippet_list():

    snippet_list = []

    for snippet in os.listdir(snippet_folder):
        snippet_path = os.path.join(snippet_folder, snippet)
        infos = os.path.splitext(snippet)[0].split(SEP)
        infos.remove(infos[-1])
        infos += [snippet_path]
        snippet_list.append(infos)

    return snippet_list


snippet_list = get_snippet_list()

print snippet_list
