# Labels, Selectors, and Annotations

## Labels

pod-definition.yaml
~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp
  labels:
    app: app1
    function: front-end
spec:
  containers:
  - name: simple-webapp
    image: simple-webapp
    ports:
    - containerPort: 8080
~~~

### Selectors

``` 
kubectl get pods --selector app=app1
```

### ReplicaSet

When trying to select particular pods inside an object such as a replica set, remember
that the labels of interest are those inside the spec section and not the labels 
listed under the parent object's (replica set's) metadata section.

replicaset-definition.yaml

~~~yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: simple-webapp
  labels: 
    app: app1
    function: front-end
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app1
  template:
    metadata:
      labels:
        app: app1
        function: front-end
    spec:
      containers:
      - name: simple-webapp
        image: simple-webapp 
~~~

## Annotations

Placed inside the metadata section as additional information such as build details.

~~~yaml
apiVersion: app/v1
kind: ReplicaSet
metadata:
  name: my-replicaset
  labels:
    app: my-app
    function: front-end
  annotations:
    buildVersion: 1.3.4
~~~

## Labs

1. How many pds are in the dev env. Note there are labels for bu, env and tier.

``` 
kubectl get pods -l env=dev

NAME          READY   STATUS    RESTARTS   AGE
app-1-fjv28   1/1     Running   0          2m59s
db-1-hph96    1/1     Running   0          2m59s
db-1-649sz    1/1     Running   0          2m59s
db-1-tbt46    1/1     Running   0          2m59s
db-1-c6zcs    1/1     Running   0          2m59s
app-1-wx8ws   1/1     Running   0          2m59s
app-1-n2pm4   1/1     Running   0          2m59s
``` 


2. How many PODs are in the `finance` business unit (bu)?

``` 
kubectl get pods -l bu=finance

NAME          READY   STATUS    RESTARTS   AGE
app-1-zzxdf   1/1     Running   0          6m27s
app-1-fjv28   1/1     Running   0          6m28s
db-2-52xk6    1/1     Running   0          6m28s
app-1-wx8ws   1/1     Running   0          6m28s
app-1-n2pm4   1/1     Running   0          6m28s
auth          1/1     Running   0          6m28s
```

3. How many objects are in the `prod` environment including PODs, ReplicaSets, etc.?

``` 
kubectl get all -l env=prod

NAME              READY   STATUS    RESTARTS   AGE
pod/app-1-zzxdf   1/1     Running   0          8m24s
pod/app-2-bfv4c   1/1     Running   0          8m25s
pod/db-2-52xk6    1/1     Running   0          8m25s
pod/auth          1/1     Running   0          8m25s

NAME            TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
service/app-1   ClusterIP   10.43.46.249   <none>        3306/TCP   8m24s

NAME                    DESIRED   CURRENT   READY   AGE
replicaset.apps/app-2   1         1         1       8m25s
replicaset.apps/db-2    1         1         1       8m25s
```

4. Identify the POD that is part of the `prod` environment, `finance` business unit, and
the `frontend` tier.

``` 
kubectl get pods -l env=prod,bu=finance,tier=frontend
NAME          READY   STATUS    RESTARTS   AGE
app-1-zzxdf   1/1     Running   0          11m
```

5. A ReplicaSet definition file is given below. There is an issue with the file. Try to create
the replica set. Fix the issue.

~~~yaml
cat replicaset-definition-1.yaml 
apiVersion: apps/v1
kind: ReplicaSet
metadata:
   name: replicaset-1
spec:
   replicas: 2
   selector:
      matchLabels:
        tier: front-end
   template:
     metadata:
       labels:
        tier: nginx
     spec:
       containers:
       - name: nginx
         image: nginx
~~~

``` 
k create -f replicaset-definition-1.yaml 
The ReplicaSet "replicaset-1" is invalid: spec.template.metadata.labels: 
Invalid value: map[string]string{"tier":"nginx"}: `selector` does not match 
template `labels`
```

``` 
vim replicaset-definition-1.yaml

==> DO CHANGES and SAVE

k create -f replicaset-definition-1.yaml
```

``` 
cat replicaset-definition-1.yaml
```

~~~yaml 
apiVersion: apps/v1
kind: ReplicaSet
metadata:
   name: replicaset-1
spec:
   replicas: 2
   selector:
      matchLabels:
        tier: nginx
   template:
     metadata:
       labels:
        tier: nginx
     spec:
       containers:
       - name: nginx
         image: nginx
~~~