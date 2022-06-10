# Network Policies

## Traffic

Components need to define network polices depending upon which direction traffic flows. These
direction policies are designated as either ingress or egress. 

### Ingress

Traffic flowing into a contextual boundary, i.e., traffic requests coming from a user.

### Egress

Traffic flowing out of a contextual boundary, i.e., responses going back to the user.

## Network Security

Pods should be able to communicate with each other without additional networking. By default,
k8s is configured following an ALLOW ALL principle.

### Access Restrictions by Pod
However, sometimes we want to restrict access to a particular pod. For example, you typically
do not want a front-end HTTP server to have direct access to the database. To restrict access, 
we employ a familiar concept by specifying selectors that will be permitted to communicate.

For example, we take note of the label in the protected resource and create a network policy 
that matches that label.

A fragment from the db-pod.yaml.

~~~yaml
labels: 
    role: db
~~~

The *selector-fragment* seen below is the first step when trying to establish a network policy.
The intention is to isolate/identify the particular pod that we wish to extend protection around.
We do this using selectors and labels.

~~~yaml
podSelector:
    matchLabels:
        role: db
~~~

The *rule-fragment* shown below demonstrates how we specify allowed interactions. Remembering
that by default, kubernetes follows an ALLOW ALL policy. But specifying granular ingress/egress
rules, the ALLOW ALL policy is no longer applicable. And we are able to specify exactly what is 
desired from a protection model.

The direction of the original request determines whether the rule is an ingress or egress rule.
The response direction is not important as it is allowed by default. Similar to AWS security
group rules.

~~~yaml
policyTypes:
- Ingress
ingress:
- from:
  - podSelector:
      matchLabels:
        name: api-pod
  ports:
  - protocol: TCP
    port: 3306
~~~

*policy-template*

~~~yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  <selector-fragment>
  <rule-fragment>
~~~

#### policy-definition.yaml

~~~yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
        role: db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          name: api-pod
    ports:
    - protocol: TCP
        port: 3306
~~~

~~~
kubectl create -f policy-definition.yaml 
~~~

### Access Restrictions by Namespace

By default, pods in all namespaces that match the pod selector value will be allowed to communicate 
with the protected pod. To prevent undesired access, you can specify a namespace selector that
will further refine the desired access routes.

See the following fragment as an example.

~~~yaml
namespaceSelector:
  matchLabels:
    name: prod
~~~

The following is a complete policy definition including the namespace selector.

#### policy-definition.yaml

~~~yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
        role: db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          name: api-pod
      namespaceSelector:
        matchLabels:
          name: prod
    ports:
    - protocol: TCP
        port: 3306
~~~

### Access Restrictions by IP Address

There may be times when access originating from outside kubernetes is desired. A backup server
is a good example. The server has a known IP address so using that information we can permit
this outside access.

~~~yaml
- ipBlock:
    cidr: 10.0.0.5/32
~~~

#### policy-definition.yaml

~~~yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
        role: db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          name: api-pod
      namespaceSelector:
        matchLabels:
          name: prod
    - ipBlock:
        cidr: 10.0.0.5/32
    ports:
    - protocol: TCP
        port: 3306
~~~

### Egress Rules

#### policy-definition.yaml

~~~yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
        role: db
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          name: api-pod
      namespaceSelector:
        matchLabels:
          name: prod
    - ipBlock:
        cidr: 10.0.0.5/32
    ports:
    - protocol: TCP
        port: 3306
  egress:
  - to:
      - ipBlock:
          cidr: 172.10.3.1/32
      ports:
        - protocol: TCP
          port: 80
  
~~~

## Solutions Supporting Network Policies

The following solutions support network policies:
- Kube-router
- Calico
- Romana
- Weave-net

The following solutions do not support network policies:
- Flannel

## Lab Solutions

1. How many network policies do you see in the environments?

~~~
kubectl get networkpolicy
~~~

Alternate solution using shorthand

~~~
kubectl get netpol
~~~

2. What pods are using this policy?

Hint: Using the selector value that shows up from question-1 check the pods.

~~~
kubectl get pods -l name=payroll
~~~

3. What type of traffic is this Network Policy configured to handle?

~~~
kubetctl describe networkpolicy payroll-policy
~~~

See: **Policy Types** in the response

4. What is the effect of the rule configured on this Network Policy?

Answer: 

5. ddk