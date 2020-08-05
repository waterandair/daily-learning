#### Use Operator
```shell script
kubectl apply --namespace="clickhouse-operator" -f <( \
    curl -s https://raw.githubusercontent.com/Altinity/clickhouse-operator/master/deploy/operator/clickhouse-operator-install-template.yaml | \
        OPERATOR_IMAGE="${OPERATOR_IMAGE}" \
        OPERATOR_NAMESPACE="${OPERATOR_NAMESPACE}" \
        METRICS_EXPORTER_IMAGE="${METRICS_EXPORTER_IMAGE}" \
        METRICS_EXPORTER_NAMESPACE="${METRICS_EXPORTER_NAMESPACE}" \
        envsubst \
)
```