# Service Account

There are two types of account in Kubernetes.

- User Accounts
- Service Accounts

## User Account

These are accounts that humans use to access resources. Examples include
an administrator, developer, user, etc.

## Service Account

These are accounts that machines and services use in order to access resources.
Examples include an account used by Prometheus to monitor Kubernets for 
performance metrics. Another example is an account used by Jenkins to deploy 
applications to k8s clusters.

### Create Service Account

Signature

~~~
kubectl create serviceaccount <service_account_name>
~~~

Example

~~~
kubectl create serviceaccount dashboard-sa
~~~

### Get Service Account

Signature
```
kubectl get <service_account_name>
```

Example
```
kubectl get dashboard-sa
```

### Describe Service Account

When a service account is created, the first thing that is created is
the service account object, a `token` is generated for the service 
account, then creates a secret storing the token in the secret object. 
The secret object is then linked to the service account. The token
can then be used as an authorization bearer token when making REST calls
to the k8s API.

Signature
``` 
kubectl describe serviceaccount <service_account_name>
```

Example
``` 
kubectl describe serviceaccount dashboard-sa
```

To view the token issue the following command.

Signature
```
kubectl describe secret <service_account_token_name>
```

Example
``` 
kubectl describe secret dashboard-sa-token-kbbdm
```

Command Line Example Usage
```
curl https://192.168.0.1:6443/api -insecure --header "Authorization: Bearer eyJ7hbg..."
```

## Default Service Account

There is a `default` service account created for every namespace.
Executing a describe command against any pod created in the 
namespace, and you will find a mounted volume representing the token of 
the default service account

``` 
kubectl describe pod my-pod
```

``` 
kubectl exec -it my-pod ls /var/run/secrets/kubernetes.io/serviceaccount
```

``` 
kubectl exec -it my-pod cat /var/run/secrets/kubernetes.io/serviceaccount/token
```

### Service Accounts in Pods

pod-definition.yaml

~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    name: my-pod
spec:
  containers:
    - name: my-pod
      image: my-pod
  serviceAccountName: dashboard-service-account
~~~

You cannot dynamically update the service account associate with a pod
definition. You must delete the pod, then recreate the pod after making
the service account change.

The service account can be dynamically applied to deployments. The reason
is due to the fact that deployments first delete the pods and then
recreate the pods with the new service account.

### automountServiceAccountToken

You can turn off the auto mounting of the default service account by
setting the `automountServiceAccountToken` to `false`.

pod-definition.yaml
```yaml
apiVersion: v1
kind: Pod
metadata: 
  name: my-kubernetes-dashboard
spec:
  containers:
    - name: my-kubernetes-dashboard
      image: my-kubernetes-dashboard
  automountServiceAccountToken: false
```