<br>

> [!TIP]
> * <a href="https://boto3.amazonaws.com/v1/documentation/api/latest/index.html" target="_target">Amazon Web Services Software Development Kit (Python)</a>
> * Inspect `/usr/local/bin` for installation outlines of <abbr title="Amazon Web Services">AWS</abbr> <abbr title="Command Line Interface">CLI</abbr>, 'eksctl', and `kubectl`.
> * [node pool](https://docs.aws.amazon.com/eks/latest/userguide/create-node-pool.html)

<br>

## Notes

Steps:

* A cluster wherein the [built-in NodePools](https://docs.aws.amazon.com/eks/latest/userguide/set-builtin-node-pools.html) are disabled.

Inspecting:

```bash
aws eks describe-cluster --name {cluster.name}
aws eks list-addons --cluster-name {cluster.name}
aws eks describe-addon --cluster-name {cluster.name} --addon-name {add.on.name}
```

<br>

### kubectl & EKS

> [!IMPORTANT]
> [Connect kubectl to an EKS cluster by creating a kubeconfig file](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)

<br>

`kubectl` connects to an Elastic Kubernetes Service (EKS) cluster via a kubeconfig file, which the directive

```shell
aws eks update-kubeconfig --region {region.code} --name {cluster.name}
kubectl get svc
```

creates; the second directive tests.  The Amazon EKS cluster authentication directive is 

```shell
aws eks get-token --cluster-name {cluster.name}
```

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
