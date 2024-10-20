from __future__ import annotations
from typing import TYPE_CHECKING, cast
from dataclasses import dataclass

from sphinx.util import logging
from sphinx.util.docutils import SphinxRole
from sphinx.errors import ExtensionError

from docutils.nodes import Node, Inline, TextElement, system_message
from docutils.parsers.rst import roles
from docutils.parsers.rst import states

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.util.typing import RoleFunction

__version__ = '0.1.0'

logger = logging.getLogger(__name__)


@dataclass
class RoleMetaInfo(object):
    """Metainfo used to assist role composition."""

    name: str
    fn: RoleFunction


class CompositeRole(SphinxRole):
    #: Rolenames to be composited
    rolenames: list[str]
    #: Whether to enable :ref:`nested-parse`
    nested_parse: bool

    def __init__(self, rolenames: list[str], nested_parse: bool):
        self.rolenames = rolenames
        self.nested_parse = nested_parse

    def run(self) -> tuple[list[Node], list[system_message]]:
        reporter = self.inliner.reporter  # type: ignore[attr-defined]

        # NOTE: We should NOT lookup roles during __init__, some roles created by
        # 3rd-party extension do not exist yet at that time.
        roles = []
        for name in self.rolenames:
            role = self.lookup_role(name)
            if role is None:
                msg = reporter.error(f'no such role: {name}', line=self.lineno)
                return [], [msg]
            roles.append(role)

        # Run all RoleFunction, collect the produced nodes:
        #
        # - the innermost element `contnode` can be an Inline or TextElement,
        # - allother elements `wrapnodes` MUST be TextElement.
        wrapnodes: list[TextElement] = []
        contnode: TextElement | Inline | None = None
        for i, role in enumerate(roles):
            ns, msgs = role.fn(
                role.name,
                self.rawtext,
                self.text,
                self.lineno,
                self.inliner,
                self.options,
                self.content,
            )
            if len(msgs) != 0:
                return [], msgs  # once system_message is thrown, return
            if len(ns) != 1:
                msg = reporter.error(
                    f'role should returns exactly 1 node, but {len(ns)} found: {ns}',
                    line=self.lineno,
                )
                return [], [msg]
            n = ns[0]

            # So that it can be used as part of composite roles.
            innermost = i == len(roles) - 1
            classes = (Inline, TextElement) if innermost else TextElement
            if not isinstance(n, classes):
                msg = reporter.error(f'node {n} is not {classes}', line=self.lineno)
                return [], [msg]

            if innermost:
                contnode = n
            else:
                wrapnodes.append(cast(TextElement, n))

        if contnode is None:
            return [], []  # no node produced, return

        if self.nested_parse:
            if not isinstance(contnode, TextElement):
                msg = reporter.error(
                    f'can not do nested parse because node {contnode} is not {TextElement}',
                    line=self.lineno,
                )
                return [], [msg]
            contnode = cast(TextElement, contnode)

            # See also:
            #
            # - :ref:`nested-parse`
            # - https://stackoverflow.com/questions/44829580/composing-roles-in-restructuredtext
            inliner = self.inliner
            memo = states.Struct(
                document=inliner.document,  # type: ignore[attr-defined]
                reporter=inliner.reporter,  # type: ignore[attr-defined]
                language=inliner.language,
            )  # type: ignore[attr-defined]
            n, msgs = inliner.parse(self.text, self.lineno, memo, wrapnodes)  # type: ignore[attr-defined]
            if len(msgs) != 0:
                return [], msgs
            contnode.replace(contnode[0], n)  # replace the Text node

        # Composite all nodes together, for examle:
        #
        # before::
        #
        #   <strong> # wrapnodes[0]
        #       <text>
        #   <literal> # wrapnodes[1]
        #       <text>
        #   <pending_xref> # contnode
        #       <text>
        #
        # after::
        #
        #   <strong>
        #       <literal>
        #           <pending_xref>
        #              <text>
        allnodes = wrapnodes + [contnode]  # must not empty
        for i in range(0, len(allnodes) - 1):
            # replace the Text node with the inner(i+1) TextElement
            allnodes[i].replace(allnodes[i][0], allnodes[i + 1])

        return [allnodes[0]], []

    def lookup_role(self, name: str) -> RoleMetaInfo | None:
        """Lookup RoleFunction by name."""

        # Lookup in docutils' regsitry.
        if name in roles._roles:  # type: ignore[attr-defined]
            return RoleMetaInfo(name=name, fn=roles._roles[name])  # type: ignore[attr-defined]
        if name in roles._role_registry:  # type: ignore[attr-defined]
            return RoleMetaInfo(name=name, fn=roles._role_registry[name])  # type: ignore[attr-defined]

        # Lookup up in domain's regsitry.
        domains = []
        if ':' in name:  # explicit domain name
            dname, name = name.split(':', maxsplit=1)
            domains.append(dname)
        else:  # implicit, try primary_domain and std domain in order
            if self.config.primary_domain and self.config.primary_domain != '':
                domains.append(self.config.primary_domain)
            domains.append('std')
        for domain_name in domains:
            try:
                domain = self.env.get_domain(domain_name)
            except ExtensionError as e:
                logger.warn(f'failed to get domain: {e}')
                return None
            if name in domain.roles:
                return RoleMetaInfo(name=f'{domain_name}:{name}', fn=domain.roles[name])

        return None


def _config_inited(app: Sphinx, config: Config) -> None:
    for name, cfg in config.comboroles_roles.items():
        if isinstance(cfg, list):
            rolenames = cfg
            nested_parse = False
        else:
            rolenames = cfg[0]
            nested_parse = cfg[1]
        app.add_role(name, CompositeRole(rolenames, nested_parse))


def setup(app: Sphinx):
    """Sphinx extension entrypoint."""

    app.connect('config-inited', _config_inited)

    app.add_config_value(
        'comboroles_roles',
        {},
        'env',
        types=dict[str, list[str] | tuple[list[str], bool]],
    )

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
