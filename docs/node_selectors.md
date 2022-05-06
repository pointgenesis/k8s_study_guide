# Node Selectors

## Label Nodes

```
kubectl label nodes <node-name> <label-key>=<label-value>
```

### Example

``` 
kubectl label nodes my-node size=LARGE
```

#### pod-definition.yaml

~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: data-processor
      image: data-processor
    nodeSelector: 
      size: LARGE
~~~

``` 
kubectl create -f pod-definition.yaml
```

## Node Selector Limitations

More complex scenarios that have multiple selection criteria cannot
be achieved using node selectors. In order to achieve this level of
advanced selectors, **Node Affinity** features were created.