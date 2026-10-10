#!/bin/python
# -*- coding: utf-8 -*-
# post process script for adding comments on html files
import re
import sys


# read html file
if len(sys.argv) < 1:
    print("python process.py <文件名>")
    exit(1)

source = sys.argv[1]
content = ''

with open(source, 'r') as f:
    content = f.read()

# append these lines before "<title>"
scripts = '''
<!-- comment.js -->
<link rel="stylesheet" href="/comment.css"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/0.3.6/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/timeago.js/3.0.2/timeago.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/spin.js/2.3.2/spin.min.js"></script>
<script src="/comment.js"></script>
<style type="text/css">
 #comment-thread {
	 padding-top: 7em;
	 margin-left: 45px;
	 margin-right: 45px;
 }
</style>	
<script type="text/javascript">
 var opt = {
	 type: "github",
	 user: "wzpan",
	 repo: "wzpan.github.io",
	 no_comment: "暂无评价呢",
	 go_to_comment: "去评价我",
	 issue_id: "11",
	 btn_class: "btn",
	 comments_target: "#comment-thread",
	 client_id: "1eb35434de75c06a513f",
	 client_secret: "6e4193f8ecd619cdfac2b1aa16b3663fe18d2e90"
 };
 getComments(opt);
</script>
<title></title>
'''

content = content.replace('<title></title>', scripts)

# append this line to the end of <div class="pc pc3 w0 h0">
comment = '''
<div id="comment-thread"></div>
'''

# The font class name (e.g. ffb, ffc) depends on how many fonts pdf2htmlEX
# extracts from the PDF, so match any of them instead of hard-coding one.
def inject(sentence, content):
    pattern = re.compile(re.escape(sentence) + '<span class="ff[a-z0-9]+">\\.</span></div>')

    def repl(m):
        return '你认识我吗？给我发表评价吧' + m.group(0)[len(sentence):] + comment

    return pattern.sub(repl, content)

content = inject('你认识我吗？给我发表评价吧', content)
content = inject('Do you know me? Please comment on me', content)

# The English sentence is split into one span per word by pdf2htmlEX, so match
# the whole line (up to the closing </div>) instead of a single contiguous run.
def inject_en(content):
    anchor = content.find('<div id="page-container">')
    if anchor < 0:
        return content
    head, tail = content[:anchor], content[anchor:]
    pattern = re.compile(r'>Do(?:(?!</div>)[\s\S])*?me<span class="ff[a-z0-9]+">\.</span></div>')
    match = pattern.search(tail)
    if match:
        tail = tail[:match.end()] + comment + tail[match.end():]
    return head + tail

content = inject_en(content)

with open(source, 'w') as f:
    f.write(content)
