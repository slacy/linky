import os
import markdown
from jinja2 import Environment, FileSystemLoader, Template

# Recursively find all text files
# Process files into lists of words
# Process bigrams and trigram frequency
# Create list of bigrams and trigrams that occur more than once
# filter out bigrams and trigrams that start or end with a stopword
# Create mapping from N-gram to list of documents that contain in
# reprocess all documents, generating links for every N-gram


def find_corpus(root, suffix):

    def visit(md_files, dirname, names):
        md_files += [os.path.join(dirname, fn)
                     for fn in names if fn.endswith(suffix)]

    md_files = []
    os.path.walk(root, visit, md_files)
    return md_files


def find_layout(filepath):
    fullpath = os.path.abspath(filepath)
    while fullpath != '/':
        base = os.path.dirname(fullpath)
        layout = os.path.join(base, '_layout/layout.html')
        if os.path.exists(layout):
            return layout
        fullpath = base
    return None


def find_root(filepath):
    fullpath = os.path.abspath(filepath)
    while fullpath != '/':
        dirname = os.path.dirname(fullpath)
        root = os.path.join(dirname, '_root')
        if os.path.exists(root):
            return dirname
        fullpath = base
    return None


def compile(filename):
    root = find_root(filename)
    layout = find_layout(filename)
    jinja2_env = Environment(loader=FileSystemLoader(root))
    out_file = open(filename.replace('.md', '.html'), 'w+')
    in_file = open(filename)
    html = markdown.markdown(in_file.read())
    template = Template(layout_file.read())
    out_file.write(html)
    out_file.close()
    in_file.close()


def main():
    corpus = find_corpus(os.curdir, '.md')
    for filename in corpus:
        compile(filename)

if __name__ == '__main__':
    main()
