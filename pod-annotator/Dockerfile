FROM ubuntu:20.04

USER root

RUN apt-get update -y
RUN apt-get install -y curl cron vim less unzip

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

RUN aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID \
    && aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY \
    && aws configure set default.region ap-northeast-2

#Install kubectl
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl

#Install aws-iam-authenticator
RUN curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.11.5/2018-12-06/bin/darwin/amd64/aws-iam-authenticator
RUN chmod +x ./aws-iam-authenticator
RUN mkdir $HOME/bin && cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator && export PATH=$HOME/bin:$PATH
RUN export PATH=$HOME/bin:$PATH
RUN aws eks --region ap-northeast-2 update-kubeconfig --name chai-production

# Change .kube config in order to enable cronjob to run aws command
RUN sed -i 's/command: aws/command: \/usr\/local\/bin\/aws/g' /root/.kube/config

# Cronjobs
COPY pod_annotate_cronjob /etc/cron.d/pod_annotate_cronjob

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/pod_annotate_cronjob
RUN crontab /etc/cron.d/pod_annotate_cronjob
RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log
