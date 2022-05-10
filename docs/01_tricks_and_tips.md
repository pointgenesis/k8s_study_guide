# Tips and Tricks

## Setting a Context and Namespace
`$ kubectl config set-context <context-of-question> --namespace=<namespace-of-question>`

## Using an Alias for kubectl
`$ alias k=kubectl`

`$ k version`

## Internalize Resource Short Names
`$ kubectl api-resources`

### Example Command Usage
`$ kubectl describe pvc my-claim`

## Force Delete Objects
`$ kubectl delete pod nginx --grace-period=0 --force`

## Finding Object Information Quickly
`$ kubectl describe pods | grep -iC 10 "author=John Doe`

`$ kubectl get pods -o yaml | grep -c 5 labels:`

## Quick Command Reference

### Command level Help
`$ kubectl <command-to-lookup> --help`

`$ kubectl create --help`

### Using the explain Option
`$ kubectl explain <command-to-lookup>`

`$ kubectl explain pods.spec`

### Watch resources as they transition through states
`$ kubectl get pod redis --watch`