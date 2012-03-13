#!/usr/bin/python
# To Export custom comments into Disqus format
# The MIT License (MIT)
# Copyright (c) 2012 Aravinda VK<hallimanearavind@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import requests
import json
import os
import datetime

DISQUS_URL = "http://disqus.com/api/3.0"
SECRET_KEY = "<YOUR SECRET KEY>"
FORUM = "<FORUM ID>"
CREATE_THREAD_URL = DISQUS_URL + "/threads/create.json?api_secret=" + SECRET_KEY
THREADS_LIST_URL = DISQUS_URL + "/threads/list.json?api_secret=" + SECRET_KEY + "&forum=" + FORUM + "&limit=100"
POST_COMMENT_URL = DISQUS_URL + "/posts/create.json?api_secret=" + SECRET_KEY

urls_and_threads = {}
r= requests.get(THREADS_LIST_URL)
threads_list = json.loads(r.content)

# Build existing threads lookup
for th in threads_list["response"]:
    urls_and_threads[th["link"]] = th["id"]

def post_comment(url, title, author_name, author_email, author_url, comment_date, message, ip_address):
    # If Thread exists then don't create it
    if urls_and_threads.has_key(url):
        thread_id = urls_and_threads[url]
        print "[OK] thread exists ", url, " ", thread_id
    else :
        post_vars = {"forum" : FORUM, "title" : title, "url" : url}
        r = requests.post(CREATE_THREAD_URL, post_vars)
        thread_data = json.loads(r.content)
        thread_id = thread_data["response"]["id"]
        urls_and_threads[url] = thread_id
        print "[OK] thread created ", url, " ", thread_id


    # Add comment
    comment = {"thread" : thread_id,
               "message" : message,
               "author_name" : author_name,
               "date" : comment_date,
               "author_email" : author_email,
               "state" : "approved",
               "author_url" : author_url,
               "ip_address" : ip_address}
    
    r = requests.post(POST_COMMENT_URL, data=comment)

    # If response code is not zero, that means Some error
    if json.loads(r.content)["code"] > 0:
        print json.loads(r.content)



     
path = 'avk_comments/json/'
listing = os.listdir(path)
# Each comment is a JSON file in avk_comments/json folder
for infile in listing:
    data = json.load(open(path + infile))
    if data["enabled"] == 1:
        post_comment("http://aravindavk.in/blog/" + data["content_id"] + "/",
                     data["content_id"],
                     data["name"],
                     data["email"],
                     data["web"],
                     datetime.datetime.strptime(data["when_created"], "%m/%d/%Y %H:%M:%S").isoformat(),
                     data["comment"],
                     data["user_ip"])
        print "[OK] done ", data["_id"]
