// http://blog.nodejitsu.com/nodejs-cloud-server-in-three-minutes/ssh.js
var util=require('util');
var spawn=require('child_process').spawn;
var ssh = spawn('ssh',['-l '+'root',' 9.123.196.241']);

ssh.stdout.on('data',function(data){
    process.stdout.write(data);
})

process.stdin.on('data',function(data){
    console.log('stdin:'+data)        
})

process.on('exit',function(data){
    console.log('node ssh exits.')        
})
