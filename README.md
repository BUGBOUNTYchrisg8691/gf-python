# gf-python
Port of Tom Hudson's gf, wrapper for grep, in Python, because I could not get the Go version to work for the life of me.


# Installation
- Simply download the grep-for.py and add to path.

# Usage
grep-for.py [-h] -m MODE [-p PATTERN] [-f FILE]

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  mode of operation: list, dump, add, op
  -p PATTERN, --pattern PATTERN
                        pattern/flags to be passed to grep from json config
                        files: aws-keys, base64, cors, debug-pages, firebase,
                        fw, go-functions, http-auth, ip, json-sec, meg-
                        headers, php-curl, php-errors, php-serialized, php-
                        sinks, php-sources, s3-buckets, sec, servers, strings,
                        takeovers, upload-fields, urls
  -f FILE, --file FILE
                        grep this file
                        
# Additional
This is one of my first programs so any additional help or advice with the code operation or really anything would be greatly appreciated. Thank you in advance.

May 29, 2020
The "urls" functionality is broken. At least, I believe it is. Regardless, I'll be fixing it today, as well as discovering what other functionality might be broken as well. Probably should've tested it a bit more thoroughly, and not been so overly excited to rush to commit it.
(UPDATE) These issues have been resolved. I have completed a more thorough debug and I've found and fixed a few more issues. I am still very unsure of the soundness of the actual regex itself. I have very basic knowledge of regex and even though it is an exact copy of what was uploaded by Tom Hudson, I am not completely sure if this program is properly handling the data. I took some steps to ensure that it is to my best knowledge.  I am hoping to talk to someone this week that know regex far better than I do and I will have the answers then and will fix any issues that still exist. I'm hoping the handling of the regex is correct already, though. Will continue to post any issues that arise and fix them as soon as possible. 
(UPDATE) May 31, 2020 - It's broken. I'm looking into it, today. I messed around and screwed it far beyond what it was as far as bugs go.
(UPDATE) June 17, 2020 - Fixed. No add functionality or multiple patterns/files, yet, but all other functionality has been restored. JSON examples file has been converted to an in-script dictionary, as well.
