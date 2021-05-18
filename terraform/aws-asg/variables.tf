variable "create_asg" {
  description = "Controls if asg should be created"
  type        = bool
  default     = true
}

variable "lc_name" {
  description = "Name to be used for launch configuration"
  type        = string
  default     = ""
}

variable "ami_id" {
  description = "The AMI to use with the launch configuration"
  type        = string
  default     = ""
}

variable "instance_type" {
  description = "Type of instance for use"
  type        = string
  default     = ""
}

variable "iam_instance_profile" {
  description = "The IAM role the launched instance will use"
  type        = string
  default     = ""
}

variable "key_name" {
  description = "The SSH public key name (in EC2 key-pairs) to be injected into instances"
  type        = string
  default     = ""
}

variable "security_group" {
  description = "ID of SG the launched instance will use"
  type        = string
  default     = ""
}

variable "user_data" {
  description = "The path to a file with user_data for the instances"
  default     = "user-data.sh"
}

variable "asg_name" {
  /* We use this to populate the following ASG settings
 * - max_size
 * - desired_capacity
 */
  type    = string
  default = ""
}

variable "asg_number_of_instances" {
  description = "The number of instances we want in the ASG"
  default     = []
  /*
 * Can be set to 0 if you never want the ASG to replace failed instances
 */
}
variable "asg_minimum_number_of_instances" {
  description = "The minimum number of instances the ASG should maintain"
  default     = []
  /*
 * Can be set to 1
 */
}

variable "health_check_type" {
  description = "The health check used by the ASG to determine health"
  type        = string
  default     = "ELB"
}

variable "availability_zones" {
  description = "A comma seperated list string of AZs the ASG will be associated with"
  type        = string
  default     = ""
  /*
 * A string list of VPC subnet IDs, ex:
 * "subnet-d2t4sad,subnet-434ladkn"
 */
}

variable "vpc_zone_subnets" {
  description = "A comma seperated list string of VPC subnets to associate with ASG, should correspond with var.availability_zones zones"
  default     = ""
}

variable "load_balancer_names" {
  description = "A comma seperated list string of ELB names the ASG should associate instances with"
  default     = ""
}

variable "health_check_grace_period" {
  description = "Number of seconds for a health check to time out"
  default     = 300
}

variable "elb_names" {
  description = "Name to be used for ELB"
  type        = string
  default     = ""
}