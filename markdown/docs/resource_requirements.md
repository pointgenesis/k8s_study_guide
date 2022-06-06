# Resource Requirements

## Available Resources

The Kubernetes Scheduler decides on which node to place a pod. The resources available on a node dictate where a pod
is placed. If a given node does not have sufficient resources for a given pod, then the node will not be selected. If 
there are no nodes available with sufficient resources, then the pod will be held in a pending state until a node with
sufficient resources becomes available.

## Resource Requests

- CPU
- Memory
- Disk

### Example Pod Definition 

~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
  labels:
    name: simple-webapp-color
spec:
  containers:
    - name: simple-webapp-color
      image: simple-webapp-color
      ports: 
        - containerPort: 8080
      resources:
        requests:
          memory: "1Gi"
          cpu: 1
~~~

### CPU Resource Requests with Resources

- Expressed as low as 0.1
- 0.1 can be expressed as 100m
- m is milli
- Requests can be as low as 1m
- 1 CPU is equivalent to 1 virtual CPU or 1 hyper thread

### Difference between Storage Scales

#### Metric Style

- 1G (Gigabyte) = 1,000,000,000 bytes
- 1M (Megabyte) = 1,000,000 bytes
- 1K (Kilobyte) = 1,000 bytes

#### Binary Style

- 1Gi (Gibibyte) = 1,073,741,824 bytes
- 1Mi (Mebibyte) = 1,048,576 bytes
- 1Ki (Kibibyte) = 1,024 bytes

### Example Pod Definition with Limits

~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
  labels:
    name: simple-webapp-color
spec:
  containers:
    - name: simple-webapp-color
      image: simple-webapp-color
      ports: 
        - containerPort: 8080
      resources:
        requests:
          memory: "1Gi"
          cpu: 1
        limits:
          memory: "2Gi"
          cpu: 2
~~~

When a container requests more resources such as CPU than the defined limit,
then kubernetes will throttle the request. However, if MEM requests exceed
the available memory enough times, then the pod will be terminated.

## Default Limits

### Memory

~~~yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-limit-range
spec:
  limits:
  - default:
      memory: 512Mi
    defaultRequest:
      memory: 256Mi
    type: Container
~~~

### CPU

~~~yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: cpu-limit-range
spec:
  limits:
  - default:
      cpu: 1
    defaultRequest:
      cpu: 0.5
    type: Container
~~~