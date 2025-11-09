#!/bin/bash
# Security monitoring script - ניטור התקפות ועלויות

echo "🛡️  Security & Cost Monitoring Report"
echo "====================================="

echo ""
echo "📊 Rate Limiting Status:"
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx --tail=50 | grep "rate limit\|429\|auth"

echo ""
echo "🚨 Failed Authentication Attempts:"
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx --tail=100 | grep "401\|403" | wc -l

echo ""
echo "💰 Request Count (Cost Estimation):"
echo "Total requests in last 10 minutes:"
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx --since=10m | grep "service-a" | wc -l

echo ""
echo "⚠️  Blocked IPs (High failure rate):"
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx --tail=200 | grep "401" | awk '{print $1}' | sort | uniq -c | sort -nr | head -5

echo ""
echo "✅ Legitimate Access:"
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx --tail=50 | grep "200.*service-a" | tail -5