# Ingress Services

Ingress services are conceptually equivalent to layer-7 load balancers.

1. Deploy an Ingress Controller
   - nginx (supported by k8s)
   - haproxy
   - traefik
   - istio
   - contour
2. Configure the Rules (Ingress Resources)

## Ingress Controller

- Auth
- ConfigMap
- Deployment
- Service

### Deployment

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
      labels:
        name: nginx-ingress
    spec:
      containers:
      - name: nginx-ingress-controller
        image: quay.io/kubernetes-ingress-controller-nginx-ingress
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
        containerPort
~~~

### Service

~~~yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-ingress
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
    name: http
  - port: 443
    targetPort: 443
    protocol: TCP
    name: https
  selectors:
    name: nginx-ingress
~~~

### ConfigMap

~~~yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-configuration
~~~

### Auth

~~~yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nginx-ingress-serviceaccount
~~~

- Roles
- ClusterRoles
- RoleBindings