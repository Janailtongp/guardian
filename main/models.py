from django.db import models

import os
import uuid
import hashlib
from urllib.parse import urlencode
from datetime import date
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
)
from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage

from typing import Dict, List, Optional, Tuple
# Create your models here.

from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = "auth_user"
        ordering = ("name",)

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    username = models.CharField(
        max_length=50,
        unique=True,
        help_text=(
            "Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[
            validators.RegexValidator(
                r"^[\w.@+-]+$",
                (
                    "Enter a valid username. "
                    "This value may contain only letters, numbers "
                    "and @/./+/-/_ characters."
                ),
                "invalid",
            )
        ],
        error_messages={
            "unique": ("A user with that username already exists.")
        },
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def get_api_token(self) -> Optional[str]:
        token:  Optional[Token] = Token.objects.filter(user=self).first()
        if token:
            return token.key
        return None

    def gravatar_url(self) -> str:
        email_encoded: bytes = self.email.lower().encode('utf-8')
        email_hash: str = hashlib.sha256(email_encoded).hexdigest()
        params: str = urlencode({'s': '300'})
        return f"https://www.gravatar.com/avatar/{email_hash}?{params}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class PerfilManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Client(models.Model):
    legal_name = models.fields.CharField(
        verbose_name="Nome legal",
        max_length=255
    )
    cnpj = models.fields.CharField(
        verbose_name="CNPJ",
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )
    cpf = models.fields.CharField(
        verbose_name="CPF",
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )
    collaborators = models.ManyToManyField(
        User,
        verbose_name="Colaboradores",
        help_text="Colaboradores possuem acesso a processos da empresa",
        blank=True
    )
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self) -> str:
        return f"{self.legal_name} ({self.get_registration()})"

    def clean(self) -> None:
        if not (self.cnpj or self.cpf):
            raise ValidationError(
                "Pelo menos um dos campos CNPJ ou CPF é obrigatório"
            )

    def get_registration(self) -> str:
        return self.cnpj or self.cpf


def attachment_unic_path(instance, filename):
    """Função usada no upload_to do Anexo para calcular um nome único."""
    filename, file_extension = os.path.splitext(filename)
    filename = "{}_{}{}".format(filename, uuid.uuid4(), file_extension)
    return os.path.join("attachments/", filename)


class Attachment(models.Model):
    file = models.FileField(
        upload_to=attachment_unic_path, max_length=300, blank=True
    )
    local_file = models.FileField(
        storage=FileSystemStorage(),
        blank=True,
        upload_to="devta/",
        max_length=1024,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("file",)

    def get_size(self) -> str:
        GB: int = 1024 ** 3
        MB: int = 1024 ** 2
        KB: int = 1024

        size: int = self.file.size or 0
        if int(size / GB) > 0:
            return "{:.2f} GB".format((size / GB))
        elif int(size / MB) > 0:
            return "{:.2f} MB".format((size / MB))
        elif int(size / KB) > 0:
            return "{:.2f} KB".format((size / KB))
        return f"{size} Bytes"

    def get_filename_elipsys(self):
        name: str = self.get_realy_filename()
        if len(name) <= 30:
            return name
        return name[:30] + b" ..."

    def get_realy_filename(self) -> str:
        """Return the name witout UUID4."""
        name: str = ""
        if self.file:
            name = self.file.name
        if not name and self.local_file:
            name = self.local_file.name
        name = "_".join(os.path.basename(name).split("_")[:-1])
        return name.encode("utf-8")

    def get_ext(self) -> Optional[str]:
        name: Optional[str] = self.file.name
        if not name and self.local_file:
            name = self.local_file.name
        splitted = os.path.splitext(name)
        if len(splitted) == 2 and splitted[1]:
            return splitted[1]
        return None

    def get_file_object(self):
        if self.file.name:
            return self.file
        return self.local_file

    def get_raw_filename(self) -> str:
        """Returns the name of the file with the UUID4."""
        name: Optional[str] = self.file.name
        if not name and self.local_file:
            name = self.local_file.name
        return os.path.splitext(name)[0]

    def get_url(self) -> str:
        url: str = ""
        if self.file:
            url = self.file.url
        elif self.local_file:
            url = self.local_file.url
        return url

    def __str__(self) -> str:
        return "Attachment: {}".format(self.get_realy_filename())


class RoutineType(models.Model):
    name = models.fields.CharField(max_length=255, blank=False, null=False)
    code = models.fields.IntegerField(blank=False, null=False)
    description = models.fields.TextField(max_length=255, blank=True)

class Routine(models.Model):
    name = models.fields.CharField(max_length=255, blank=False, null=False)
    type = models.ForeignKey(RoutineType, on_delete=models.CASCADE, blank=False, null=False)
    description = models.fields.TextField(max_length=255, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False, null=False)
    provider_name = models.fields.CharField(max_length=255, blank=False, null=False)
    provider_cnpj = models.fields.CharField(max_length=255, blank=False, null=False)
    
    participants = models.ManyToManyField(
        User,
        related_name="users",
    )

    external_users = models.ManyToManyField(
        User,
        related_name="guests",
    )

    attachments = models.ManyToManyField(
        Attachment,
        related_name="docs",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # sequence in the created year
    sequence = models.IntegerField(null=False, blank=False)
    
    
    def clean(self) -> None:
        if not (self.pk or self.sequence):
            self.sequence = Routine.objects.filter(
                created_at__year=date.today().year
            ).count() + 1
    
    def get_code(self) -> str:
        return f"{str(self.sequence).zfill(4)}/{self.created_at.year}"