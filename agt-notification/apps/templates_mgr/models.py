"""
AGT Notification Service v1.0 - Modeles : Template, TemplateVersion, TemplateVariable.
"""
import uuid
from django.db import models


class Template(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=20)
    platform_id = models.UUIDField(null=True, blank=True, db_index=True)
    category = models.CharField(max_length=30, default="transactional")
    is_active = models.BooleanField(default=True)
    created_by = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "templates"
        constraints = [models.UniqueConstraint(fields=["name", "platform_id"], name="unique_template_name_platform")]
        ordering = ["name"]

    def get_current_version(self, locale="fr"):
        version = self.versions.filter(is_current=True, locale=locale).first()
        if not version and locale != "fr":
            version = self.versions.filter(is_current=True, locale="fr").first()
        return version

    def render(self, variables, locale="fr"):
        from jinja2 import Environment
        version = self.get_current_version(locale)
        if not version:
            raise ValueError(f"Aucune version active pour '{self.name}' (locale: {locale})")
        env = Environment()
        subject = env.from_string(version.subject or "").render(**variables) if version.subject else None
        body = env.from_string(version.body).render(**variables)
        return {"subject": subject, "body": body}

    @classmethod
    def resolve(cls, name, platform_id=None, channel=None):
        qs = cls.objects.filter(name=name, is_active=True)
        if platform_id:
            tpl = qs.filter(platform_id=platform_id).first()
            if tpl:
                return tpl
        tpl = qs.filter(platform_id__isnull=True).first()
        if tpl:
            return tpl
        raise cls.DoesNotExist(f"Template '{name}' introuvable")


class TemplateVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name="versions")
    version = models.IntegerField()
    locale = models.CharField(max_length=10, default="fr")
    subject = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField()
    is_current = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "template_versions"
        ordering = ["-version"]
        unique_together = [("template", "version", "locale")]


class TemplateVariable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name="variables")
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    required = models.BooleanField(default=False)
    default_value = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "template_variables"
        unique_together = [("template", "name")]
