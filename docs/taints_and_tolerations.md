# Taints and Tolerations

Taints and tolerances set restrictions on what pods can be scheduled on a 
node. 

## Taints

**Taints** are set on nodes.

### Signature
`
kubectl taint nodes <node-name> <key>=<value>: <taint-effect>
`

### Taint-effect

- **NoSchedule** 
  - Scheduler will not place the pod on the node.
- **PreferNoSchedule** 
  - System will try to avoid placing the pod on the node.
- **NoExecute** 
  - System will not schedule new pods that do not tolerate the taint on the node
  - Scheduler will evict existing pods if they do not tolerate the taint.

### Example

`
kubectl taint nodes node1 app=blue:NoSchedule
`

## Tolerations

**Tolerations** are set on pods.

### Example Pod Definition File

~~~yaml
apiVersion: v1
kind: Pod
metadata: 
  name: my-pod
  labels:
    name: my-pod
spec: 
  containers:
    - name: nginx-container
      image: nginx
    tolerations:
      - key: "app"
        operator: "Equal"
        value: "blue"
        effect: "NoSchedule"
~~~

___Note: all attribute values under tolerations must be in quotes.___ 

The master node does not accept pods due to taints that are applied
to the master node. You can see this taint by running the following command.

```
kubectl describe node kubemaster | grep -i taint
> Taints: node-role.kubernetes.io/master:NoSchedule
```