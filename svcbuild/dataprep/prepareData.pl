#! /usr/bin/perl -w
###############################
# Prepare the data objects    #
# Author: Lynn                #
# Date: 2014.04               #
###############################
use strict;
use Net::SCP::Expect;
use Net::SSH::Expect;
use Net::SSH::Perl;
require "/var/www/cgi-bin/svc/code/common.pl";

my $cluster_ip;
my $cluster_pwd;
my $cluster_user;
my $cluster_port;
my $cluster_type;
my $is_mdiskgrp;
my $vdisk_gen;
my $vdisk_thinpro;
my $vdisk_mirror;
my $vdisk_thinmirror;
my $vdisk_compress;
my $host_fc;
my $host_iscsi;
my $host_sas;
my $host_vdisk_mapping;
my $fcmap;
my $fccg;
my $fcmap_add2_fccg;
my $rcrel;
my $rccg;
my $rcrel_add2_rccg;
my $user_sec;
my $user_adm;
my $user_copy;
my $user_service;
my $user_monitor;
my $usergrp;
my $user_add2_usergrp;
my $tmp_dest = "/tmp";
my $shell_path = "/SVC/script/lynn";


#Read configuration file and set the configure vaules
open CONF, "config";
while(<CONF>)
{       if($_ =~ m/^\s+$/)
        {
                next;
        }
        my $startchar = substr($_, 0, 1);
        if($startchar eq '#')
        {
                next;
        }
        my ($name, $value) = split(/==/, $_);
        $value =~ s/^\s+|\s+$//;
        if($name =~ m/cluster_ip/)
        {
                $cluster_ip = $value;
        }
         elsif($name =~ m/cluster_port/)
        {
                $cluster_port = $value;
        }
         elsif($name =~ m/cluster_user/)
        {
                $cluster_user = $value;
        }
        elsif($name =~ m/cluster_pwd/)
        {
                $cluster_pwd = $value;
        }
        elsif($name =~ m/cluster_type/)
        {
                $cluster_type = $value;
        }
        elsif($name =~ m/is_mdiskgrp/)
        {
                $is_mdiskgrp = $value;
        }
        elsif($name =~ m/vdisk_gen/)
        {
                $vdisk_gen = $value;
        }
        elsif($name =~ m/vdisk_thinpro/)
        {
                $vdisk_thinpro = $value;
        }elsif($name =~ m/vdisk_mirror/)
        {
                $vdisk_mirror = $value;
        }elseif($name =~ m/vdisk_thinmirror/)
	{
		$vdisk_thinmirror = $value;
	}
	elsif($name =~ m/vdisk_compress/)
        {
                $vdisk_compress = $value;
        }
        elsif($name =~ m/host_fc/)
        {
                $host_fc = $value;
        }
        elsif($name =~ m/host_iscsi/)
        {
                $host_iscsi = $value;
        }
        elsif($name =~ m/host_sas/)
        {
                $host_sas = $value;
        }
        elsif($name =~ m/host_vdisk_mapping/)
        {
                $host_vdisk_mapping = $value;
        }
        elsif($name =~ m/fcmap/)
        {
                $fcmap = $value;
        }elsif($name =~ m/fccg/)
        {
                $fccg = $value;
        }elseif($name =~ m/fcmap_add2_fccg/)
        {
                $fcmap_add2_fccg = $value;
        }
	elsif($name =~ m/rcrel/)
        {
                $rcrel = $value;
        }
        elsif($name =~ m/rccg/)
        {
                $rccg = $value;
        }
        elsif($name =~ m/rcrel_add2_rccg/)
        {
                $rcrel_add2_rccg = $value;
        }
        elsif($name =~ m/user_sec/)
        {
                $user_sec = $value;
        }
        elsif($name =~ m/user_adm/)
        {
                $user_adm = $value;
        }
        elsif($name =~ m/user_copy/)
        {
                $user_copy = $value;
        }elsif($name =~ m/user_service/)
        {
                $user_service = $value;
        }elseif($name =~ m/user_monitor/)
        {
                $user_monitor = $value;
        }elsif($name =~ m/usergrp/)
        {
                $usergrp = $value;
        }elseif($name =~ m/user_add2_usergrp/)
        {
                $user_add2_usergrp = $value;
        }



}
close CONF;



#Go through the ssh authentication, login the cluster
while(1){
	my $ssh = Net::SSH::Expect->new(
    		raw_pty => 1,
		host => $cluster_ip,
		password => $cluster_pwd,
		user => $cluster_user,
		port => $cluster_port,
		timeout => 30);
	 	$ssh->login();

#Get the cluster type
if($cluster_type =~ m/SVC/){
	if($is_mdiskgrp =~ m/No/){
	my $get_mdisk = $ssh ->exec("svcinfo lsmdisk -filtervalue status=online | grep unmanaged");
	my @mdisk = split(/\n/, $get_mdisk);

	my $mdisk_count=0;
	my $mdisk_id;

	while($mdisk_count<@mdisk){
		print "$mdisk_count";
        	if($mdisk[$mdisk_count] =~ m/mdisk\d/){
                	my @mdisk_area = split(/mdisk\d/, $mdisk[$mdisk_count]);
                	$mdisk_id .= $mdisk_area[0].":";
        	}
        	$mdisk_count++;
	}
	$mdisk_id =~ s/\s+//g;
	$mdisk_id = substr($mdisk_id,0,length($mdisk_id)-1);
	print "mdiskid= $mdisk_id\n";
	
       #Create mdiskgrp Auto_mdiskgrp0
        my $mdiskgrp_cmd ="svctask mkmdiskgrp -name Auto_mdiskgrp0 -easytier auto -ext 32 -guiid 0 -mdisk $mdisk_id -warning 80%";
        my $mdiskgrp_result = $ssh->exec($mdiskgrp_cmd);
        #print "create SVC family mdiskgrp result:$mdiskgrp_result\n";

	}elseif($is_mdiskgrp =~ m/Yes/){
		print "You have manual created mdiskgrp Auto_mdiskgrp0. \n";
	}
}
elseif($cluster_type =~ m/V7000/){
	

	if($is_mdiskgrp =~ m/No/){
        	my $get_mdisk = $ssh ->exec("svcinfo lsmdisk -filtervalue status=online | grep unmanaged");
        	my @mdisk = split(/\n/, $get_mdisk);

        	my $mdisk_count=0;
        	my $mdisk_id;

       		while($mdisk_count<@mdisk){
                	print "$mdisk_count";
                	if($mdisk[$mdisk_count] =~ m/mdisk\d/){
                        	my @mdisk_area = split(/mdisk\d/, $mdisk[$mdisk_count]);
                       	 	$mdisk_id .= $mdisk_area[0].":";
                	}
               		$mdisk_count++;
        	}
        	$mdisk_id =~ s/\s+//g;
        	$mdisk_id = substr($mdisk_id,0,length($mdisk_id)-1);
        	print "mdiskid= $mdisk_id\n";

       		#Create mdiskgrp Auto_mdiskgrp0
        	my $mdiskgrp_cmd ="svctask mkmdiskgrp -name Auto_mdiskgrp0 -easytier auto -ext 32 -guiid 0 -mdisk $mdisk_id -warning 80%";
       	 	my $mdiskgrp_result = $ssh->exec($mdiskgrp_cmd);
        	#print "create V7000 family mdiskgrp result:$mdiskgrp_result\n";

       	 	}elseif($is_mdiskgrp =~ m/Yes/){
                	print "You have manual created mdiskgrp Auto_mdiskgrp0. \n";
        	}
}else{
	print "The cluster type is wrong, exit.\n";
}






# Copy the create vdisk shell script to server
my $vdiskShell_path = "$shell_path/volumesCommand.sh";
&copyFile2Server($node,$node_user,$node_pwd,$ssh_port,$vdiskShell_path,$tmp_dest);
# Invoke the volumes shell script
#(SHELL Generic,Thin-provision,Mirror,Thin-mirror,compressed)
my $vdisk = $ssh ->exec("sh $tmp_dest/volumesCommand.sh 200 100 100 100 100");
print "vdisk result: $vdisk\n";
sleep(100);


# Get the cluster name or id
my $cluster_cmd="svcinfo lscluster | grep 00000";
my $cluster_res = $ssh -> exec($cluster_cmd);
my @cluster = split(/\n/,$cluster_res);

my $cluster_id_res = $cluster[1];
my $cluster_id = substr($cluster_id_res,0,16);


# Copy the copyservice shell script to server
my $copyServiceShell_path = "$shell_path/copyservicesCommand.sh";
&copyFile2Server($node,$node_user,$node_pwd,$ssh_port,$copyServiceShell_path,$tmp_dest);
# Invoke the copyservices shell script
my $copyservice = $ssh ->exec("sh $tmp_dest/copyservicesCommand.sh $cluster_id");
print "copy services result: $copyservice\n";
sleep(100);

# Copy the host shell script to server
my $hostShell_path = "$shell_path/hostCommand.sh";
&copyFile2Server($node,$node_user,$node_pwd,$ssh_port,$hostShell_path,$tmp_dest);
#Invoke the host shell script
my $host = $ssh ->exec("sh $tmp_dest/hostCommand.sh");
print "host result: $host\n";
sleep(100);
}
