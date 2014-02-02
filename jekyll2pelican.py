# -*- coding: utf-8 -*-
#!/usr/bin/env python

import argparse
import codecs
import os
import re
import yaml


__doc__ = """
To convert Jekyll Markdown files into Pelican Markdown files
Features: 1. Metadata conversion, 2. Code conversion
(from {% highlight <lang> %} block)
"""

BLOG_AUTHOR = "Aravinda VK"
pelican_metadata = ['title', 'slug', 'author', 'date',
                    'tags', 'category', 'summary']


def _get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('jekyll_dir',
                        help='Path to the jekyll source files(_posts)')
    parser.add_argument('pelican_dir',
                        help='path to the output directory(content)')
    return parser.parse_args()


def _image_captions(lines):
    """
    I am replacing Image captions
    Old: <span class="imgCaption">Caption</span>
    New: *Caption*
    """
    body = []
    for line in lines:
        m = re.match('<(span|div)\sclass="imgCaption">(.+)</(span|div)>', line)
        if m:
            body.append("*%s*" % m.group(2))
        else:
            body.append(line)

    return body


def _ignore_lines(lines):
    """
    Earlier I used some custom spacers to make content look
    good in website, now I am achieving the same using
    css styles, so removing them
    """
    body = []
    for line in lines:
        if not line.startswith('<div class="sep') and \
           not line.startswith('<div class="clear') and \
           not line.startswith('<div class="clear" style='):
            line = line.replace("(/photo/", "(/images/")
            line = re.sub("<br/>$", "  ", line)
            body.append(line)

    return body


def _pelican_code(lines):
    """
    In jekyll code block is highlighted as
    {% highlight python %}
    def hello():
        print "hello"
    {% endhighlight %}

    In pelican code blocks can be highlighted
    by just using :::
        :::python
        def hello():
            print "hello"
    """
    in_code = False
    op = []
    for line in lines:
        m = re.match('{% highlight\s(\S+)\s%}', line)
        if m and not in_code:
            in_code = True
            op.append("    :::%s" % m.group(1))
        elif line.startswith('{% endhighlight %}') and in_code:
            in_code = False
        elif in_code:
            op.append("    %s" % line)
        else:
            op.append(line)
    return op


def _pelican_body(body):
    """
    Converts code syntax highlight style, image captions and removes
    old unused html.
    """
    body = _pelican_code(body)
    body = _image_captions(body)
    body = _ignore_lines(body)
    return "\n".join(body)


def _get_md_files(path):
    """
    Returns sorted list of Markdown files from jekyll directory
    """
    files = os.listdir(path)
    full_path_func = lambda f: os.path.join(path, f)
    is_md_func = lambda f: os.path.splitext(f)[1] in ('.md', '.markdown')
    md_files = [full_path_func(f) for f in files if is_md_func(f)]
    md_files.sort()
    return md_files


def _pelican_meta_lines(jekyll_meta):
    """
    Convert jekyll style meta into Pelican style meta.
    """
    meta_lines = []
    for i in pelican_metadata:
        if i in jekyll_meta:
            val = jekyll_meta[i]
            if type(jekyll_meta[i]) == list:
                vals = [unicode(x) for x in jekyll_meta[i]]
                val = ",".join(vals)

            meta_lines.append("%s: %s" % (i.capitalize(), val))

    return "\n".join(meta_lines)


def _parse(lines, file_date, slug):
    """
    Parse Metadata and Content from jekyll markdown file,
    Convert jekyll metadata into Pelican metadata. Also
    converts the content to Pelican form.

    Returns Pelican markdown file content.
    """
    metadata_lines = []
    body_lines = []
    is_metadata = False
    for line in lines:
        if line == '---' and not is_metadata:
            is_metadata = True
        elif line == '---' and is_metadata:
            is_metadata = False
        elif is_metadata:
            metadata_lines.append(line)
        else:
            body_lines.append(line)

    metadata = yaml.load('\n'.join(metadata_lines))
    metadata["slug"] = slug
    if "desc" in metadata:
        metadata["summary"] = metadata["desc"]
        del metadata["desc"]

    if "categories" in metadata:
        metadata["category"] = metadata["categories"]
        del metadata["categories"]

    if "date" not in metadata:
        metadata["date"] = file_date

    if "author" not in metadata:
        metadata["author"] = BLOG_AUTHOR

    return "%s\n\n%s" % (_pelican_meta_lines(metadata),
                         _pelican_body(body_lines))


def jekyll_to_pelican(idx, filepath, pelican_dir):
    """
    Converts jekyll markdown file into Pelican markdown file,
    <YY>-<MM>-<DD>-blog-post-slug.markdown into
    XXXX-blog-post-slug.md
    where XXXX is the number(idx) given to that blog post
    """
    with codecs.open(filepath, "r", "utf-8") as f:
        name, ext = os.path.splitext(os.path.basename(filepath))
        file_date = "-".join(name.split("-")[0:3])
        slug = '-'.join(name.split('-')[3:])
        pelican_file_name = '%s-%s.md' % (str(idx).zfill(4), slug)

        lines = (line.rstrip('\n') for line in f)
        content = _parse(lines, file_date, slug)

        with codecs.open(os.path.join(pelican_dir, pelican_file_name),
                         'w', 'utf-8') as f:
            f.write(content)

        print "[OK] processed %s ==> %s" % (filepath, pelican_file_name)


if __name__ == "__main__":
    args = _get_args()
    jekyll_md_files = _get_md_files(args.jekyll_dir)

    for idx, f in enumerate(jekyll_md_files):
        jekyll_to_pelican(idx, f, args.pelican_dir)
