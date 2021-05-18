aws_asg
==============
A Terraform module for creating an Auto-Scaling Group and a launch
configuration for it, for use with an Elastic Load Balancer.
This module makes the following assumptions:
* You have subnets in a VPC and that you want your instances
   in two subnets (in two AZs)
* You can fully bootstrap your instances using an AMI + user_data
* *You want to associate the ASG with an ELB*
* Your instances behind the ELB will be in a VPC
* Your using a single Security Group for all instances in the ASG

Input Variables
---------------

- `lc_name` - The launch configuration name
- `ami_id`
- `instance_type`
- `iam_instance_profile` - The ARN of the Instance Profile the LC should
   launch instances with.
   E.g. arn:aws:iam::XXXXXXXXXXXX:instance-profile/my-instance-profile
- `key_name` - The SSH key name (uploaded to EC2) instances should
   be populated with.
- `security_group` - The Security Group ID that instances in the ASG
    - This is usually set to resolve to a security group you make in the
      same template as this module, e.g. "${module.sg_web.security_group_id_web}"
    - It needs to be customized based on the name of your module resource.
   should use.
- `user_data` - The path to the user_data file for the Launch Configuration.
    - Terraform will include the contents of this file in the Launch Configuration.
- `asg_name` - The Auto-Scaling group name.
- `asg_number_of_instances` - The number of instances we want in the ASG
    - This is used to populate the following ASG settings.
    - max_size
    - desired_capacity
- `asg_minimum_number_of_instances` - The minimum number of instances
   the ASG should maintain.
    - This is used for min_size
    - It defaults to 1
    - You can set it to 0 if you want the ASG to do nothing when an
      instances fails
- `health_check_grace_period` - Number of seconds for the health check
   time out. Defaults to 300.
- `health_check_type` - The health check type. Options are `ELB` and
   `EC2`. It defaults to `ELB` in this module.
- `load_balancer_names` - The name(s) of the ELB(s) to associate with the ASG,
   for settings it's backend instances. Ideally this is a reference to
   an ELB you're making in the same template as this ASG. Can be a CSV of ELB names
   if more than one is desired.
- `availability_zones` - CSV of availability zones (AZs) for the ASG. *ex. "us-east-1a,us-east-1c"*
- `vpc_zone_subnets` - CSV of VPC subnets to associate with ASG. There should be one subnet
   for each of the `availability_zones.` *ex. "subnet-d2gd22,subnet-2kjn8qq"*

Outputs
-------

- `launch_config_id`
- `asg_id`

Usage
-----

You can use these in your terraform template with the following steps.

1.) Adding a module resource to your template, e.g. `main.tf`

```
module "my_autoscaling_group" {
  source = ""
  lc_name = "${var.lc_name}"
  ami_id = "${var.ami_id}"
  instance_type = "${var.instance_type}"
  iam_instance_profile = "${var.iam_instance_profile}"
  key_name = "${var.key_name}"

  //Using a reference to an SG we create in the same template.
  // - It needs to be customized based on the name of your module resource
  // - It is recommended that you use https://github.com/terraform-community-modules/tf_aws_sg/tree/master/sg_https_only
  //   for the SG
  security_group = "${module.sg_https_only.security_group_id_web}"

  user_data = "${var.user_data}"
  asg_name = "${var.asg_name}"
  asg_number_of_instances = "${var.asg_number_of_instances}"
  asg_minimum_number_of_instances = "${var.asg_minimum_number_of_instances}"

  //Using a reference to an SG we create in the same template
  load_balancer_names = "${module.my_elb.elb_name}"

  // The health_check_type can be EC2 or ELB and defaults to ELB
  health_check_type = "${var.health_check_type}"

  availability_zones = "${var.availability_zones}"
  vpc_zone_subnets = "${var.vpc_zone_subnets}"
}
```

2.) Setting values for the following variables, either through `terraform.tfvars` or `-var` arguments on the CLI

- lc_name
- ami_id
- instance_type
- iam_instance_profile
- key_name
- security_group
- user_data
- asg_name
- asg_number_of_instances
- load_balancer_names
- availability_zones
- vpc_zone_subnets