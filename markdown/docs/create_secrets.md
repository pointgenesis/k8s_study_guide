#Secrets

## Imperative Create

### --from-literal Syntax

`kubectl create secret generic <secret-name> --from-literal=<key>=<value>`

#### Code Example

~~~
kubectl create secret generic \
    my-app-secret --from-literal=DB_HOST=mysql \
                  --from-literal=DB_USER=root \
                  --from-literal=DB_PASSWORD=password
~~~

### --from-file Syntax

~~~
kubectl create secret generic <secret-name> --from-file=<path-to-file>
~~~

#### Code Example

~~~
kubectl create secret generic my-app-secret --from-file=my_app_secret.properties
~~~

## Declarative Create

`secret-data.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
    name: app-secret
data:
    DB_HOST: bXlzcWw=
    DB_USER: cm9vdA==
    DB_PASSWORD: cGFzc3dvcmQ=
```

~~~
kubectl create -f secret-data.yaml
~~~

### Encode Secret Values

#### Plain-text Values Are Not Allowed
```yaml
DB_HOST: mysql
DB_USER: root
DB_PASSWORD: password
```

#### Base-64 Encoded Values Are Required

~~~
echo -n 'mysql' | base64
bXlzcWw=
~~~

~~~
echo -n 'root' | base64
cGFzc3dvcmQ=
~~~

~~~
echo -n 'password' | base64
cm9vdA==
~~~

```yaml
DB_HOST: bXlzcWw=
DB_USER: cm9vdA==
DB_PASSWORD: cGFzc3dvcmQ=
```

#### Decode Base-64 Encoded Values

~~~
echo -n 'bXlzcWw=' | base64 --decode
mysql
~~~

~~~
echo -n 'cGFzc3dvcmQ=' | base64 --decode
root
~~~

~~~
echo -n 'cm9vdA==' | base64 --decode
password
~~~

## View Secrets

To view only the secret names, then issue the following command...

~~~
kubectl get secrets
~~~

To view additional information about a secret, then describe the secret(s)...

~~~
kubectl describe secrets
~~~

~~~
kubectl describe secret <secret-name>
~~~

~~~
kubectl describe secret my-app-secret
~~~

To view additional information, including the encoded secret values, then issue the following command...

~~~
kubectl get secret my-app-secret -o yaml
~~~

## Secrets in Pods

`pod-definition.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata: 
    name: simple-webapp-color
    lables:
        name: simple-webapp-color
spec:
    containers:
    - name: simple-webapp-color
      image: simple-webapp-color
      ports:
        - containerPort: 8080
      envFrom:
        - secretRef:
            name: app-secret
```

### Environment

```yaml
envFrom:
  - secretRef:
    name: app-config
```

### Single ENV key/value pair

```yaml
env:
  - name: DB_Password
    valueFrom: 
      secretKeyRef:
        name: app-secret
        key: DB_Password
```

### Volume

```yaml
volumes:
  - name: app-secret-volume
    secret:
      secretName: app-secret
```

## Secrets in Pods as Volumes

### Volume

~~~yaml
volumes:
  - name: app-secret-volume
    secret: 
      secretName: app-secret
~~~

#### Inside the Container

The secrets are mounted as files inside the volume. 
The keys are files. The values are stored as content inside the file.

~~~
ls /opt/app-secret
DB_Host DB_Password DB_User
~~~

~~~
cat /opt/app-secret-volumes/DB_Password
password
~~~
