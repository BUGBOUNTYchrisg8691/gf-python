#!/bin/bash/env python3

# Grep-For-Python - A grep wrapper based on Tom Hudson's (https://github.com/tomnomnom) "gf"

import argparse
import os
import subprocess

examples = {'aws-keys': {
    "flags": "-HanrE",
    "pattern": r"([^A-Z0-9]|^)(AKIA|A3T|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{12,}"
    }, 'base64': {
    "flags": "-HnroE",
    "pattern": r"([^A-Za-z0-9+/]|^)(eyJ|YTo|Tzo|PD[89]|aHR0cHM6L|aHR0cDo|rO0)[%a-zA-Z0-9+/]+={0,2}"
    }, 'cors': {
    "flags": "-HnriE",
    "pattern": [
        r"Access-Control-Allow"
    ]}, 'debug-pages': {
    "flags": "-HnraiE",
    "pattern": r"(Application-Trace|Routing Error|DEBUG\"? ?[=:] ?True|Caused by:|stack trace:|Microsoft .NET Framework|Traceback|[0-9]:in `|#!/us|WebApplicationException|java\\.lang\\.|phpinfo|swaggerUi|on line [0-9]|SQLSTATE)"
    }, 'firebase': {
    "flags": "-Hnri",
    "pattern": r"firebaseio.com"
    }, 'fw': {
    "flags": "-HnriE",
    "pattern": [
        r"django",
        r"laravel",
        r"symfony",
        r"graphite",
        r"grafana",
        r"X-Drupal-Cache",
        r"struts",
        r"code ?igniter",
        r"cake ?php",
        r"grails",
        r"elastic ?search",
        r"kibana",
        r"log ?stash",
        r"tomcat",
        r"jenkins",
        r"hudson",
        r"com.atlassian.jira",
        r"Apache Subversion",
        r"Chef Server",
        r"RabbitMQ Management",
        r"Mongo",
        r"Travis CI - Enterprise",
        r"BMC Remedy",
        r"artifactory"
    ]}, 'go-functions': {
    "flags": "-HnriE",
    "pattern": r"func [a-z0-9_]+\\("
    }, 'http-auth': {
    "flags": "-hrioaE",
    "pattern": r"[a-z0-9_/\\.:-]+@[a-z0-9-]+\\.[a-z0-9.-]+"
    }, 'ip': {
    "flags": "-HnroE",
    "pattern": r"(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
    }, 'json-sec': {
    "flags": "-harioE",
    "pattern": r"(\\\\?\"|&quot;|%22)[a-z0-9_-]*(api[_-]?key|S3|aws_|secret|passw|auth)[a-z0-9_-]*(\\\\?\"|&quot;|%22): ?(\\\\?\"|&quot;|%22)[^\"&]+(\\\\?\"|&quot;|%22)"
    }, 'meg-headers': {
    "flags": "-hroiE",
    "pattern": r"^\u003c [a-z0-9_\\-]+: .*"
    }, 'php-curl': {
    "flags": "-HnrE",
    "pattern": r"CURLOPT_(HTTPHEADER|HEADER|COOKIE|RANGE|REFERER|USERAGENT|PROXYHEADER)"
    }, 'php-errors': {
    "flags": "-HnriE",
    "pattern": [
        r"php warning",
        r"php error",
        r"fatal error",
        r"uncaught exception",
        r"include_path",
        r"undefined index",
        r"undefined variable",
        r"\\?php",
        r"<\\?[^x]",
        r"stack trace\\:",
        r"expects parameter [0-9]*",
        r"Debug Trace"
    ]}, 'php-serialized': {
    "flags": "-HnrE",
    "pattern": [
        r"a:[0-9]+:{",
        r"O:[0-9]+:\"",
        r"s:[0-9]+:\""
    ]}, 'php-sinks': {
    "flags": "-HnriE",
    "pattern": r"[^a-z0-9_](system|exec|popen|pcntl_exec|eval|create_function|unserialize|file_exists|md5_file|filemtime|filesize|assert) ?\\("
    }, 'php-sources': {
    "flags": "-HnrE",
    "pattern": [
        r"\\$_(POST|GET|COOKIE|REQUEST|SERVER|FILES)",
        r"php://(input|stdin)"
    ]}, 's3-buckets': {
    "flags": "-hrioaE",
    "pattern": [
        r"[a-z0-9.-]+\\.s3\\.amazonaws\\.com",
        r"[a-z0-9.-]+\\.s3-[a-z0-9-]\\.amazonaws\\.com",
        r"[a-z0-9.-]+\\.s3-website[.-](eu|ap|us|ca|sa|cn)",
        r"//s3\\.amazonaws\\.com/[a-z0-9._-]+",
        r"//s3-[a-z0-9-]+\\.amazonaws\\.com/[a-z0-9._-]+"
    ]}, 'sec': {
    "flags": "-HanriE",
    "pattern": r"(aws_access|aws_secret|api[_-]?key|ListBucketResult|S3_ACCESS_KEY|Authorization:|RSA PRIVATE|Index of|aws_|secret|ssh-rsa AA)"
    }, 'servers': {
    "flags": "-hri",
    "pattern": r"server: "
    }, 'strings': {
    "flags": "-hroiaE",
    "pattern": [
        r"\"[^\"]+\"",
        r"'[^']+'"
    ]}, 'takeovers': {
    "flags": "-HnriE",
    "pattern": [
        r"There is no app configured at that hostname",
        r"NoSuchBucket",
        r"No Such Account",
        r"You're Almost There",
        r"a GitHub Pages site here",
        r"There's nothing here",
        r"project not found",
        r"Your CNAME settings",
        r"InvalidBucketName",
        r"PermanentRedirect",
        r"The specified bucket does not exist",
        r"Repository not found",
        r"Sorry, We Couldn't Find That Page",
        r"The feed has not been found.",
        r"The thing you were looking for is no longer here, or never was",
        r"Please renew your subscription",
        r"There isn't a Github Pages site here.",
        r"We could not find what you're looking for.",
        r"No settings were found for this company:",
        r"No such app",
        r"is not a registered InCloud YouTrack",
        r"Unrecognized domain",
        r"project not found",
        r"This UserVoice subdomain is currently available!",
        r"Do you want to register",
        r"Help Center Closed"
    ]}, 'upload-fields': {
    "flags": "-HnriE",
    "pattern": r"\u003cinput[^\u003e]+type=[\"']?file[\"']?"
    }, 'urls': {
    "flags": "-oriahE",
    "pattern": r"https?://[^\"\\'> ]+"
    }
}

def getFlagsPattern( name ):
    """Returns flags and regex to be passed to grep."""

    flags = examples[name]['flags']
    pattern = examples[name]['pattern']

    return flags, pattern

def main():
    """Formats grep string with proper flags and pattern, passes it to shell,
    and returns result."""

    parser = argparse.ArgumentParser()
    parser.add_argument( '-m', '--mode', nargs=1, dest='mode', required=True,
        help='mode of operation: list, dump, op, add')
    parser.add_argument( '-p', '--pattern', nargs='+', dest='pattern',
        help='pattern/flags to be passed to grep from json config files: ' \
        'aws-keys, base64, cors, debug-pages, firebase, fw, go-functions, ' \
        'http-auth, ip, json-sec, meg-headers, php-curl, php-errors, ' \
        'php-serialized, php-sinks, php-sources, s3-buckets, sec, servers, ' \
        'strings, takeovers, upload-fields, urls' )
    parser.add_argument( '-f', '--file', nargs='+', dest='file',
        help='file to be grep\'d' )
    args = parser.parse_args()
    if( args.mode[0] == 'list' ):
        patterns = examples.keys()
        for pattern in patterns:
            print( pattern )
    if( args.mode[0] == 'dump' ):
        flags, pattern = getFlagsPattern( args.pattern[0] )
        if( isinstance( pattern, str )):
            command = f'grep --color {flags} "{pattern}"'
        else:
            command = []
            for pat in pattern:
                command.append( f'grep --color {flags} "{pat}"')
        if( isinstance( command, str )):
            print( command )
        else:
            for com in command:
                print( com )
    if args.mode[0] == 'op':
        flags, pattern = getFlagsPattern( args.pattern[0] )
        if( isinstance( pattern, str )):
            command = f'grep --color {flags} "{pattern}"'
        if( isinstance( pattern, list )):
            command = []
            for pat in pattern:
                command.append( f'grep --color {flags} "{pat}"')
        if( isinstance( command, str )):
            proc = subprocess.run( command, shell=True, capture_output=True,
                text=True )
            if( proc.returncode == 0 ):
                print( proc )
                print( proc.stdout )
                print( 'This has been logged in an output file in your current directory.' )
                with open( 'output', 'a' ) as file:
                    file.write( proc.stdout )
            if( proc.returncode == 1 ):
                print( proc )
                print( 'Nothing was found with grep' )
            if( proc.returncode != 0 and proc.returncode != 1 ):
                print( 'There was an error processing your arguments. Errors have been logged.' )
                print( proc )
                print( proc.stderr )
                with open( 'error', 'a' ) as file:
                    file.write( proc.stderr )
        if( isinstance( command, list )):
            for com in command:
                print(com)
                proc = subprocess.run( com, shell=True, capture_output=True,
                    text=True )
                if( proc.returncode == 0 ):
                    print( proc )
                    print( proc.stdout )
                    print( 'This has been logged in an output file in your current directory.' )
                    with open( 'output', 'a' ) as file:
                        file.write( proc.stdout )
                if( proc.returncode == 1 ):
                    print( proc )
                    print( 'Nothing was found with grep' )
                if( proc.returncode != 0 and proc.returncode != 1 ):
                    print( 'There was an error processing your arguments. Errors have been logged.' )
                    print( proc )
                    print( proc.stderr )
                    with open( 'error', 'a' ) as file:
                        file.write( proc.stderr )

if __name__ == '__main__':
    main()