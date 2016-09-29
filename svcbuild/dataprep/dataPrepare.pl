#!/usr/bin/perl -w
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
my $rcrel;
my $rccg;
my $user_sec;
my $user_adm;
my $user_copy;
my $user_service;
my $user_monitor;
my $usergrp;
my $tmp_dest = "/tmp";
my $shell_path = "/root/testtool/svcbuild/dataprep";
my $get_mdiskgrp;
my $drive_id = "";
my $auto_mdiskgrp_capacity;

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
        }elsif($name =~ m/vdisk_thinmirror/)
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
        }
		elsif($name =~ m/rcrel/)
        {
                $rcrel = $value;
        }
        elsif($name =~ m/rccg/)
        {
                $rccg = $value;
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
        }elsif($name =~ m/user_monitor/)
        {
                $user_monitor = $value;
        }elsif($name =~ m/usergrp/)
        {
                $usergrp = $value;
        }
}
close CONF;

print "cluserip:$cluster_ip\npwd:$cluster_pwd\nuser:$cluster_user\nport:$cluster_port\n";

#Go through the ssh authentication, login the cluster

	my $ssh = Net::SSH::Expect->new(
    	raw_pty => 1,
		host => $cluster_ip,
		password => $cluster_pwd,
		user => $cluster_user,
		port => $cluster_port,
		timeout => 30);
	 	$ssh->login();

#Check the system has the Auto_mdiskgrp or not
$get_mdiskgrp = $ssh ->exec("svcinfo lsmdiskgrp  | awk '{if(NR>=2) print \$2 }'");
#Check the exist mdiskgrp "Auto_mdiskgrp0"'s capacity, if it doesn't have capacity, then delete it.
$auto_mdiskgrp_capacity = $ssh ->exec("svcinfo lsmdiskgrp Auto_mdiskgrp0 | awk '{if(NR==6) print \$2}'");
sub createPool{
	my ($svc,$v7000) =@_;
	if($svc==1){
		my $get_mdisk = $ssh ->exec("svcinfo lsmdisk -filtervalue status=online | grep unmanaged");
		my @mdisk = split(/\n/, $get_mdisk);
		my $mdisk_count=0;
		my $mdisk_id;
		while($mdisk_count<@mdisk){
        	if($mdisk[$mdisk_count] =~ m/mdisk\d/){
                	my @mdisk_area = split(/mdisk\d/, $mdisk[$mdisk_count]);
                	$mdisk_id .= $mdisk_area[0].":";
        	}
        	$mdisk_count++;
		}
		$mdisk_id =~ s/\s+//g;
		$mdisk_id = substr($mdisk_id,0,length($mdisk_id)-1);
		print "Get the stable mdisk id list:$mdisk_id\n";
		
       #Create mdiskgrp Auto_mdiskgrp0
        my $mdiskgrp_cmd ="svctask mkmdiskgrp -name Auto_mdiskgrp0 -easytier auto -ext 32 -guiid 0 -mdisk $mdisk_id -warning 80%";
        my $mdiskgrp_result = $ssh->exec($mdiskgrp_cmd);
        print "create SVC family mdiskgrp result:$mdiskgrp_result\n";
        
	}elsif($v7000 ==1){
		my $get_drive = $ssh ->exec("svcinfo lsdrive -filtervalue use=candidate:status=online | awk '{if(NR>=2) print \$1}'");
        my @drives = split(/\n/, $get_drive);
		#shift the first element(this is a command)
		shift @drives;
		pop @drives;
        my $drive_count=1;

		#The cluster can not speicified so much drives.
		my $drive_num;

		if(@drives >= 6){
			$drive_num = 6;
		}
		else{
			$drive_num = @drives;
		}
		while($drive_count<$drive_num){
			my $tmp = $drives[$drive_count];
			chomp($tmp);
			#$drive_id = $drive_id."$tmp:";
            $drive_id = join ':',$drive_id, $tmp;
			$drive_count++ ;
		}
        $drive_id =~ s/\s+//g;
		$drive_id =~ s/:\[.+//g;
		$drive_id =~ s/^.//;

		#Create mdiskgrp Auto_mdiskgrp0
        my $mdiskgrp_cmd ="svctask mkmdiskgrp -ext 1024 -guiid 0 -warning 80% -name Auto_mdiskgrp0";
        my $array_cmd = "svctask mkarray -drive $drive_id -level raid0 -sparegoal 0 Auto_mdiskgrp0";
       	 	
		my $mdiskgrp_result = $ssh->exec($mdiskgrp_cmd);
       	my $array_result = $ssh->exec($array_cmd); 
       	 	
      	print "create V7000 family mdiskgrp result:$mdiskgrp_result\n";
        print "create V7000 family array result:$array_result\n";
	}
	
}
#Get the cluster type
if($cluster_type =~ m/SVC/){
	if($get_mdiskgrp !~ /Auto_mdiskgrp/){
		createPool 1,0;
	}
	elsif($get_mdiskgrp =~ /Auto_mdiskgrp/ && $auto_mdiskgrp_capacity == 0){
		#delete the "Auto_mdiskgrp0" mdiskgrp
		$ssh -> exec("svctask rmmdiskgrp -force Auto_mdiskgrp0");
		createPool 1,0;
	}else{
		print "Cluster is already created Auto_mdiskgrp0 successfully, you can use it right now.\n"
	}
}
elsif($cluster_type =~ m/V7000/){
	if($get_mdiskgrp !~ /Auto_mdiskgrp/){
		createPool 0,1;
	}
	elsif($get_mdiskgrp =~ /Auto_mdiskgrp/ && $auto_mdiskgrp_capacity == 0){
		#delete the "Auto_mdiskgrp0" mdiskgrp
		$ssh -> exec("svctask rmmdiskgrp -force Auto_mdiskgrp0");
		createPool 0,1;
	}else{
		print "Cluster is already created Auto_mdiskgrp0 successfully, you can use it right now.\n"
	}
     
}else{
	print "The cluster type is wrong, exit.\n";
}

# Copy the create vdisk shell script to server
my $vdiskShell_path = "$shell_path/volumesCommand.sh";
&copyFile2Server($cluster_ip,$cluster_user,$cluster_pwd,$cluster_port,$vdiskShell_path,$tmp_dest);
# Invoke the volumes shell script
#(SHELL Generic,Thin-provision,Mirror,Thin-mirror,compressed)
my $vdisk = $ssh ->exec("sh $tmp_dest/volumesCommand.sh $vdisk_gen $vdisk_thinpro $vdisk_mirror $vdisk_thinmirror $vdisk_compress");
print "vdisk result: $vdisk\n";
sleep(100);

# Copy the host shell script to server
my $hostShell_path = "$shell_path/hostCommand.sh";
&copyFile2Server($cluster_ip,$cluster_user,$cluster_pwd,$cluster_port,$hostShell_path,$tmp_dest);
#Invoke the host shell script
my $host = $ssh ->exec("sh $tmp_dest/hostCommand.sh $host_fc $host_iscsi $host_sas $host_vdisk_mapping");
print "host result: $host\n";
sleep(100);


# Get the cluster name or id
my $cluster_cmd="svcinfo lscluster | grep 00000";
my $cluster_res = $ssh -> exec($cluster_cmd);
my @cluster = split(/\n/,$cluster_res);

my $cluster_id_res = $cluster[1];
my $cluster_id = substr($cluster_id_res,0,16);


# Copy the copyservice shell script to server
my $copyServiceShell_path = "$shell_path/copyservicesCommand.sh";
&copyFile2Server($cluster_ip,$cluster_user,$cluster_pwd,$cluster_port,$copyServiceShell_path,$tmp_dest);
# Invoke the copyservices shell script
my $copyservice = $ssh ->exec("sh $tmp_dest/copyservicesCommand.sh $fccg $fcmap $rccg $rcrel $cluster_id");
print "copy services result: $copyservice\n";
sleep(100);



# Copy the user shell script to server
my $userShell_path = "$shell_path/userCommand.sh";
&copyFile2Server($cluster_ip,$cluster_user,$cluster_pwd,$cluster_port,$userShell_path,$tmp_dest);
# Invoke the copyservices shell script
my $user = $ssh ->exec("sh $tmp_dest/userCommand.sh $user_sec $user_adm $user_copy $user_service $user_monitor $usergrp");
print "user result: $user\n";
sleep(100);

