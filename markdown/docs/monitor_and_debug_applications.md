# Monitor

## Third-party Monitoring Solutions
Kubernetes does not offer a very functional monitoring capability. Therefore, third-party
tools such as the following are used in practice.

- Prometheus
- Elastic Stack
- DataDog
- dynatrace
- Metrics Server

## Heapster vs. Metrics Server

Heapster (deprecated) was replaced with Metrics Server

### Metrics Server

#### Getting Started
``` 
git clone https://github.com/kubernetes-incubator/metrics-server.git
```

```
kubectl create -f deploy/1.8+/
```
### View

``` 
kubectl top node
```

``` 
kubectl top pod
```