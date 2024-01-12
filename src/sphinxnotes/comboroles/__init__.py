from __future__ import annotations
from typing import TYPE_CHECKING, cast

from sphinx.util.docutils import SphinxRole

from docutils.nodes import Node, Inline, TextElement, Text, system_message
from docutils.parsers.rst import roles
from docutils.parsers.rst import states

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.config import Config

__version__ = '0.1.0'

class CompositeRole(SphinxRole):
    #: Rolenames to be composited
    rolenames: list[str]
    #: Whether to enable :ref:`nested-parse`
    nested_parse: bool


    def __init__(self, rolenames: list[str], nested_parse: bool):
        self.rolenames = rolenames
        self.nested_parse = nested_parse


    def run(self) -> tuple[list[Node], list[system_message]]:
        nodes: list[TextElement] = []
        reporter = self.inliner.reporter # type: ignore[attr-defined]

        # Lookup RoleFunction by name.
        # NOTE: We can not do this during __init__, some roles created by
        # 3rd-party extension do not exist yet at that time.
        components = []
        for r in self.rolenames:
            if r in roles._roles: # type: ignore[attr-defined]
                components.append(roles._roles[r]) # type: ignore[attr-defined]
            elif r in roles._role_registry: # type: ignore[attr-defined]
                components.append(roles._role_registry[r]) # type: ignore[attr-defined]
            else:
                msg = reporter.error(f'no such role: {r}', line=self.lineno)
                return [], [msg]

        # Run all RoleFunction, collect the produced nodes.
        for comp in components:
            ns, msgs = comp(self.name, self.rawtext, self.text, self.lineno, self.inliner, self.options, self.content)

            # The returned nodes should be exactly one TextElement and contains
            # exactly one Text node as child, like this::
            #
            #   <TextElement>
            #       <Text>
            #
            # So that it can be used as part of composite roles.
            if len(msgs) != 0:
                return [], msgs # once system_message is thrown, return
            if len(ns) != 1:
                msg = reporter.error(f'role should returns exactly 1 node, but {len(ns)} found: {ns}', line=self.lineno)
                return [], [msg]
            if not isinstance(ns[0], (Inline, TextElement)):
                msg = reporter.error(f'node {ns[0]} is not ({Inline}, {TextElement})', line=self.lineno)
                return [], [msg]
            n = cast(TextElement, ns[0])
            if len(n) != 1:
                msg = reporter.error(f'node {n} should has exactly 1 child, but {len(n)} found', line=self.lineno)
                return [], [msg]
            if not isinstance(n[0], Text):
                msg = reporter.error(f'child of node {n} should have Text, but {type(n[0])} found', line=self.lineno)
                return [], [msg]
            nodes.append(n)

        if len(nodes) == 0:
            return [], [] # no node produced, return

        if self.nested_parse:
            # See also:
            #
            # - :ref:`nested-parse`
            # - https://stackoverflow.com/questions/44829580/composing-roles-in-restructuredtext
            inliner = self.inliner
            memo = states.Struct(
                document=inliner.document, # type: ignore[attr-defined]
                reporter=inliner.reporter, # type: ignore[attr-defined]
                language=inliner.language) # type: ignore[attr-defined]
            n, msgs = inliner.parse(self.text, self.lineno, memo, nodes[-1]) # type: ignore[attr-defined]
            if len(msgs) != 0:
                return [], msgs
            nodes[-1].replace(nodes[-1][0], n) # replace the Text node

        # Composite all nodes together, for examle:
        #
        # before::
        #
        #   <strong>
        #       <text>
        #   <literal>
        #       <text>
        #
        # after::
        #
        #   <strong>
        #       <literal>
        #            <text>
        for i in range(0, len(nodes) -1):
            nodes[i].replace(nodes[i][0], nodes[i+1]) # replace the Text node with the inner(i+1) TextElement

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
