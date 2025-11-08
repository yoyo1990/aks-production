# AKS Production-Ready Demo (עברית / English)

מטרה: לפרוס באופן אוטומטי אשכול AKS ב-Azure עם שתי אפליקציות (Service A ו-Service B) המדגימות IaC (Terraform), אבטחה (RBAC, NetworkPolicy), ותזמור מיקרו-שירותים (Ingress, Probes).

---

## מה נמצא בתיקייה

- `infra/` - Terraform לפריסת Resource Group, ACR, AKS (RBAC מופעל). ערוך את `variables.tf` לפני `terraform apply`.
- `app-a/` - קוד Python (fetch BTC כל דקה) + Dockerfile
- `app-b/` - placeholder container שמריץ HTTP פשוט
- `k8s/` - manifests: Deployments, Services, Ingress, NetworkPolicy
- `docs/deploy.sh` - תסריט אוטומציה לדוגמה (ניתן להריץ ב-Bash)

## דגשים חשובים

1. Network Policy
   - `k8s/network-policy.yaml` מיישם מדיניות שמגבילה כניסות ל-Service B כך ש-`service-a` לא יוכלו לתקשר ל-`service-b` אלא אם כן נוספים לכללים נוספים.
   - הערה: יישום מדיניות תלוי ב-network plugin של ה-cluster (AKS עם `network_policy = "azure"` תומך).

2. Liveness / Readiness Probes
   - `app-a` מספק נתיבי `/healthz` (liveness) ו-`/ready` (readiness).
   - Probes מוגדרים ב-`k8s/deployment-a.yaml` עם זמני המתנה ו-threshold מתאימים.

3. Resource Limits/Requests
   - מוגדרים ב-YAML כדי למנוע שימוש יתר במשאבים ולסייע scheduler.

## הוראות פריסה (תקציר)

1. Terraform (infra):
   - עדכן `infra/variables.tf` (למשל `acr_name`) עם ערכים תקפים.
   - `terraform init` ו-`terraform apply` (או השתמש ב-`docs/deploy.sh`).
   - לאחר הסיום: `terraform destroy` כדי למנוע חיובים.

2. בניית ודחיפת תמונות (דוגמה):
   - השתמש ב-output `acr_login_server` כדי לתייג את התמונות.
   - דוגמה ב-PowerShell (שים לב להחליף ערכים):

```powershell
# אמור להיות אחרי terraform apply ו-
$ACR = "<YOUR_ACR_LOGIN>.azurecr.io"
docker build -t $ACR/service-a:latest ./app-a
docker build -t $ACR/service-b:latest ./app-b
docker push $ACR/service-a:latest
docker push $ACR/service-b:latest
```

3. קבלת קונפיג של kube ופריסה:

```powershell
az aks get-credentials --resource-group <rg> --name <aks_cluster_name>
kubectl apply -f k8s/
```

4. מציאת ה-Ingress URL:

```powershell
kubectl get ingress services-ingress -o wide
# או
kubectl get svc -n ingress-nginx
```

## בדיקות מהירות

- בדוק ש-`/service-A/metrics` דרך ה-Ingress מחזיר JSON עם moving_average.
- בדוק `kubectl get pods` ו-`kubectl describe pod <pod>` כדי לאמת probes
- בדוק מדיניות רשת: נסה `kubectl exec` מפוד של service-a ל-service-b וודא שהתקשורת נחסמת.

## עלויות ותזכורת

הפעלת AKS ו-VMs יוצרת עלויות. הרץ `terraform destroy` לאחר הבדיקה.

