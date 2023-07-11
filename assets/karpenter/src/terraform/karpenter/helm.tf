resource "helm_release" "karpenter" {
  namespace        = var.namespace
  create_namespace = true

  name       = "karpenter"
  repository = "https://charts.karpenter.sh/"
  chart      = "karpenter"
  version    = var.karpenter_version

  set {
    name  = "serviceAccount.annotations.eks\\.amazonaws\\.com/role-arn"
    value = module.karpenter_irsa.iam_role_arn
  }

  set {
    name  = "clusterName"
    value = module.eks.cluster_id
  }

  set {
    name  = "clusterEndpoint"
    value = module.eks.cluster_endpoint
  }

  set {
    name  = "aws.defaultInstanceProfile"
    value = aws_iam_instance_profile.karpenter.name
  }
}
