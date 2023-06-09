# Cluster Configuration

## Getting Started

### Hub Cluster (groundbreaker-acm)

- install Red Hat OpenShift GitOps Operator
- bootstrap hub cluster ArgoCD instance and [link ArgoCD to ACM](https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes/2.6/html/applications/managing-applications#prerequisites-argo)

```
$ oc apply -k groundbreaker-acm/argocd
```

| File | Purpose |
| ---- | ------- |
| argocd.yaml | Changes to the OpenShift GitOps cluster install of Argo CD |
| gitopscluster.yaml, placement.yaml | Sets up the link between ACM and openshift-gitops |
| managedclustersetbinding.yaml | Adds the ACM ClusterSet grouping to ArgoCD |

Once the links are made, ACM will populate the clusters based on the placement rule in the Argo CD instance in the openshift-gitops namespace.

### Configure ArgoCD

Since we are using a private repo on GitHub we have to configure ArgoCD to use a token for authentication.

```
$ ssh-keygen -m pem -f groundbreaker-demo-deploy-key
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

By default, users have no permissions in the cluster-wide ArgoCD. We will add our user to a cluster-admins group to debug ArgoCD directly.

```
$ oc adm groups new cluster-admins
$ oc adm groups add-users cluster-admins <your username>
```

### Deploy Cluster Certificate Management Applications

Now we can deploy the ApplicationSets that manage the cert-manager operator as well as the resources that manage updating the default ingress and API server certificates.

```
$ oc apply -f cluster-config/global/applications/cert-manager-operator.yaml
$ oc apply -f cluster-config/global/applications/cluster-certificates.yaml
```