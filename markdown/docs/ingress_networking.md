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

### Imperative Commands

###### Format

```
kubectl create ingress <ingress-name> --rule="<host/path=service:port>"
```

###### Example

```
kubectl create ingress ingress-test --rule="wear.myonline-store.com/wear=wear-service:80>"
```

### rewrite-target

This is similar to the ProxyPass directive in an httpd.conf file for Apache HTTPD Server where
and incoming request is mapped to a corresponding location, i.e., 

```
ProxyPath "/backend" "http://backend.example.com"
```

The ***rewrite-target*** maps the ingress request in the same way.

See the following [examples](https://kubernetes.github.io/ingress-nginx/examples/rewrite/) for more details.

~~~yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
  name: rewrite
  namespace: default
spec:
  ingressClassName: nginx
  rules:
  - host: rewrite.bar.com
    http:
      paths:
      - path: /something(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: http-svc
            port: 
              number: 80
~~~

In this ingress definition, any characters captured by (.*) will be assigned to the placeholder $2, which is then used as a parameter in the rewrite-target annotation.

For example, the ingress definition above will result in the following rewrites:

rewrite.bar.com/something rewrites to rewrite.bar.com/
rewrite.bar.com/something/ rewrites to rewrite.bar.com/
rewrite.bar.com/something/new rewrites to rewrite.bar.com/new


##### App Root

~~~yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/app-root: /app1
  name: approot
  namespace: default
spec:
  ingressClassName: nginx
  rules:
  - host: approot.bar.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: http-svc
            port: 
              number: 80
~~~

To fix that we want to "ReWrite" the URL when the request is passed on to the watch or wear applications. We don't want to pass in the same path that user typed in. So we specify the rewrite-target option. This rewrites the URL by replacing whatever is under rules->http->paths->path which happens to be /pay in this case with the value in rewrite-target. This works just like a search and replace function.

For example: replace(path, rewrite-target)
In our case: replace("/path","/")

~~~yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: test-ingress
  namespace: critical-space
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /pay
        backend:
          serviceName: pay-service
          servicePort: 8282
~~~

## Lab Solution

1. We have deployed two applications. Explore the setup.

    ~~~
    kubectl get deployments --all-namespaces
    ~~~

2. Let's deploy an Ingress Controller. First, create a namespace called 'ingress-space'.

    ns &lrarr; namespace
    
    ~~~
    kubectl create ns ingress-space
    ~~~

3. The NGINX Ingress Controller requires a ConfigMap object. Create a ConfigMap object in the ingress-space.

    cm &lrarr; configmap 
    
    ~~~
    kubectl create cm nginx-configuration  -n ingress-space
    ~~~

4. The NGINX Ingress Controller requires a ServiceAccount. Create a ServiceAccount in the
ingress-space with name, ingress-serviceaccount.

    sa &lrarr; serviceaccount 
    
    ~~~
    kubectl create sa ingress-serviceaccount -n ingress-space
    ~~~

5. We created the Roles and RoleBindings for the ServiceAccount. Check it out!

    ~~~
     kubectl -n ingress-space get roles.rbac.authorization.k8s.io
     
     kubectl -n ingress-space get rolebindings.rbac.authorization.k8s.io
    ~~~

6. Let's deploy the Ingress Controller. Create a deployment using the file given. There are
several issues with the file. Try to fix the issues.

    ~~~yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: ingress-controller
      namespace: ingress-space
    spec:
      replicas: 1
      selector:
        matchLabels:
          name: nginx-ingress
      template:
        metadata:
          labels:
            name: nginx-ingress
        spec:
          serviceAccountName: ingress-serviceaccount
          containers: 
            - name: nginx-ingress-controller
              image: quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.21.0
              args: 
                - /nginx-ingress-controller
                - --configmap=$(POD_NAMESPACE)/nginx-configuration
                - --default-backend-service=app-space/default-http-backend
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

7. Let's create a service to make Ingress available to external users.

    Specs:

    - Name: ingress
    - Type: NodePort
    - Port: 80
    - TargetPort: 80
    - NodePort: 30080
    - Note: Remember to use the right selector
        
    ```
    kubectl -n ingress-space expose deployment ingress-controller --name ingress
    --port 80 --target-port 80 --type NodePort --dry-run=client -o yaml > ingress-service.yaml
    ```
    
    ~~~yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: ingress
      namespace: ingress-space
    spec:
      ports:
        - port: 80
          protocol: TCP
          targetPort: 80
          nodePort: 30080
        selector:
          name: nginx-ingress
        type: NodePort
    status:
      loadBalancer: {}
    ~~~
    
    ~~~
    kubectl apply -f ingress-service.yaml
    ~~~

8. Create the ingress resource to make the applications available at /wear and /watch on the ingress service.

    Spec:
    
    - Ingress Created
    - Path: /wear
    - Path: /watch
    - Configure correct backend service for /wear
    - Configure correct backed service for /watch
    - Configure correct backend port for /wear service
    - Configure correct backend port for /watch service
    
    ~~~
    kubectl get svc -n app-space
    ~~~
    
    ~~~
    vi ingress-resource.yaml
    ~~~

    Copy/Paste from the Ingress documentation, then update according to our given specs.
    
    ~~~yaml
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      namespace: app-space
      name: service-ingress
      annotations:
        nginx.ingress.kubernetes.io/rewrite-target: /
    spec:
      ingressClassName: nginx-example
      rules:
      - http:
          paths:
          - path: /wear
            pathType: Prefix
            backend:
              service:
                name: wear-service
                port:
                  number: 8080
          - path: /watch
            pathType: Prefix
            backend:
              service:
                name: video-service
                port:
                  number: 8080              
    ~~~
    
    Finally, apply the changes.
    
    ~~~
    kubectl apply -f ingress-resource.yaml
    ~~~
    
    ~~~
    kubectl -n app-space describe ingress service-ingress
    ~~~

## References

[[1] Ingress, https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#-em-ingress-em-](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#-em-ingress-em-)

[[2] Ingress Feature State, https://kubernetes.io/docs/concepts/services-networking/ingress/](https://kubernetes.io/docs/concepts/services-networking/ingress/)

[[3] Path types, https://kubernetes.io/docs/concepts/services-networking/ingress/#path-types](https://kubernetes.io/docs/concepts/services-networking/ingress/#path-types)

