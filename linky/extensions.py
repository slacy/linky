"""Jinja2 extensions for linky static site generator"""
import os
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

        args = [nodes.Const(parser.name), nodes.Name('ROOT', 'load')]
        while not parser.stream.current.test_any('block_end'):
            args.append(parser.parse_expression())

        make_call_node = lambda: self.call_method(
            '_link_support', args=args)

        return nodes.Output([make_call_node()]).set_lineno(tag.lineno)

    def _link_support(self, this_page, root, page_title):
        """WAT"""

        if self.environment.pre_process:
            return page_title

        inbound = None
        for template, meta in self.environment.metamap.iteritems():
            if 'inbound' in meta and page_title in meta['inbound']:
                inbound = template

        if not inbound:
            raise Exception("Can't find inbound link for '%s'" % page_title)

        # (inbound_dir, inbound_file) = os.path.split(inbound)
        # (this_dir, _this_file) = os.path.split(this_page)
        # relative_dir = os.path.relpath(inbound_dir, this_dir)
        # relative_filename = os.path.join(relative_dir, inbound_file)
        absolute_filename = os.path.join(root, inbound.strip('/'))

        href = absolute_filename.replace(".jinja2", ".html")
        result = '<a href="%s">%s</a>' % (href, page_title)
        return result


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
