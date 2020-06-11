## Update and Upgrade OS - Windows and Linux distro (Ubuntu and Amazon Linux )

`Requirement`

* Automatically Patch defined OS

## Deployement Instructions
```
* Modify the template_hosts file to hosts and add your target mahines.
* Run the playbook - "ansible-playbook <playbookname>"
```

## In-case of ROLL-BACK
```
* Define the patch to rollback in the script.
* Run the playbook to process it.
```
## Sync the Update OS files from Ansible dir to S3

`Recommended to push your logs to S3 server' = 'ansible-playbook <playbookname> >/etc/ansible/windows-playbbook/<name_of_the_file>.txt`
* s3 sync <desired file> s3://bucketname/path/
