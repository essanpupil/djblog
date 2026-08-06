{{- define "djblog.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{- define "djblog.labels" -}}
app.kubernetes.io/name: {{ include "djblog.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "djblog.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{- define "djblog.secretName" -}}
{{- if .Values.secret.existingSecret }}
{{- .Values.secret.existingSecret -}}
{{- else if .Values.secret.enabled }}
{{- .Values.secret.name -}}
{{- else -}}
{{- "" -}}
{{- end -}}
{{- end -}}

{{- define "djblog.redisServiceName" -}}
{{- printf "%s-redis" (include "djblog.fullname" .) -}}
{{- end -}}
