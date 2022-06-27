## Description
Pod annotator is a periodical kubectl runner that adds annotation to the pod.
In order not for auto scaler to evict Spark jobs when scaling down, We should attach annotations to all Spark pods.
However, AWS does not provide any config modifications for job-controller pod, where job-runner is. Due to this, Auto scaler keeps evicting job-controller pod, which results in spark job failure

## How it works
every 20 seconds, Pod annotator runs the crontab for `kubectl annotate` command to job-controller pods, so that it prevents from eviction.

```
kubectl annotate pods cluster-autoscaler.kubernetes.io/safe-to-evict='false'  -l "emr-containers.amazonaws.com/component=job.submitter" >> /var/log/cron.log 2>&1
```

## How To deploy 
1. change directory to pod-annotator
2. build the docker image and push it onto ECR Registry. 
   ```
   docker build . --build-arg AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY --build-arg AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY -t YOUR_TAG \
   && docker push YOUR_IMAGE
   ```
3. deploy YAML onto EMR namespace
    ```
   kubectl apply -f pod_annotator.yaml
    ```
