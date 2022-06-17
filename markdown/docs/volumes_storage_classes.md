# Storage Classes

When utilizing a third-party file system solution such as AWS, GCP, etc., you must first
create the disk resource on the external system. This process is known as *Static Provisioning*.

A better solution is for the volume creation to happen automatically when the application requires
its use. This solution is called *Dynamic Provisioning* and is where *Storage Classes* come into play.

## Storage Class

#### sc-definition.yaml

~~~yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: google-storage
provisioner: kubernetes.io/gce-pd
~~~

Additionally, option attributes can be defined for provisioners. These are specific to the 
individual targeted platform.

#### Optional Attributes
~~~yaml
parameters:
type: pd-standard [ pd-standard | pd-ssd ]
replication-type: none [ none | regional-pd ]
~~~

These attributes allow you to create different storage classes as seen in the following examples.

#### Standard (sc-standard-definition.yaml)

~~~yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: google-storage
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-standard
  replication-type: none
~~~

#### Gold (sc-gold-definition.yaml)

~~~yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: google-storage
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
  replication-type: none
~~~

#### Platinum (sc-platinum-definition.yaml)

~~~yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: google-storage
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
  replication-type: regional-pd
~~~

Previously, we required a **Persistent Volume (PV)** definition to requisition storage. Now, the storage
class definition replaces the need for a PV. So, in the **Persistent Volume Claim (PVC)**, we
add the **storageClassName** defined in the **Storage Class** definition.

The **provisioner** defined in the sc-definition.yaml file provisions a new disk with the 
requested size on GCP, AWS, Azure, etc. creates a persistent volume then binds the claim
to that volume. A persistent volume is still created in the background automatically by
the storage class, but a PV definition is no longer created manually by the user.

There are many available provisioners such as _AWSElasticBlockStore_, _AzureFile_, _AzureDisk_,
_CephFS_, _Cinder_, _FC_, _FlexVolume_, _Flocker_, _GCEPersistentDisk_, _Glusterfs_, _iSCSI_, _Quobyte_,
_NFS_, _RBD_, _VsphereVolume_, _PortworxVolume_, _ScaleIO_, _StorageOS_, _Local_, etc. 

#### pvc-definition.yaml

~~~yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: google-storage
  resources:
    requests:
      storage: 500Mi
~~~

#### pod-definition.yaml

~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: random-number-generator
spec:
  containers:
  - image: alpine
    name: alpine
  command: ["/bin/sh","-c"]
  args: ["shuf -i 0-100 -n 1 >> /opt/"]
  volumeMounts:
  - mountPath: /opt
    name: data-volume
  volumes:
  - name: data-volume
    persistentVolumeClaim:
      claimName:
~~~

## Labs Solutions

----------

controlplane ~ ➜  alias k=kubectl

controlplane ~ ➜  k get sc
NAME                   PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
local-path (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  6m45s

controlplane ~ ➜  

----------

controlplane ~ ➜  k get sc
NAME                        PROVISIONER                     RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
local-path (default)        rancher.io/local-path           Delete          WaitForFirstConsumer   false                  8m2s
local-storage               kubernetes.io/no-provisioner    Delete          WaitForFirstConsumer   false                  59s
portworx-io-priority-high   kubernetes.io/portworx-volume   Delete          Immediate              false                  59s

----------

controlplane ~ ✖ k get sc local-storage
NAME            PROVISIONER                    RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
local-storage   kubernetes.io/no-provisioner   Delete          WaitForFirstConsumer   false                  2m35s

controlplane ~ ➜  

----------

WaitForCustomer

----------

portworx-volume

----------

No

----------

Let's fix that. Create a new PersistentVolumeClaim by the name of local-pvc that should bind to the volume local-pv.

Inspect the pv local-pv for the specs.

CheckCompleteIncomplete
PVC: local-pvc

Correct Access Mode?

Correct StorageClass Used?

PVC requests volume size = 500Mi?

answer...

controlplane ~ ➜  vim pvc-def.yaml 

controlplane ~ ➜  k replace -f pvc-def.yaml --force
persistentvolumeclaim "local-pvc" deleted
persistentvolumeclaim/local-pvc replaced

controlplane ~ ➜  cat pvc-def.yaml 
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: local-pvc
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: local-storage
  resources:
    requests:
      storage: 500Mi

----------

Pending

----------

A pod matching characteristics has not been scheduled.

----------

controlplane ~ ➜  k run nginx --image nginx:alpine -o yaml --dry-run=client > nginx-def.yaml

controlplane ~ ➜  vim nginx-def.yaml 

controlplane ~ ➜  k create -f nginx-def.yaml 
pod/nginx created

controlplane ~ ➜  cat nginx-def.yaml 
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  containers:
  - image: nginx:alpine
    name: nginx
    resources: {}
    volumeMounts:
    - mountPath: /var/www/html
      name: local-volume
  volumes:
  - name: local-volume
    persistentVolumeClaim:
      claimName: local-pvc
status: {}

-----

Bound

-----


controlplane ~ ➜  vim delayed-volume-sc.yaml

controlplane ~ ➜  cat delayed-volume-sc.yaml 
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: delayed-volume-sc
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer

controlplane ~ ➜  k create -f delayed-volume-sc.yaml 
storageclass.storage.k8s.io/delayed-volume-sc created

controlplane ~ ➜  k get pvc delayed-volume-sc
Error from server (NotFound): persistentvolumeclaims "delayed-volume-sc" not found

controlplane ~ ✖ k get pvc
NAME        STATUS   VOLUME     CAPACITY   ACCESS MODES   STORAGECLASS    AGE
local-pvc   Bound    local-pv   500Mi      RWO            local-storage   21m




