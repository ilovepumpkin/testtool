#! /usr/bin/perl -w
use strict;
use Net::SCP::Expect;
use Net::SSH::Expect;
use Net::SSH::Perl;

my $node = "9.186.12.78";
my $node_pwd = "l0destone";
my $node_user = "root";
my $ssh_port = 26;

print "Login the cluster.....\n";
my $ssh = Net::SSH::Expect->new(
    raw_pty => 1,
	host => $node,
	password => $node_pwd,
	user => $node_user,
	port => $ssh_port,
	timeout => 30);
my $test = $ssh->login();

#Check the node status ONLINE
my $node_status_result = $ssh->exec("svcinfo lsnode | awk '{if(NR==2){print }}'");
my @status = split(/\n/, $node_status_result);

my $node_status = $status[1];
while($node_status !~ m/online/){
	print "Error in cluster, please make nodes as candidate status then run the script.\n"
}
=pod
#Get the umanaged mdisk ID
my $mdisk_cmd = $ssh ->exec("svcinfo lsmdisk -filtervalue status=online | grep unmanaged");
my @mdisk = split(/\n/, $mdisk_cmd);

my $count=0;
my $mdisk_id;

while($count<@mdisk){
	if($mdisk[$count] =~ m/mdisk\d/){
		my @mdisk_area = split(/mdisk\d/, $mdisk[$count]);
		$mdisk_id .= $mdisk_area[0].":";
	}
	$count++;
}
$mdisk_id =~ s/\s+//g;
$mdisk_id = substr($mdisk_id,0,length($mdisk_id)-1);
print "mdiskid= $mdisk_id";

#Create default mdiskgrp0
my $mdiskgrp_cmd ="svctask mkmdiskgrp -name Auto_mdiskgrp -easytier auto -ext 32 -guiid 0 -mdisk $mdisk_id -warning 80%";
my $mdiskgrp_result = $ssh->exec($mdiskgrp_cmd);
print "restult $mdiskgrp_result\n";
my @mdiskgrp = split(/\n/, $mdiskgrp_result);

my $mdiskgrp_status = $mdiskgrp[0];
if($mdiskgrp_status !~ m/successfully/){

}

print "Create mdiskgrp Auto_mdiskgrp: $mdiskgrp_status\n";
=cut	
#Create generic vdisks
#my $genericVdisk_cmd= "for i in {0..50}; do svctask mkvdisk -mdiskgrp mdiskgrp0 -iogrp 0 -size 1 -unit gb -name lynn_fvt_gen_$i; done";
my $vdisk_count=0;
my $vdisk;
while($vdisk_count <=29){

    $vdisk = $ssh->exec("svctask mkvdisk -mdiskgrp Auto_mdiskgrp -iogrp 0 -size 1 -unit mb -name Auto_lynn_gen_$vdisk_count");
	if($vdisk !~ m/successfully/){
		print "Fail to create generic vdisk, please check the running task.";
	}
	else {
		my @vdisk_res = split(/\n/,$vdisk);
		print "Create Vdisk: $vdisk_res[1]\n";
	}
	$vdisk_count++;
}

sleep(1800);
