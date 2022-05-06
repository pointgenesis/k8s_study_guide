# Docker Security

## Security

Containers run in a namespace that is isolated from processes outside of itself.

Processes can have different PIDs in different namespaces.

Docker runs processes as the root user. If you do not want the process to run 
as root, then specify the USER to run.

The root user of the container is not really the same as the root user of the 
system.

### Linux Capabilities

- chown
- dac
- kill
- setfcap
- setpcap
- setgid
- setuid
- net_bind
- net_raw
- mac_admin
- broadcast
- net_admin
- sys_admin
- sys_chroot
- audit_write
- ...many more...

Reference
~~~
/usr/include/linux/capability.h
~~~

## Container Security

Docker has a limited set of available capabilities, but you can override this
behavior and allow selected Linux command capabilities. These can only be 
applied at the container-level and not at the more fine-grained level in the
pod.

### Kubernetes Security

Containers are encapsulated in pods. You can configure security settings at a 
container-level or at the pod-level.

When security settings are applied at the pod level, then the settings are 
carried over to all containers in the pod.

The pod settings will override the settings at the container level when both
pod-level and container-level security settings are set.

### Security Context

#### Pod-level Security

~~~yaml
apiVersion: v1
kind: Pod
metadata: 
  name: my-web-pod
  labels:
    name: my-web-pod
spec:
  securityContext:
    runAsUser: 1000
  containers:
    - name: ubuntu
      image: ubuntu
      command: ["sleep", "3600"]
~~~

#### Container-level Security

Note: The `capabilities` feature is only applicable at the container level
as seen in the following example.

~~~yaml
apiVersion: v1
kind: Pod
metadata: 
  name: my-web-pod
  labels:
    name: my-web-pod
spec:
  containers:
    - name: ubuntu
      image: ubuntu
      command: ["sleep", "3600"]
      securityContext:
        runAsUser: 1000
        capabilities:
          add: ["MAC_ADMIN"]
~~~