# 🚀 AKS Production System - מערכת אבטחה מתקדמת

## 📋 מה השתנה:
✅ **Security Context** מתקדם בכל הPods  
✅ **Namespace מאובטח** עם Pod Security Standards  
✅ **Network Policies** מתקדמות  
✅ **Resource Limits** למניעת DoS  
✅ **ServiceAccount** עם הרשאות מינימליות  

---

## 🎯 איך להפעיל הכל (פעם אחת!):

### 1. 🏗️ תשתית:
```bash
cd infra
terraform init
terraform plan
terraform apply
```

### 2. 🛡️ הפעלת אבטחה:
```bash
# יצירת namespace מאובטח
kubectl apply -f k8s/namespace.yaml

# הפעלת Network Policies
kubectl apply -f k8s/network-policy.yaml
kubectl apply -f k8s/advanced-network-policies.yaml

# פריסת האפליקציות (עם אבטחה!)
kubectl apply -f k8s/deployment-a.yaml
kubectl apply -f k8s/deployment-b.yaml
kubectl apply -f k8s/service-a.yaml
kubectl apply -f k8s/service-b.yaml

# הפעלת Ingress עם authentication
kubectl apply -f k8s/auth-secret.yaml
kubectl apply -f k8s/ingress.yaml
```

### 3. ✅ בדיקה:
```bash
kubectl get pods -n bitcoin-app
kubectl get networkpolicies -n bitcoin-app
kubectl describe limitrange -n bitcoin-app
```

---

## 🔐 מה האבטחה כוללת:

### 🛡️ **ברמת Pod:**
- Non-root execution
- Read-only filesystem (כשאפשר)
- Drop ALL capabilities  
- No privilege escalation

### 🌐 **ברמת רשת:**
- בידוד service-a מ-service-b
- חסימת גישה לmetadata servers
- הגבלת פורטים לרק מה שצריך
- Basic Authentication על Ingress

### 📊 **ברמת משאבים:**
- CPU/Memory limits
- Request limits
- Pod Security Standards = "restricted"

### 🔑 **ברמת הרשאות:**
- ServiceAccount מינימלי
- RBAC restricted
- Namespace isolation

---

## 💡 **חשוב להבין:**

### ❌ **לא צריך להפעיל בכל פעם!**
- הקבצים = **תצורה קבועה**
- Kubernetes זוכר ומפעיל אוטומטית
- רק כשמשנים קוד = `kubectl apply` שוב

### ✅ **מתי להריץ שוב:**
- שינוי בקוד האפליקציה → בנה Docker image חדש
- שינוי ב-YAML files → `kubectl apply`
- שינוי בTerraform → `terraform apply`

---

## 🎉 **התוצאה:**
מערכת production-ready עם **5 שכבות אבטחה חינמיות!**