#!/bin/bash



echo "start to apply kubenetes manifests"

for file in */manifests/*.yaml; do
    kubectl apply -f "$file"
done


