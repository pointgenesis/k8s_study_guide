# Multi-container Pods

## Ambassador

## Adapter

## Sidecar

## Labs Solution

1. How many containers are found in the red pod?

``` 
kubectl get pod red -o wide
NAME   READY   STATUS              RESTARTS   AGE   IP       NODE           NOMINATED NODE   READINESS GATES
red    0/3     ContainerCreating   0          19s   <none>   controlplane   <none>           <none>
```

2. Identify the name of the containers running in the blue pod?

``` 
kubectl get pod blue -o wide
NAME   READY   STATUS    RESTARTS   AGE    IP            NODE           NOMINATED NODE   READINESS GATES
blue   2/2     Running   0          7m4s   10.244.0.10   controlplane   <none>           <none>
```

3. Identify the name of the containers running in the blue pod.

``` 
kubectl get pod blue -o yaml | grep -iC 5 containerID
```

~~~yaml
  - containerID: docker://ff007aca6254f97732df386b61396219aa330a2ab47b26a816a1bee45e565f49
    image: busybox:latest
    imageID: docker-pullable://busybox@sha256:d2b53584f580310186df7a2055ce3ff83cc0df6caacf1e3489bff8cf5d0af5d8
    lastState: {}
    name: navy
    ready: true
    restartCount: 0
    started: true
    state:
      running:
        startedAt: "2022-05-09T22:37:44Z"
  - containerID: docker://12f450412c2bd4cca254b3e3cc3941459476d57c84cab0b172fe14360118e10e
    image: busybox:latest
    imageID: docker-pullable://busybox@sha256:d2b53584f580310186df7a2055ce3ff83cc0df6caacf1e3489bff8cf5d0af5d8
    lastState: {}
    name: teal
    ready: true
~~~

4. Create a multi-container pod with 2 containers.

Use the spec given below.
If the pod goes into the crashloopbackoff then add the command sleep 
1000 in the lemon container.

Name: yellow

- Container 1 Name: lemon
- Container 1 Image: busybox
- Container 2 Name: gold
- Container 2 Image: redis

~~~yaml
apiVersion: v1
kind: Pod
metadata:
        name: yellow
spec:   
        containers:
          - name: lemon
            image: busybox
            command:
            - sleep
            - "1000"
          - name: gold
            image: redisq
~~~

~~~
kubectl create -f yellow.yaml
pod/yellow created
~~~

4. Inspect the app pode and identify the number of containers.

~~~
kubectl get pod app -o yaml | grep -iC 5 containerID
~~~

~~~yaml
  - lastProbeTime: null
    lastTransitionTime: "2022-05-09T22:35:00Z"
    status: "True"
    type: PodScheduled
  containerStatuses:
  - containerID: docker://41749c190af15f959660192b9e3dc568e1819a5cea84faa3f624c3a019900530
    image: kodekloud/event-simulator:latest
    imageID: docker-pullable://kodekloud/event-simulator@sha256:1e3e9c72136bbc76c96dd98f29c04f298c3ae241c7d44e2bf70bcc209b030bf9
    lastState: {}
    name: app
    ready: true
~~~

5. View the logs and identify the user having Login issues.

~~~
kubectl -n elastic-stack logs kibana
~~~

~~~
kubectl -n elastic-stack exec -it app -- cat /log/app.log | grep -iC 2 login
~~~

~~~
--
  [2022-05-09 23:33:25,907] INFO in event-simulator: USER4 is viewing page3
[2022-05-09 23:33:26,517] INFO in event-simulator: USER2 is viewing page3
[2022-05-09 23:33:26,909] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2022-05-09 23:33:26,909] INFO in event-simulator: USER1 is viewing page3
[2022-05-09 23:33:27,518] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2022-05-09 23:33:27,518] INFO in event-simulator: USER4 is viewing page2
[2022-05-09 23:33:27,910] INFO in event-simulator: USER4 logged out
--
  [2022-05-09 23:33:30,914] INFO in event-simulator: USER1 logged out
[2022-05-09 23:33:31,523] INFO in event-simulator: USER4 is viewing page2
[2022-05-09 23:33:31,916] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2022-05-09 23:33:31,916] INFO in event-simulator: USER4 is viewing page3
[2022-05-09 23:33:32,524] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2022-05-09 23:33:32,524] INFO in event-simulator: USER1 logged in
[2022-05-09 23:33:32,917] WARNING in event-simulator: USER7 Order failed as the item is OUT OF STOCK.
~~~

6. Add a sidecar container to send logs to ElasticSearch. Use the following
spec.


- Name: app
- Container Name: sidecar
- Container Image: kodekloud/filebeat-configured
- Volume Mount: log-volume
- Mount Path: /var/log/event-simulator/
- Existing Container Name: app
- Existing Container Image: kodekloud/event-simulator

~~~
kubectl get pod --namespace=elastic-stack app -o yaml > app.yaml
vim app.yaml
~~~

~~~yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: "2022-05-10T00:19:20Z"
  labels:
    name: app
  name: app
  namespace: elastic-stack
  resourceVersion: "3224"
  uid: e3d76311-60a0-43c6-966b-93e4c531f426
spec:
  containers:
  - image: kodekloud/filebeat-configured
    name: sidecar
    volumeMounts:
    - mountPath: /var/log/event-simulator/
      name: log-volume
  - image: kodekloud/event-simulator
    imagePullPolicy: Always
    name: app
    resources: {}
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /log
      name: log-volume
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: kube-api-access-9hl9t
      readOnly: true
  dnsPolicy: ClusterFirst
  enableServiceLinks: true
  nodeName: controlplane
  preemptionPolicy: PreemptLowerPriority
  priority: 0
  restartPolicy: Always
  schedulerName: default-scheduler
  securityContext: {}
  serviceAccount: default
~~~

~~~
kubectl delete pod app --namespace=elastic-stack
~~~

~~~
kubectl create -f app.yaml
~~~

~~~
root@controlplane ~ ✖ kubectl get pod app --namespace=elastic-stack
NAME   READY   STATUS    RESTARTS   AGE
app    2/2     Running   0          23s
~~~
