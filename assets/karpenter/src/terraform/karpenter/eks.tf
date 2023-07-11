module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "18.29.0"

  cluster_name    = "${var.cluster_name}-${terraform.workspace}"
  cluster_version = var.cluster_version

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  enable_irsa = true

  node_security_group_additional_rules = {
    ingress_nodes_karpenter_port = {
      description                   = "Cluster API to Node group for Karpenter webhook"
      protocol                      = "tcp"
      from_port                     = 8443
      to_port                       = 8443
      type                          = "ingress"
      source_cluster_security_group = true
    }

    ingress_nodes_metrics_port = {
      description                   = "Cluster API to Node group for Metrics Server"
      protocol                      = "tcp"
      from_port                     = 4443
      to_port                       = 4443
      type                          = "ingress"
      source_cluster_security_group = true
    }
  }

  node_security_group_tags = {
    # NOTE - if creating multiple security groups with this module, only tag the
    # security group that Karpenter should utilize with the following tag
    # (i.e. - at most, only one security group should have this tag in your account)
    "karpenter.sh/discovery/${var.cluster_name}-${terraform.workspace}" = "${var.cluster_name}-${terraform.workspace}"
  }

  eks_managed_node_groups = {
    initial = {
      name                  = "${var.cluster_name}-ng"
      instance_types        = ["t3.small"]
      create_security_group = false

      min_size     = 2
      max_size     = 3
      desired_size = 2

      iam_role_additional_policies = [
        # Required by Karpenter
        "arn:${local.partition}:iam::aws:policy/AmazonSSMManagedInstanceCore"
      ]

      tags = {
        # This will tag the launch template created for use by Karpenter
        "karpenter.sh/discovery/${var.cluster_name}-${terraform.workspace}" = "${var.cluster_name}-${terraform.workspace}"
      }
    }
  }
}