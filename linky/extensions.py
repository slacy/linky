"""Jinja2 extensions for linky static site generator"""
import simplejson
import markdown2
from jinja2.ext import Extension
from jinja2 import nodes


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
        return nodes.CallBlock(
            self.call_method('_markdown_support'),
            [],
            [],
            body
        ).set_lineno(lineno)

    def _markdown_support(self, caller):
        """WAT"""
        return self.environment.markdowner.convert(caller()).strip()


class LinkExtension(Extension):
    """A link tag for Jinja2"""
    tags = set(['link'])

    def parse(self, parser):
        stream = parser.stream
        tag = stream.next()

        args = []
        while not parser.stream.current.test_any('block_end'):
            args.append(parser.parse_expression())

        make_call_node = lambda: self.call_method(
            '_link_support', args=args)

        return nodes.Output([make_call_node()]).set_lineno(tag.lineno)

    def _link_support(self, page_title):
        """WAT"""
        if self.environment.pre_process:
            return page_title

        inbound = None
        for template, meta in self.environment.metamap.iteritems():
            if 'inbound' in meta and page_title in meta['inbound']:
                inbound = template

        if not inbound:
            raise Exception("Can't find inbound link for '%s'" % page_title)
        return "<Link to %s titled %s>" % (inbound, page_title)



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
        args = [nodes.Const(parser.name)]
        return nodes.CallBlock(
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
