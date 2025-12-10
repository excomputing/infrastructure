
<br>

> [!TIP]
> * <a href="https://boto3.amazonaws.com/v1/documentation/api/latest/index.html" target="_target">Amazon Web Services Software Development Kit (Python)</a>
> * <a href="https://kubernetes.io" target="_blank">kubernetes</a>
>   * <a href="https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/" target="_blank">managing resource containers</a>
> * <a href="https://karpenter.sh" target="_blank">karpenter.sh</a>

<br>


## `KUBECTL` & `EKSCTL`

Setting up

* [Set up kubectl and eksctl](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html): Beware, Docker Desktop installs `kubectl`.
* [kubectl reference](https://kubernetes.io/docs/reference/kubectl/generated/)
* [eksctl reference](https://docs.aws.amazon.com/eks/latest/eksctl/what-is-eksctl.html)
* Inspect `/usr/local/bin` for installation outlines of <abbr title="Amazon Web Services">AWS</abbr> <abbr title="Command Line Interface">CLI</abbr>, 'eksctl', and `kubectl`.


<br>


## `CLUSTER` & `ADDITIONS`

A cluster wherein the [built-in NodePools](https://docs.aws.amazon.com/eks/latest/userguide/set-builtin-node-pools.html) are disabled:

```shell
python src/kubernetes.py
```

Inspecting:

```bash
aws eks describe-cluster --name {cluster.name}
aws eks list-addons --cluster-name {cluster.name}
aws eks describe-addon --cluster-name {cluster.name} --addon-name {add.on.name}
```

<br>

## `KUBECTL` & `EKS` & `EKSCTL`

### connecting

> [!IMPORTANT]
> [Connect kubectl to an EKS cluster by creating a kubeconfig file](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)

<br>

`kubectl` connects to an Elastic Kubernetes Service (EKS) cluster via a kubeconfig file, via the directive

```shell
aws eks update-kubeconfig --region {region.code} --name {cluster.name}
```

Inspect, test, via

```shell
kubectl get svc
```

The Amazon EKS cluster authentication directive is

```shell
aws eks get-token --cluster-name {cluster.name}
```

<br>

### custom node class, custom node pool

> [!IMPORTANT]
> * [Create a Node Class for Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/create-node-class.html), [node classes](https://karpenter.sh/docs/concepts/nodeclasses/)
> * [Create a Node Pool for EKS Auto Mode](https://docs.aws.amazon.com/eks/latest/userguide/create-node-pool.html)

Next, the node class & node pool

```shell
kubectl apply -f src/eks/node-class.yaml
kubectl apply -f src/eks/node-pool.yaml
```

and inspecting

```shell
kubectl get nodepools
```

<br>

### custom node class: access entry

> [!IMPORTANT]
> * [Create node class access entry](https://docs.aws.amazon.com/eks/latest/userguide/create-node-class.html#auto-node-access-entry)

Refer to src/eks/node.sh

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
