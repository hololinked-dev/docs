cd vps-maintenance
git sparse-checkout init --cone
git sparse-checkout set cluster/manifests/helm/apps cluster/manifests/helm/ingress
git sparse-checkout reapply
cd ..