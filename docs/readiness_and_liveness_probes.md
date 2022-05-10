# Readiness and Liveness Probes

## Readiness Probes

### POD Status

- Pending
- ContainerCreating
- Running
- Terminated

### POD Conditions

- PodScheduled {True | False}
- Initialized {True | False}
- ContainersReady {True | False}
- Ready {True | False}

~~~
kubectl describe pod <pod-name> | grep -iC 5 conditions
~~~

#### Ready
This is an indication of whether the pod is ready to serve requests.
Unfortunately, this status is not a good indicator of actual readiness of the application.
That is where readiness probes are helpful.

~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp
  labels:
    name: simple-webapp
spec:
  containers:
  - name: simple-webapp
    image: simple-webapp
    ports: 
    - containerPort: 8080
    readinessProbe:
      httpGet:
        path: /api/ready
        port: 8080
~~~

### readinessProbe

#### HTTP Test

~~~yaml
readinessProbe:
  httpGet:
    path: <PATH>
    port: <PORT>
  initialDelaySeconds: <delay in seconds>
  periodSeconds: <retry interval in seconds>
  failureThreshold: <number of failures before marking failed>
~~~

#### TCP Test

~~~yaml
readinessProbe:
  tcpSocket:
    port: 3306
~~~

#### Exec Command

~~~yaml
readinessProbe:
  exec:
    command:
      - <command>
      - <arg>   
~~~

## Liveness Probes

### livenessProbe

#### HTTP Test

~~~yaml
livenessProbe:
  httpGet:
    path: <PATH>
    port: <PORT>
  initialDelaySeconds: <delay in seconds>
  periodSeconds: <retry interval in seconds>
  failureThreshold: <number of failures before marking failed>
~~~

#### TCP Test

~~~yaml
livenessProbe:
  tcpSocket:
    port: 3306
~~~

#### Exec Command

~~~yaml
livenessProbe:
  exec:
    command:
      - <command>
      - <arg>   
~~~