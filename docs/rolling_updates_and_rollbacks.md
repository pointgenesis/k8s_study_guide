# Rolling Updates & Rollbacks in Deployments

## Rollout Command
To see the rollout status issue the following commands
~~~
kubectl rollout status <deployment-name>
~~~

~~~
kubectl rollout status deployment/myapp-deployment
~~~

To see the history of rollouts and revisions, issue the following command:

~~~
kubectl rollout history <deployment-name>
~~~

~~~
kubectl rollout history deployment/myapp-deployment
~~~

## Deployment Strategies

### Recreate (All At Once)

This strategy takes down all currently running instances at once, then deploys the 
replacement instances. There is downtime experienced with this approach.

### Rolling Update 
`DEFAULT`

This strategy takes down a single instance, replaces it with a newer version, then
proceeds to another older node repeating the process until all older nodes are replaced.
Downtime is not experienced with this approach with only minimal degradation.

### Apply Changes

You can update `image` information and apply the changes to update deployments.

**deployment-definition.yaml**

~~~yaml
apiVersion: apps/v1
kind: Deployment
metdata:
  name: myapp-deployment
  labels:
    app: myapp
    type: front-end
spec:
  template:
    metadata:
      name: myapp-pod
      labels:
        app: myapp
        type: front-end
    spec:
      containters:
      - name: nginx-container
        image: nginx:1.7.1
  replicas: 3
  selector:
    matchLabels:
      type: front-end
~~~

~~~
kubectl apply -f deployment-definition.yaml
~~~

You can also do this imperatively; however, the deployment definition file will be out of
sync with the actual deployment.

~~~
kubectl set image <deployment-name> <image-name>=<image-version>
~~~

~~~
kubectl set image deployment/myapp-deployment nginx=nginx:1.9.1
~~~

### Upgrades

A ReplicaSet is created when you do a deployment. When you do an upgrade deployment, another
ReplicaSet is created where the newer version is deployed. Then the initial ReplicaSet is
drained to 0 pods.

You can see both ReplicaSets and the number of pods in each by issuing the following command:

~~~
kubectl get replicasets
~~~

### Rollbacks

If you need to roll back to a previous version, then issue the following command.

~~~
kubectl rollout undo <deployment-name>
~~~

~~~
kubectl rollout undo deployment/myapp-deployment
~~~

The current pod versions will be terminated and replaced by the previous version present
in the initial replica set before the deployment. The initial replica set will be 
returned to the starting state, the new replica set will be scaled down to 0.

## Summary of Commands

### Create

~~~
kubectl create -f <deployment-file-name>
~~~

### Get

~~~
kubectl get deployment <deployment-name>
~~~

### Update

~~~
kubectl apply -f <updated-deployment-file-name>
~~~

~~~
kubectl set image <deployment-name> <old-image-name>=<new-image-name>
~~~

### Status

~~~
kubectl rollout status <deployment-name>
~~~

~~~
kubectl rollout history <deployment-name>
~~~

### Rollback

~~~
kubectl rollout undo <deployment-name>
~~~

## Updating a Deployment - Addendum

Here are some handy examples related to updating a Kubernetes Deployment:

- Creating a deployment, checking the rollout status and history:

In the example below, we will first create a simple deployment and inspect the rollout status and the rollout history:

~~~
master $ kubectl create deployment nginx --image=nginx:1.16
deployment.apps/nginx created
~~~

~~~
master $ kubectl rollout status deployment nginx
Waiting for deployment "nginx" rollout to finish: 0 of 1 updated replicas are available...
deployment "nginx" successfully rolled out
 
master $
~~~

~~~ 
master $ kubectl rollout history deployment nginx
deployment.extensions/nginx
REVISION CHANGE-CAUSE
1     <none>
 
master $
~~~

### Using the --revision flag:

Here the revision 1 is the first version where the deployment was created.

You can check the status of each revision individually by using the --revision flag:

~~~
master $ kubectl rollout history deployment nginx --revision=1
deployment.extensions/nginx with revision #1
 
Pod Template:
 Labels:    app=nginx    pod-template-hash=6454457cdb
 Containers:  nginx:  Image:   nginx:1.16
  Port:    <none>
  Host Port: <none>
  Environment:    <none>
  Mounts:   <none>
 Volumes:   <none>
master $ 
~~~

### Using the --record flag:

You would have noticed that the "change-cause" field is empty in the rollout history output. We can use the --record flag to save the command used to create/update a deployment against the revision number.

~~~
master $ kubectl set image deployment nginx nginx=nginx:1.17 --record
deployment.extensions/nginx image updated
master $master $
~~~

~~~
master $ kubectl rollout history deployment nginx
deployment.extensions/nginx
 
REVISION CHANGE-CAUSE
1     <none>
2     kubectl set image deployment nginx nginx=nginx:1.17 --record=true
master $
~~~

You can now see that the change-cause is recorded for the revision 2 of this deployment.

Let's make some more changes. In the example below, we are editing the deployment and changing the image from nginx:1.17 to nginx:latest while making use of the --record flag.

~~~
master $ kubectl edit deployments. nginx --record
deployment.extensions/nginx edited
~~~

~~~
master $ kubectl rollout history deployment nginx
REVISION CHANGE-CAUSE
1     <none>
2     kubectl set image deployment nginx nginx=nginx:1.17 --record=true
3     kubectl edit deployments. nginx --record=true
~~~ 
 
~~~
master $ kubectl rollout history deployment nginx --revision=3
deployment.extensions/nginx with revision #3
 
Pod Template: Labels:    app=nginx
    pod-template-hash=df6487dc Annotations: kubernetes.io/change-cause: kubectl edit 
    deployments. nginx --record=true
 
 Containers:
  nginx:
  Image:   nginx:latest
  Port:    <none>
  Host Port: <none>
  Environment:    <none>
  Mounts:   <none>
 Volumes:   <none>
 
master $
~~~

### Undo a change:

Lets now rollback to the previous revision:

~~~
master $ kubectl rollout undo deployment nginx
deployment.extensions/nginx rolled back
 
master $ kubectl rollout history deployment nginx
deployment.extensions/nginxREVISION CHANGE-CAUSE
1     <none>
3     kubectl edit deployments. nginx --record=true
4     kubectl set image deployment nginx nginx=nginx:1.17 --record=true
~~~ 
 
~~~ 
master $ kubectl rollout history deployment nginx --revision=4
deployment.extensions/nginx with revision #4Pod Template:
 Labels:    app=nginx    pod-template-hash=b99b98f9
 Annotations: kubernetes.io/change-cause: kubectl set image deployment 
 nginx nginx=nginx:1.17 --record=true
 Containers:
  nginx:
  Image:   nginx:1.17
  Port:    <none>
  Host Port: <none>
  Environment:    <none>
  Mounts:   <none>
 Volumes:   <none>
~~~

~~~ 
master $ kubectl describe deployments. nginx | grep -i image:
  Image:    nginx:1.17
master $
~~~

With this, we have rolled back to the previous version of the deployment with the image = nginx:1.17.