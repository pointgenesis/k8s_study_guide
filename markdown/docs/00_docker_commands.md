# Docker Commands

## Run Image

The run command will run an image of the docker container from the local host if it exists.
If the image does not exist, then docker will first reach out to the docker hub and download
a copy to the local machine. Subsequent executions will use the local image copy.

``` 
docker run nginx
```

## List Containers

#### ps

Lists all **running** containers.

``` 
docker ps
```

#### ps -a

List all containers regardless of status. Both running, terminated, pending, etc. containers
will be displayed.

``` 
docker ps -a
```

## Stop Containers

#### stop <container-name>

``` 
docker stop scary_sally
```

**Note: Docker automatically generates a random name for containers.**

## Remove Container

#### rm <container-name>

``` 
docker rm scary_sally
```

## List Images

#### images

``` 
docker images
```

## Remove Images

#### rmi <image-name>

``` 
docker rmi nginx
```

You cannot delete an image that has active references. Verify that no containers are dependent
on the image before attempting to delete.

## Get Latest Image

#### pull <image-name>

``` 
docker pull nginx
```

## Execute a Command

#### exec <container-name> <command-statement>

``` 
docker exec pretty_horse_32 cat /etc/hosts
```

## Attached vs Detached Mode

By default, the docker run command executes in the attached mode. This means the command prompt
is not available for user input. The process must terminate, generally, by the user pressing
the CTRL+C keys to quit.

#### Attached Mode

``` 
docker run some-kind-of-monster
```

There is another mode where the user is able to use the terminal. The process is kicked off
and is running in the background, but the user is free to proceed in the foreground. 