# Cluster Configuration

This directory holds all of the cluster configuration pushed by ACM to the managed clusters

## Repository Filesystem Layout

| Directory | Purpose |
| ---- | ------- |
| applications/ | Where the ApplicationSets that ACM uses on the hub to configure the managed clusters |
| clusters/ | Using Kustomize we build off of the configs in global/ and customize them for the specific cluster |
| global/ | Where all of the generic Kubernetes deployment YAML is |

## Getting Started

### Hub Cluster (groundbreaker-acm)

- install Red Hat OpenShift GitOps Operator
- bootstrap hub cluster ArgoCD instance and link ArgoCD to ACM [(upstream doc)](https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes/2.6/html/applications/managing-applications#prerequisites-argo) 
using the manifests in `groundbreaker-acm/argocd`

```
$ oc apply -k groundbreaker-acm/argocd
```

| File | Purpose |
| ---- | ------- |
| argocd.yaml | Changes to the OpenShift GitOps cluster install of Argo CD |
| gitopscluster.yaml, placement.yaml | Sets up the link between ACM and openshift-gitops |
| managedclustersetbinding.yaml | Adds the ACM ClusterSet `global` and `default` groupings to ArgoCD |

Once the links are made, ACM will populate the clusters based on the placement rule in the Argo CD instance in the openshift-gitops namespace.

### Configure ArgoCD for GitHub Repository

Since we are using a private repo on GitHub we have to configure ArgoCD to use a token for authentication.

```
$ ssh-keygen -m pem -f groundbreaker-demo-deploy-key
```
```
$ cat <<EOF | oc create -f -
apiVersion: v1
kind: Secret
metadata:
  name: groundbreaker-demo-repo
  namespace: openshift-gitops
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  type: git
  url: git@github.com:rh-nspdev/groundbreaker-demo.git
  insecure: "true"
  sshPrivateKey: |
$(cat groundbreaker-demo-deploy-key | sed 's/^/    /')
EOF
```

Add the public key to the list of [deploy keys for the repository.](https://github.com/rh-nspdev/groundbreaker-demo/settings/keys)

#### Debugging ArgoCD

:warning: This section is only required if you are debugging things in the ArgoCD UI and need read/write access to ArgoCD directly! :warning:

By default, users have no permissions in the cluster-wide ArgoCD deployed into the `openshift-gitops` namespace. We will add our user to a cluster-admins group to debug ArgoCD directly.

```
$ oc adm groups new cluster-admins
$ oc adm groups add-users cluster-admins <your username>
```

We are using [sync phases](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/) extensively with ArgoCD to place resources in a particular order.

### Deploy Cluster Secrets Management

We will use a lower-level Hive (underneath ACM Cluster Management) resource called a SyncSet to deploy
secrets to nodes. We want to do this because we need to "push" secrets to the managed clusters from the
hub cluster but without storing them in Git.

Alternatively we could use some central secret store like Vault but that is out of scope for this project.

Another strategy would be to use ACM's ManifestWork which is similar but would require applying to each cluster
indivdually, this way we only apply one resource and it works for all.

```
$ cat <<EOF | oc create -f -
apiVersion: hive.openshift.io/v1
kind: SelectorSyncSet
metadata:
  name: secrets
spec:
  clusterDeploymentSelector:
    matchLabels:
      vendor: OpenShift

  resources:
  - apiVersion: v1
    kind: Secret
    metadata:
      name: google-client-secret
      namespace: openshift-config
    data:
      clientSecret: (base64-encoded client secret from google)
EOF
```

### Deploy Cluster Certificate Management

Now we can deploy the ApplicationSet that manages the cert-manager operator as well as the resources that manage updating the default ingress and API server certificates.

Note: Managed clusters may go offline as a result of changing the API certificates, [ACM has documentation on how to fix it](https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes/2.7/html-single/troubleshooting/index#identifying-clusters-offline-after-certificate-change)

```
$ oc apply -f cluster-config/applications/cluster-certificates.yaml
```

We can also deploy our base configuration

```
$ oc apply -f cluster-config/applications/base-config.yaml
```
