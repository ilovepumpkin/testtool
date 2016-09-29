#!/usr/bin/perl -w
use strict;


my $a = "1:2:3:4:5:6:8:9:10:13:14:15:16:17:18:19:20:21:22:23:[11:30:06]lepus-a:~#:";
$a =~ s/\s+//g;
$a =~ s/\:\[.+//g;

#y $a = substr($str,0,-1);
print "a=$a\n";
