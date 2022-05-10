# Container Logging

## Docker Logs

```
docker run -d kodekloud/event-simulator
```

```
docker logs -f ecf
```

## Kubernetes Logs

~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: event-simulator-pod
spec:
  containers:
  - name: event-simulator
    image: kodekloud/event-simulator
  - name: image-processor
    image: some-image-processor
~~~

```
kubectl create -f event-simulator.yaml
```

The following is indeterminate with respect to desired container logs you want...

``` 
kubectl logs -f event-simulator-pod
```

Specify the container whose logs you wish to access...

``` 
kubectl logs -f <pod-name> <container-name>
```

``` 
kubectl logs -f event-simulator-pod event-simulator
```
