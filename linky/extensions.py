"""Jinja2 extensions for linky static site generator"""
import simplejson
import markdown2
from jinja2.ext import Extension
from jinja2.nodes import CallBlock, Const


class MarkdownExtension(Extension):
    """A markdown tag for Jinja2"""
    tags = set(['markdown'])

    def __init__(self, environment):
        super(MarkdownExtension, self).__init__(environment)
        environment.extend(markdowner=markdown2.Markdown())

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        body = parser.parse_statements(
            ['name:endmarkdown'],
            drop_needle=True
        )
        return CallBlock(
            self.call_method('_markdown_support'),
            [],
            [],
            body
        ).set_lineno(lineno)

    def _markdown_support(self, caller):
        """WAT"""
        return self.environment.markdowner.convert(caller()).strip()


class MetaExtension(Extension):
    """A markdown tag for Jinja2"""
    tags = set(['meta'])

    def __init__(self, environment):
        super(MetaExtension, self).__init__(environment)
        if not hasattr(environment, 'metamap'):
            environment.extend(metamap={})

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        body = parser.parse_statements(
            ['name:endmeta'],
            drop_needle=True
        )
        args = [Const(parser.name)]
        return CallBlock(
            self.call_method('_meta_support', args),
            [],
            [],
            body
        ).set_lineno(lineno)

    def _meta_support(self, template_name, caller):
        # self.environment.metamap.update()
        python_data = simplejson.loads(caller())
        self.environment.metamap.update({template_name: python_data})
        return "<!-- %s -->" % str(python_data)
