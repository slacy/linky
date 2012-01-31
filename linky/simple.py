"""yo gabba"""
import os
from jinja2 import Environment, FileSystemLoader
from jinja2.ext import Extension
from jinja2.nodes import CallBlock
import markdown2

# Recursively find all text files
# Process files into lists of words
# Process bigrams and trigram frequency
# Create list of bigrams and trigrams that occur more than once
# filter out bigrams and trigrams that start or end with a stopword
# Create mapping from N-gram to list of documents that contain in
# reprocess all documents, generating links for every N-gram


class MarkdownExtension(Extension):
    """A markdown tag for Jinja2"""
    tags = set(['markdown'])

    def __init__(self, environment):
        super(MarkdownExtension, self).__init__(environment)
        environment.extend(
            markdowner=markdown2.Markdown()
        )

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


def find_corpus(root, suffix):
    """find_corpus"""

    def visit(_found, dirname, names):
        """visit"""
        new = [os.path.abspath(os.path.join(dirname, fn))
               for fn in names if fn.endswith(suffix)]
        _found += new

    found_files = []

    os.path.walk(root, visit, found_files)
    return found_files


def find_layout(filepath):
    """find_layout"""
    fullpath = os.path.abspath(filepath)
    while fullpath != '/':
        base = os.path.dirname(fullpath)
        layout = os.path.join(base, '_layout', 'layout.html')
        if os.path.exists(layout):
            return layout
        fullpath = base
    return None


def find_root(filepath):
    """find_root"""
    fullpath = os.path.abspath(filepath)
    while fullpath != '/':
        dirname = os.path.dirname(fullpath)
        root = os.path.join(dirname, '_root')
        if os.path.exists(root):
            return dirname
        fullpath = dirname
    return None


class Preprocessor(object):
    """Preprocessor"""

    def __init__(self):
        self.content = {}

    def compile(self, filename):
        """compile"""

        print "compiling %s" % filename
        root = find_root(filename)
        print "root is %s" % root
        env = Environment(loader=FileSystemLoader(root), extensions=[MarkdownExtension])
        out_filename = filename.replace('.jinja2', '.html')
        out_file = open(out_filename, 'w+')
        # html = open(filename, 'r').read()

        template_relative = filename.replace(root, '')
        template = env.get_template(template_relative)
        final = template.render()
        out_file.write(final)
        out_file.close()


def main():
    """main"""
    corpus = find_corpus(os.curdir, '.jinja2')

    pre = Preprocessor()

    for filename in corpus:
        pre.compile(filename)

if __name__ == '__main__':
    main()
