# Jobs and Cron Jobs

## Jobs

### RestartPolicy

By default, the container restartPolicy is Always.

``` 
restartPolicy: Always
```

The pod will continue to restart the container if it fails.

There are cases when this behavior is not desired. In those cases, change the policy to 
Never.

``` 
restartPolicy: Never
```

#### pod-definition.yaml

~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: math-pod
spec:
  containers:
  - name: math-add
    image: ubuntu
    command: ['expr', '3', '+', '2']
  restartPolicy: Never
~~~

### Create, View, and Delete

#### job-definition.yaml

~~~yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: math-add-job
spec:
  template:
    spec: 
      containers: 
      - name: math-add
        image: ubuntu
        command: ['expr', '3', '+', '2']
      restartPolicy: Never
~~~

#### Create

~~~
kubectl create -f job-definition.yaml
~~~

#### View

~~~
kubectl get jobs
~~~

~~~
kubectl get pods
~~~

~~~
kubectl logs math-add-job-93k9k
~~~

#### Delete

~~~
kubectl delete job math-add-job
~~~

#### Multiple Jobs

If multiple runs of the job are desired then set the completions attribute. This will 
create a number of pods that match the desired number of completions. Note, that the
pods do not execute in parallel, but instead run in a serial fashion after each one 
completes its workload successfully.

``` 
completions: <number-of-pods-to-create>
```

##### Example 

###### job-definition.yaml

~~~yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: math-add-job
spec:
  completions: 3
  template:
    spec: 
      containers: 
      - name: math-add
        image: ubuntu
        command: ['expr', '3', '+', '2']
      restartPolicy: Never
~~~

You can request that the jobs run in parallel by including the attribute *parallelism*.

``` 
parallelism: 3
```

##### Example

###### job-definition.yaml

~~~yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: math-add-job
spec:
  parallelism: 3
  completions: 3
  template:
    spec:
      containers: 
      - name: math-add
        image: ubuntu
        command: ['expr', '3', '+', '2']
      restartPolicy: Never
~~~

## Cron Jobs

### Example

#### cron-job-definition.yaml

~~~yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: reporting-cron-job
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec: 
      completions: 3
      parallelism: 3
      template: 
        spec:
          containers: 
          - name: reporting-tool
            image: reporting-tool
          restartPolicy: Never
~~~

### Create

``` 
kubectl create -f cron-job-definition.yaml
```

```
kubectl get cronjob
```