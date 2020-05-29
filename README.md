# gf-python
Port of Tom Hudson's gf, wrapper for grep, in Python, because I could not get the Go version to work for the life of me.


# Installation
- Simply download the main.py and examples directory.
- Create .gf directory in $HOME directory, move examples directory into .gf directory.
  - Or put it wherever you would like and make sure you change the "base_dir" variable of the "get_pattern_dir" function in     main.py to the location of the examples directory.
- Add file execution to path or alias it, or however you prefer.
  - I usually add the line 'alias gf="python3 <path/to/main.py>"' to my .bash_aliases file.
  - Open terminal and execute 'source ~/.bashrc'
- ... and you are good to go.

# Usage
main.py [-h] -m MODE [-p PATTERN [PATTERN ...]] [-f FILES [FILES ...]]

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  mode of operation: list, dump, op
  -p PATTERN [PATTERN ...], --pattern PATTERN [PATTERN ...]
                        pattern/flags to be passed to grep from json config
                        files: aws-keys, base64, cors, debug-pages, firebase,
                        fw, go-functions, http-auth, ip, json-sec, meg-
                        headers, php-curl, php-errors, php-serialized, php-
                        sinks, php-sources, s3-buckets, sec, servers, strings,
                        takeovers, upload-fields, urls
  -f FILES [FILES ...], --files FILES [FILES ...]
                        grep in this folder or file
                        
# Additional
This is one of my first programs so any additional help or advice with the code operation or really anything would be greatly appreciated. Thank you in advance.

May 29, 2020
The "urls" functionality is broken. I'll be fixing it today, as well as discovering what other functionality might be broken as well. Probably should've tested it a bit more thoroughly.
