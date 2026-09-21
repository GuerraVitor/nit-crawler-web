from django.db import models


class LattesReportRun(models.Model):
    STATUS_PENDING = "pending"
    STATUS_RUNNING = "running"
    STATUS_DONE = "done"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pendente"),
        (STATUS_RUNNING, "Em execução"),
        (STATUS_DONE, "Concluído"),
        (STATUS_FAILED, "Falhou"),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    extra_ids = models.JSONField(default=list, blank=True)
    ignored_duplicate_ids = models.JSONField(default=list, blank=True)
    log = models.TextField(blank=True, default="")
    error = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"LattesReportRun #{self.pk} ({self.status})"
