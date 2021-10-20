# HA Proxy builds

To debug and build locally you need to apply the following patch,
substituting the RPM of your choice:

```diff
From 469e5891b71c0ac30d6f110684e0e3e315f6d15e Mon Sep 17 00:00:00 2001
From: Andrew McDermott <amcdermo@redhat.com>
Date: Tue, 14 Jan 2020 18:47:45 +0000
Subject: [PATCH] build haproxy with proxmox support

---
 Makefile                         | 2 +-
 images/router/haproxy/Dockerfile | 7 +++++--
 2 files changed, 6 insertions(+), 3 deletions(-)

diff --git a/Makefile b/Makefile
index e866dff..c694232 100644
--- a/Makefile
+++ b/Makefile
@@ -30,7 +30,7 @@ all: build
 build:
	$(GO_BUILD_RECIPE)

-images/router/*/Dockerfile: images/router/base/Dockerfile
+images/router/*/Dockerfile: build
	imagebuilder -t registry.svc.ci.openshift.org/openshift/origin-v4.0:`basename $(@D)`-router -f images/router/`basename $(@D)`/Dockerfile .

 images/router/*/Dockerfile.rhel: images/router/base/Dockerfile.rhel
diff --git a/images/router/haproxy/Dockerfile b/images/router/haproxy/Dockerfile
index 1a646b1..857ce4e 100644
--- a/images/router/haproxy/Dockerfile
+++ b/images/router/haproxy/Dockerfile
@@ -1,5 +1,7 @@
-FROM registry.svc.ci.openshift.org/openshift/origin-v4.0:base-router
-RUN INSTALL_PKGS="haproxy20 rsyslog sysvinit-tools" && \
+FROM centos:7
+RUN rpm -ivh https://github.com/frobware/haproxy-hacks/raw/master/RPMs/PROXMOX-haproxy20-2.0.12-2.el7.x86_64.rpm
+RUN /usr/sbin/haproxy -vv
+RUN INSTALL_PKGS="procps-ng socat rsyslog sysvinit-tools" && \
	 yum install -y $INSTALL_PKGS && \
	 rpm -V $INSTALL_PKGS && \
	 yum clean all && \
@@ -10,6 +12,7 @@ RUN INSTALL_PKGS="haproxy20 rsyslog sysvinit-tools" && \
	 chown -R :0 /var/lib/haproxy && \
	 chmod -R g+w /var/lib/haproxy
 COPY images/router/haproxy/* /var/lib/haproxy/
+COPY openshift-router /usr/bin/openshift-router
 LABEL io.k8s.display-name="OpenShift HAProxy Router" \
	   io.k8s.description="This component offers ingress to an OpenShift cluster via Ingress and Route rules." \
	   io.openshift.tags="openshift,router,haproxy"
--
2.21.1
```

## Build

This will build the openshift-router locally, copying the binary into
the image:

	$ make images/router/haproxy/Dockerfile

	$ docker images | head
	REPOSITORY                                             TAG                 IMAGE ID            CREATED              SIZE
	registry.svc.ci.openshift.org/openshift/origin-v4.0    haproxy-router      ab9a5059f2b9        About a minute ago   278 MB

## Tag and push the image to a registry

	$ docker tag registry.svc.ci.openshift.org/openshift/origin-v4.0:haproxy-router frobware/router:next
	$ docker push frobware/router:next

## Disable CVO and Ingress controller

	$ oc scale deployment -n openshift-cluster-version cluster-version-operator --replicas=0
	deployment.apps/cluster-version-operator scaled

	$ oc scale deployment -n openshift-ingress-operator ingress-operator --replicas=0
	deployment.apps/ingress-operator scaled

## Use our new image

	$ oc set image deployment/router-default router=docker.io/frobware/router:next
	deployment.apps/router-default image updated
