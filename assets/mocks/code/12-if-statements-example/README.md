# Terraform If-Statements & If-Else-Statements example

This folder contains an If-Statements and If-Else-Statements example of a [Terraform](https://www.terraform.io/) file on AWS (Amazon Web Services).

It shows how to use a:

1 - simple If-Statement funcionality using an "enable_autoscaling" variable in the module in order to execute or not the resources:

* resource "aws_autoscaling_schedule" "scale_out_during_business_hours"
* resource "aws_autoscaling_schedule" "scale_in_at_night"

Defining the values of "enable_autoscaling" variable:

* true (= 1) in Production
* false (= 0) in Staging

2 - more complicated If-Statement funcionality using the "instance_type" variable in the module in order to execute or not the resource:

* resource "aws_cloudwatch_metric_alarm" "low_cpu_credit_balance"

and using:

count = "${format("%.1s", var.instance_type) == "t" ? 1 : 0}"

where:

* true (= 1) if "var.instance_type" start with a letter "t" (e.g., t2.micro)
* false (= 0) if "var.instance_type" does not start with a letter  "t"

3 - a more complicated If-Else-Statement funcionality using a "enable_new_user_data" variable in the module in order to a data script or another:

* if "enable_new_user_data" is true (staging environment) the execute "user_data_new.sh"
* if "enable_new_user_data" is false (production environment) the execute "user_data.sh"

Furthermore, it shows how to develop (not duplicating code) web server clusters in different environments using a module.

The environments are:

* Staging (stage)
* Production (prod)

This is the file layout in this repo:

```bash
live
    ├── global
    │       └── s3/
    │           ├── main.tf
    │           └── (etc)
    │
    ├── stage
    │       ├── services/
    │       │   └── webserver-cluster/
    │       │       ├── main.tf
    │       │       └── (etc)
    │       └── data-stores/
    │           └── mysql/
    │               ├── main.tf
    │               └── (etc)
    │
    └── prod
            ├── services/
            │   └── webserver-cluster/
            │       ├── main.tf
            │       └── (etc)
            └── data-stores/
                └── mysql/
                    ├── main.tf
                    └── (etc)

modules
    └── services/
        └── webserver-cluster/
            ├── main.tf
            └── (etc)
```

It uses in common for both environments:

* Terraform Remote State example: [live/global/s3](live/global/s3)
* Terraform Web Server Cluster module example: [modules/services/webserver-cluster](modules/services/webserver-cluster)

It uses for staging environment:

* Terraform MySQL on RDS example (staging environment): [live/stage/data-stores/mysql](live/stage/data-stores/mysql)
* Terraform Web Server Cluster example (staging environment): [live/stage/services/webserver-cluster](live/stage/services/webserver-cluster)

It uses for production environment:

* Terraform MySQL on RDS example (production environment): [live/prod/data-stores/mysql](live/prod/data-stores/mysql)
* Terraform Web Server Cluster example (production environment): [live/prod/services/webserver-cluster](live/prod/services/webserver-cluster)

## Requirements

* You must have [Terraform](https://www.terraform.io/) installed on your computer.
* You must have an [AWS (Amazon Web Services)](http://aws.amazon.com/) account.
* It uses the Terraform AWS Provider that interacts with the many resources supported by AWS through its APIs.
* This code was written for Terraform 0.10.x.

## Using the code

* Configure your AWS access keys.

  **Important:** For security, it is strongly recommend that you use IAM users instead of the root account for AWS access.

  Setting your credentials for use by Terraform can be done in a number of ways, but here are the recommended approaches:

  * The default credentials file
  
    Set credentials in the AWS credentials profile file on your local system, located at:

    `~/.aws/credentials` on Linux, macOS, or Unix

    `C:\Users\USERNAME\.aws\credentials` on Windows

    This file should contain lines in the following format:

    ```bash
    [default]
    aws_access_key_id = <your_access_key_id>
    aws_secret_access_key = <your_secret_access_key>
    ```
    Substitute your own AWS credentials values for the values `<your_access_key_id>` and `<your_secret_access_key>`.

  * Environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
  
    Set the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables.

    To set these variables on Linux, macOS, or Unix, use `export`:

    ```bash
    export AWS_ACCESS_KEY_ID=<your_access_key_id>
    export AWS_SECRET_ACCESS_KEY=<your_secret_access_key>
    ```

    To set these variables on Windows, use `set`:

    ```bash
    set AWS_ACCESS_KEY_ID=<your_access_key_id>
    set AWS_SECRET_ACCESS_KEY=<your_secret_access_key>
    ```

* Use Terraform Remote State example for creating the remote state bucket. See: [live/global/s3](live/global/s3)

* Use Terraform module example for Web Server Cluster example in the staging environment and Web Server Cluster example in the production environment. See: [modules/services/webserver-cluster](modules/services/webserver-cluster)

* Use Terraform MySQL on RDS example for creating a MySQL database in the staging environment. See: [live/stage/data-stores/mysql](live/stage/data-stores/mysql)

* Use Terraform Web Server Cluster example for creating a web server cluster in the staging environment. See: [live/stage/services/webserver-cluster](live/stage/services/webserver-cluster)

* Use Terraform MySQL on RDS example for creating a MySQL database in the production environment. See: [live/prod/data-stores/mysql](live/prod/data-stores/mysql)

* Use Terraform Web Server Cluster example for creating a web server cluster in the production environment. See: [live/prod/services/webserver-cluster](live/prod/services/webserver-cluster)
