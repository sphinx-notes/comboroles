from __future__ import annotations
from typing import TYPE_CHECKING, cast

from sphinx.util.docutils import SphinxRole 

# Memo:
#
# https://docutils.sourceforge.io/FAQ.html#is-nested-inline-markup-possible
# https://stackoverflow.com/questions/44829580/composing-roles-in-restructuredtext

from docutils.nodes import Node, Inline, TextElement, Text, system_message
from docutils.parsers.rst import roles
from docutils.parsers.rst import states

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.util.typing import RoleFunction

__version__ = '0.1.0'

class CompositeRole(SphinxRole):
    #: Roles to be composited
    components: list[RoleFunction]
    nested_parse: bool

    def __init__(self, rolenames: list[str], nested_parse: bool):
        self.components = []
        for r in rolenames:
            if r in roles._roles: # type: ignore[attr-defined]
                self.components.append(roles._roles[r]) # type: ignore[attr-defined]
            elif r in roles._role_registry: # type: ignore[attr-defined]
                self.components.append(roles._role_registry[r]) # type: ignore[attr-defined]
            else:
                raise KeyError(f'no such role: {r}')
        self.nested_parse = nested_parse


    def run(self) -> tuple[list[Node], list[system_message]]:
        nodes: list[TextElement] = []
        reporter = self.inliner.reporter # type: ignore[attr-defined] 

        # Run all RoleFunction, collect the produced nodes.
        for comp in reversed(self.components): 
            ns, sysmsgs = comp(self.name, self.rawtext, self.text, self.lineno, self.inliner, self.options, self.content)
            if len(sysmsgs) != 0:
                return [], sysmsgs # once system_message is thrown, return
            if len(ns) != 1:
                msg = reporter.error(f'role should returns exactly 1 nodes, but {len(ns)} found: {ns}', line=self.lineno)
                return [], [msg]
            if not isinstance(ns[0], (Inline, TextElement)):
                msg = reporter.error(f'node {ns[0]} is not ({Inline}, {TextElement})', line=self.lineno)
                return [], [msg]
            n = cast(TextElement, ns[0])
            if len(n.children) != 1:
                msg = reporter.error(f'node {n} should has exactly 1 child, but {len(n.children)} found', line=self.lineno)
                return [], [msg]
            if not isinstance(n[0], Text):
                msg = reporter.error(f'child of node {n} should have Text, but {type(n[0])} found', line=self.lineno)
                return [], [msg]
            nodes.append(n)


        # ref: https://stackoverflow.com/questions/44829580/composing-roles-in-restructuredtext
        if self.nested_parse:
            memo = states.Struct(
                document=self.inliner.document, # type: ignore[attr-defined] 
                reporter=reporter, 
                language=self.inliner.language) # type: ignore[attr-defined] 

            n, sysmsgs = self.inliner.parse(self.text, self.lineno, memo, nodes[-1]) # type: ignore[attr-defined] 
            if len(sysmsgs) != 0:
                return [], sysmsgs
            nodes[-1].replace(nodes[-1][0], n)

        # Composite all nodes together.
        for i in range(0, len(nodes) -1):
            nodes[i].replace(nodes[i][0], nodes[i+1])

        return [nodes[0]], []

def _config_inited(app:Sphinx, config:Config) -> None:
    for name, cfg in config.comboroles_roles.items():
        if isinstance(cfg, list):
            rolenames = cfg
            nested_parse = False
        else:
            rolenames = cfg[0]
            nested_parse = cfg[1]
        app.add_role(name, CompositeRole(rolenames, nested_parse))
        

def setup(app:Sphinx):
    """Sphinx extension entrypoint."""

    app.connect('config-inited', _config_inited)

    app.add_config_value('comboroles_roles', {}, 'env', types=dict[str, list[str] | tuple[list[str],bool]])

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
