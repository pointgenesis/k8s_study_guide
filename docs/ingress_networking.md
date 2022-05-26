# Ingress

Ingress performs a service similar to a Layer-7 Load Balancer that is built into 
the kubernetes cluster that can be configured using native kubernetes primitives just
like any other object in kubernetes.

In order to be externally accessible, the ingress must be published as a NodePort 
service or via a cloud native load balancer. This is a one-time configuration.

Ongoing configurations of load balancing, authentication, SSL/TLS, and URL routing
decisions occur on the ingress controller.

## Ingress vs Services

Ingress is a higher level function that sits above the services.

### Deploy (Ingress Controller)

A kubernetes does not come with an ingress controller deployed by default.

Examples of ingress controllers are third-party services such as

- *GCP HTTP(S)/Load Balancer (GCE)** (Supported by Kubernetes) 
- *Nginx** (Supported by Kubernetes)
- Contour
- HAProxy
- Traefik
- Istio

#### ingress-controller.yaml

~~~yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-ingress-controller
spec:
  replicas: 1
  selector:
    matchLabels:
      name: nginx-ingress
  template: 
    metadata:
      name: nginx-ingress
    spec:
      containers:
      - name: nginx-ingress-controller
        image: quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.21.0
      args:
      - /nginx-ingress-controller
      - --configmap=$(POD_NAMESPACE)/nginx-configuration
      env:
      - name: POD_NAME
        valueFrom:
          fieldRef:
            fieldPath: metadata.name
      - name: POD_NAMESPACE
        valueFrom:
          fieldRef:
            fieldPath: metadata.namespace
      ports:
      - name: http
        containerPort: 80
      - name: https
        containerPort: 443

~~~

Nginx expects configurations for the following features

- err-log-path
- keep-alive
- ssl-protocols

We can decouple these from the Nginx configuration by supplying a config map.

#### ingress-config-map.yaml

~~~yaml
kind: ConfigMap
version: v1
metadata:
  name: nginx-configuration
~~~

#### ingress-service-account.yaml

~~~yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nginx-ingress-serviceaccount
~~~

##### Bindings

- Roles
- ClusterRoles
- RoleBindings

### Configure (Ingress Resources)

A set of rules and configurations applied to an ingress controller.

#### ingress-wear.yaml

~~~yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wear
spec:
  backend:
    serviceName: wear-service
    port: 80
~~~

```
kubectl create -f ingress-wear.yaml
```

```
kubectl get ingress
```

#### Rules

Are used to create route patterns via application context, domain, subdomain, etc.

##### Routing via Paths
###### ingress-wear-watch.yaml

~~~yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wear-watch
spec:
  rules:
  - http:
      paths:
      - path: /wear
        pathType: Prefix
        backend:
          service:
            name: wear-service
            port: 80
      - path: /watch
        pathType: Prefix
        backend:
          service:
            name: watch-service
            port: 80
~~~

```
kubectl create -f ingress-wear-watch.yaml
```

```
kubectl describe ingress ingress-wear-watch
```
Note the `Default backend` attribute. If a request does not match any configured paths,
then the request is directed to the default backend. You must create a default backend
to handle these requests. Otherwise, the user will receive a 404 HTTP response.

#### Routing via Host (Domain)

##### ingress-wear-watch-yaml
~~~yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wear-watch
spec:
  rules:
  - host: wear.my-online-store.com  
    http:
      paths:
      - backend: 
          serviceName: wear-service
          servicePort: 80
  - host: watch.my-online-store.com  
    http:
      paths:
      - backend:
          serviceName: watch-service
          servicePort: 80
~~~

## Imperative Commands

### Format

```kubectl createe ingress <ingress-name> --rule="<host/path=service:port>"```

### Example

```kubectl createe ingress ingress-test --rule="wear.myonline-store.com/wear=wear-service:80>"```

### References

[[1] Ingress, https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#-em-ingress-em-](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#-em-ingress-em-)
[[2] Ingress Feature State, https://kubernetes.io/docs/concepts/services-networking/ingress/](https://kubernetes.io/docs/concepts/services-networking/ingress/)
[[3] Path types, https://kubernetes.io/docs/concepts/services-networking/ingress/#path-types](https://kubernetes.io/docs/concepts/services-networking/ingress/#path-types)

