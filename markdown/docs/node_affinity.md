# Node Affinity

Ensures that pods are hosted on particular nodes as desired.

## Node Selector vs Node Affinity

### Node Selector

Not able to construct complex selector patterns such as AND, OR, NOT, etc.
operators. But the syntax is easier to grasp.

#### Example

~~~yaml
apiVersion: v1
kind: Pod
metadata: 
  name: myapp-pod
spec:
  containers:
  - name: data-processor
    image: data-processor
  nodeSelector: 
    size: LARGE
~~~

### Node Affinity

More complex query/selection capabilities, but more difficult to understand
the syntax.

#### Examples

##### Multiple Values
~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: data-processor
    image: data-processor
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: size
            operator: In
            values: 
            - LARGE
            - MEDIUM
~~~

##### Not a Particular Value(s)

~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: data-processor
    image: data-processor
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: size
            operator: NoIn
            values: 
            - SMALL
~~~

##### If Exists (no particular value)

~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: data-processor
    image: data-processor
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: size
            operator: Exists
~~~

### Node Affinity Types

#### Available for Use Today

- requiredDuringSchedulingIgnoredDuringExecution
- preferredDuringSchedulingIgnoredDuringExecution

#### Support Planned in Near Future

- requiredDuringSchedulingRequiredDuringExecution

### Summary of Node Affinity Types

The node affinity type determines the behavior with respect to placing
new pods vs how to deal with already running pods. *DuringScheduling* is
associated with pods not running on nodes but about to be scheduled. 
*DuringExecution* is associated with pods already running on a node.

| Type   |DuringScheduling|DuringExecution|
|--------|----------------|---------------|
| Type 1 |     Required   |    Ignored    |
| Type 2 |     Preferred  |    Ignored    |
| Type 3 |     Required   |   Required    |

# LAB

~~~
root@controlplane:~# alias k=kubectl
root@controlplane:~# k get node node01 --show-labels
NAME     STATUS   ROLES    AGE   VERSION   LABELS
node01   Ready    <none>   21m   v1.20.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=node01,kubernetes.io/os=linux
root@controlplane:~# 
~~~

~~~
root@controlplane:~# k label node node01 color=blue
node/node01 labeled
root@controlplane:~# k get node node01 --show-labels
NAME     STATUS   ROLES    AGE   VERSION   LABELS
node01   Ready    <none>   23m   v1.20.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,color=blue,kubernetes.io/arch=amd64,kubernetes.io/hostname=node01,kubernetes.io/os=linux
~~~

~~~
root@controlplane:~# k create deployment blue --image=nginx --replicas=3
deployment.apps/blue created
~~~

~~~
root@controlplane:~# k get node controlplane -o yaml | grep -iC 5 taint
root@controlplane:~# k get node node01 -o yaml | grep -iC 5 taint
root@controlplane:~# 
~~~

~~~
root@controlplane:~# k create deployment red --image=nginx --replicas=2 --dry-run=client -o yaml > red.yaml
root@controlplane:~# vim red.yaml
root@controlplane:~# k create -f red.yaml
~~~