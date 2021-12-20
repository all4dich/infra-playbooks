# infra-playbooks
This repository keeps Ansible or other toolkits artifacts  to manage  Nota's development infra

## jenkins-env
### How to deploy 
Run `docker-compoe up -d` command on 'jenkins-env' directory

## nexus-oss
### How to deploy/redeploy
1. Host에서  Nexus 실행 데이타를 저장할 위치를 결정합니다.
> 예. /raid1/data/nota/nexus-oss
2. run-nexus-oss.sh /raid1/data/nota/nexus-oss 를 실행합니다. 
3. docker-compose ps 명령을 실행하여  다음과 같이 서비스 목록 및 port mapping 정보를 확인합니다.
```
[~/work-remote/nota-github/infra-playbooks/nexus-oss]$ docker-compose ps
          Name                         Command               State                                                            Ports
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
nexus-oss_nexus_service_1   sh -c ${SONATYPE_DIR}/star ...   Up      0.0.0.0:35000->35000/tcp,:::35000->35000/tcp, 0.0.0.0:35001->35001/tcp,:::35001->35001/tcp,
                                                                     0.0.0.0:35002->35002/tcp,:::35002->35002/tcp, 0.0.0.0:35003->35003/tcp,:::35003->35003/tcp,
                                                                     0.0.0.0:8081->8081/tcp,:::8081->8081/tcp
[~/work-remote/nota-github/infra-playbooks/nexus-oss]$
```

### How to stop the running Nexus oss
1. docker-compose ps 명령으로, Nexus OSS 서비스가 실행중인지 확인합니다.
```
[~/work-remote/nota-github/infra-playbooks/nexus-oss]$ docker-compose ps
          Name                         Command               State                                                            Ports
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
nexus-oss_nexus_service_1   sh -c ${SONATYPE_DIR}/star ...   Up      0.0.0.0:35000->35000/tcp,:::35000->35000/tcp, 0.0.0.0:35001->35001/tcp,:::35001->35001/tcp,
                                                                     0.0.0.0:35002->35002/tcp,:::35002->35002/tcp, 0.0.0.0:35003->35003/tcp,:::35003->35003/tcp,
                                                                     0.0.0.0:8081->8081/tcp,:::8081->8081/tcp
[~/work-remote/nota-github/infra-playbooks/nexus-oss]$
```
2. docker-compose down 명령을 실행합니다. 
3. docker-compose ps 명령으로 실행중인 서비스가 없음을 확인합니다.
```
[~/work-remote/nota-github/infra-playbooks/nexus-oss]$ docker-compose ps
          Name                         Command               State                                                            Ports
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
[~/work-remote/nota-github/infra-playbooks/nexus-oss]$
```

### How to terminate the existing Nexus oss service
1. Host 에서 Nexus Data 를 저장하고 있는 경로를 확인합니다.
> 예. /raid1/data/nota/nexus-oss 
2. 다음의 명령을 실행합니다. 실행중인 Container runtime 은 물론, Local의 데이타까지 모두 삭제합니다. 
```shell
 ./clear-nexus-service.sh  /raid1/data/nota/nexus-oss  
```
