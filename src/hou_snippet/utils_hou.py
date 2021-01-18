import hou

HOU_VER = hou.applicationVersion()[0]


def is_snippet(selection):
    """Check if selected node is a snippet network.

    Args:
        selection (obj): Houdini node single selection. Expecting utils.get_selection(-1).

    Returns:
        bool: True or False if selection is a snippet network.
    """
    if not selection:
        return False
    snippet_verif = hou.node(selection.path() + "/snippet_verification")
    if "snp_" not in selection.name() or not snippet_verif:
        return False
    return True


def get_selection(single_or_multiple):
    """Return node selection, single or multiple.

    Args:
        single_or_multiple (int): Selection mode. -1 if single, 1 if multiple. Safety check.
    
    Returns:
        obj: Houini selection object.
    """
    selection = hou.selectedNodes()
    if single_or_multiple == 0 and selection:
        selection = hou.selectedNodes()[0]
    return selection
