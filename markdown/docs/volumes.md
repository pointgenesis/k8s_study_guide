# Volumes

## Docker Volumes

Docker containers are transient in nature. They are called upon used, then destroy when finished.

The data in the container is also destroyed. To enable data persistence, a volume is attached
to the docker container to retain the data after the container is destroyed.

## Kubernetes Volumes

Kubernetes pods are similar in nature to Docker containers in that they are transient. Data is
stored in a volume to persist past pod deletion.

### Volumes and Mounts

The following is an example of a volume mount.

#### example-pod.yaml

~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: random-number-generator
spec:
  containers:
  - image: alpine
    name: alpine
    command: ["/bin/sh", "-c"]
    args: ["shuf -i 0-100 -n 1 >> /opt/number.out;"]
    volumeMounts:
    - mountPath: /opt
      name: data-volume
  volumes:
  - name: data-volume
    hostPath: 
      path: /data
      type: Directory
~~~

### Volume Types

#### Directory

This type of volume is actually just a directory on the host. This does not work well for
multi-node clusters as the other nodes will use a local directory with this same name, but 
these directories will not be in sync with each other and therefore are not feasible for 
multi node shared storage. Unless you configure an external replicated storage solution.

Kubernetes supports several storage solutions such as the following:
- Public cloud aka AWS, Azure, GCP, etc.
- NFS
- GlusterFS
- Flocker
- ceph
- SCALEIO

# Persistent Volumes

A persistent volume is a cluster-wide pool of storage volumes configured by an administrator
and used by users deploying applications on the cluster. The users can select storage from
this pool using persistent volume claims.

#### accessModes
- ReadOnlyMany
- ReadWriteOnce
- ReadWriteMany

#### pv-definition.yaml
~~~yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-vol1
spec:
  accessMode:
    - ReadWriteOnce
  capacity:
    storage: 1Gi
  hostPath:
    path: /tmp/data
~~~

``` 
kubectl create -f pv-definition.yaml
```

``` 
kubectl get persistentvolume
```

Note: you would never use...

~~~yaml
  hostPath:
    path: /tmp/data
~~~

Instead, use a supported pooled solution as discussed previously such as...

~~~yaml
  awsElasticBlockStore:
    volumeID: <volume-id>
    fsType: ext4
~~~

### Persistent Volume Claims

As previously noted, an administrator defines a persistent volume, and users create persistent
volume claims to utilize storage resources. Every persistent volume claim is bound to a single
persistent volume.

### Binding

Kubernetes tries to match PVC requests to available storage using attributes such as

- Sufficient Capacity
- Access Modes
- Volume Modes
- Storage 

You can attempt to specify a particular persistent volume by binding using a matching selector.

#### persistent-volume-fragment.yaml

~~~yaml
labels:
  name: my-pv
~~~

#### persistent-volume-claim-fragment.yaml

~~~yaml
selector:
  matchLabels:
    name: my-pv
~~~

It is possible for a smaller claim to get bound to a larger claim if there are no better
options available.

There is a 1-1 relationship between claims (pvc) and volumes (pv). Volumes are not shared
with multiple persistent volume claims. And persistent volume claims cannot share the same
volume.

If there are no volumes available that match the attributes required by the claim, then
the claim will wait in a **pending** state until an available volume is created/appears.

#### pvc-definition.yaml

~~~yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessMode:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
~~~

#### Create Claim

``` 
kubectl create -f pvc-definition.yaml
```

#### View Claim

``` 
kubectl get persistentvolumeclaim
```

Assuming the following persistent volume definition, and there are no other volume definitions
available. Since our claim attribute match the volume attribute for **accessMode** and no
other attributes besides storage is specified, then our claim will be bound to this volume
despite the size difference (500Mi vs 1Gi).

#### pv-definition.yaml

~~~yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-vol1
spec:
  accessMode:
    - ReadWriteOnce
  capacity:
    storage: 1Gi
  awsElasticBlockStore:
    volumeID: <volume-id>
    fsType: ext4
~~~

#### Delete Persistent Volume Claims

Deleting a persistent volume claim follows a similar pattern seen many times.

```
kubectl delete peristentvolumeclaim myclaim
```

But what happens to the underlying persitent volume after the binding is released? The configuration
options are:

- Retain
- Delete
- Recycle


By default the volume is retained, but you can specify the action in the definition. Retain 
means that the volume is retained until manually deleted. However, the volume is not 
available for other claims.

#### retain-example-pv.yaml

~~~yaml
persitentVolumeReclaimPolicy: Retain
~~~

Another option is to delete the volume; thereby freeing up storage on the device.

#### delete-example-pv.yaml

~~~yaml
persitentVolumeReclaimPolicy: Delete
~~~

The last option is to recycle the volume. The data and volume are scrubbed before making
the volume available to other claims.

#### recycle-example-pv.yaml

~~~yaml
persitentVolumeReclaimPolicy: Recycle
~~~

### Using Persistent Volume Claims in Pods

Once you create a claim, you can reference it in a pod definition as seen in the following
example.

#### pod-definition.yaml

~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
    - name: myfrontend
      image: nginx
      volumeMounts:
      - mountPath: "/var/www/html"
        name: mypd
  volumes:
    - name: mypd
      persistentVolumeClaim:
        claimName: myclaim
~~~

## Labs

#### View Logs

Exec into the container and view the logs.

```
kubectl exec webapp -- cat /log/app.log
```

If the pod were deleted, then you would no longer be able to access these logs.

1. Configure a volume to store these logs at /var/log/webapp on the host using the spec:

#### Spec:
- Name: webapp
- Image Name: kodekloud/event-simulator
- Volume HostPath: /var/log/webapp
- Volume Mount: /log

#### webapp.yaml

~~~yaml
kind: Pod
metadata:
  name: webapp
spec:
  containers:
  - name: event-simulator
    image: kodekloud/event-simulator
    env:
    - name: LOG_HANDLERS
      value: file
    volumeMounts:
    - mountPath: /log
      name: log-volume

  volumes:
  - name: log-volume
    hostPath:
      # directory location on host
      path: /var/log/webapp
      # this field is optional
      type: Directory
~~~

``` 
kubectl replace -f webapp.yaml --force
```

2. Create a PersistentVolume with the following spec:

#### Spec:

- Volume Name: pv-log
- Storage: 100Mi
- Access Modes: ReadWriteMany
- Host Path: /pv/log
- Reclaim Policy: Retain