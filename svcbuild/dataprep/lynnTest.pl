#!/usr/bin/perl -w
use strict;
use Net::SSH::Expect;
use warnings;


my $host = '9.123.196.222';
my $user = 'root';
my $password = 'l0destone';
my $port='26';
		
my $ssh = Net::SSH::Expect->new(
	host => $host,
	password => $password,
	user=> $user,
	port =>$port,
	timeout => 10);

$ssh->login();

my ($stdout,$stderr,$exit) = $ssh->exec("df -h");
#$ssh->exec("exit");
if($stderr){
   print "ErrorCode:$exit\n";
   print "ErrorMsg:$stderr";
} else {
   print $stdout;
}
exit $exit;
