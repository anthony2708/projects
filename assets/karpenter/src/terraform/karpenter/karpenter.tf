resource "kubectl_manifest" "karpenter_provisioner" {
  yaml_body = <<-YAML
  apiVersion: karpenter.sh/v1alpha5
  kind: Provisioner
  metadata:
    name: default
  spec:
    requirements:
      - key: karpenter.sh/capacity-type
        operator: In
        values: ["spot"]
      - key: karpenter.k8s.aws/instance-size
        operator: In
        values: [nano, micro, small, medium, large]
    limits:
      resources:
        cpu: 1000
        memory: 1000Gi
    provider:
      subnetSelector:
        Name: "*private*"
      securityGroupSelector:
        karpenter.sh/discovery/${module.eks.cluster_id}: ${module.eks.cluster_id}
      tags:
        karpenter.sh/discovery/${module.eks.cluster_id}: ${module.eks.cluster_id}
    ttlSecondsAfterEmpty: 30
    ttlSecondsUntilExpired: 2592000
  YAML

  depends_on = [
    helm_release.karpenter,
    aws_iam_service_linked_role.EC2SpotforEKS
  ]
}