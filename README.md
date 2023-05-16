# parse-iis-smtp-logs
### Parse the logs for the SMTP service on a Microsoft IIS server.  

This script returns a csv file consisting of source hostname, source IP address and a per-host count of occurences in the log file.

In the repo's <i><b>dist</b></i> directory there is a Windows portable executable file called ```parse-smtp-logs.exe``` that should be able to run directly on a Windows host.