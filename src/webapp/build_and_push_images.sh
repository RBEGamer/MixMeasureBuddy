#!/usr/bin/env bash

set -euo pipefail

# Usage:
#   REGISTRY=registry.example.com/myorg ./scripts/build_and_push_images.sh
# Environment:
#   REGISTRY (required) - Docker registry/repository prefix, e.g. ghcr.io/myorg
#   TAG (optional)      - image tag (default: latest)
#   DOCKERFILE_BACKEND (optional)  - path to backend Dockerfile
#   DOCKERFILE_WEB (optional)      - path to web Dockerfile
#   DOCKERFILE_PROXY (optional)    - path to proxy Dockerfile
#   CONTEXT (optional)             - root context directory (default: src/webapp)

main() {
  local registry="${REGISTRY:-}"
  local tag="${TAG:-latest}"
  local context="${CONTEXT:-$(dirname "$0")}"
  local folder_backend="${DOCKERFILE_BACKEND:-${context}/backend}"
  local folder_frontend="${DOCKERFILE_WEB:-${context}/frontend}"
  local folder_proxy="${DOCKERFILE_PROXY:-${context}/nginx}"
  local dockerfile_backend="${FOLDER_BACKEND:-${folder_backend}/Dockerfile}"
  local dockerfile_frontend="${DOCKERFILE_WEB:-${folder_frontend}/Dockerfile}"
  local dockerfile_proxy="${DOCKERFILE_PROXY:-${folder_proxy}/Dockerfile}"
  
  if [[ -z "${registry}" ]]; then
    echo "error: REGISTRY environment variable is required (e.g. REGISTRY=ghcr.io/myorg)" >&2
    exit 1
  fi

  echo "Building MixMeasureBuddy images with tag '${tag}' and registry '${registry}'"
  echo

  build_and_push \
    "${registry}/mixmeasurebuddy-suite-backend:${tag}" \
    "${dockerfile_backend}" \
    "${folder_backend}"

  build_and_push \
    "${registry}/mixmeasurebuddy-suite-frontend:${tag}" \
    "${dockerfile_frontend}" \
    "${folder_frontend}"

  build_and_push \
    "${registry}/mixmeasurebuddy-suite-proxy:${tag}" \
    "${dockerfile_proxy}" \
    "${folder_proxy}"

  echo
  echo "All images built and pushed successfully."
}

build_and_push() {
  local image="$1"
  local dockerfile="$2"
  local build_context="$3"

  echo ">>> Building ${image}"
  docker build \
    -f "${dockerfile}" \
    -t "${image}" \
    "${build_context}"

  echo ">>> Tagging ${image}"
  docker image tag "${image}" "${registry}/${image}"
  echo ">>> Pushing ${image}"
  #docker push "${image}"
  skopeo copy docker-daemon:${image} docker://"${registry}/${image}" --dest-tls-verify=false
  skopeo list-tags docker://"${registry}/${image}" --tls-verify=false
  echo
}

main "$@"
