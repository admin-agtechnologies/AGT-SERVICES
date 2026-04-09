"""
Commande Django : génération des clés RSA RS256.
Usage : python manage.py generate_keys
"""
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Génère les clés RSA RS256 pour la signature JWT."

    def add_arguments(self, parser):
        parser.add_argument("--output-dir", type=str, default="keys", help="Dossier de sortie")
        parser.add_argument("--key-size", type=int, default=2048, help="Taille de la clé (bits)")

    def handle(self, *args, **options):
        output_dir = Path(options["output_dir"])
        output_dir.mkdir(parents=True, exist_ok=True)

        private_key = rsa.generate_private_key(public_exponent=65537, key_size=options["key_size"])

        private_path = output_dir / "private.pem"
        private_path.write_bytes(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
        private_path.chmod(0o600)

        public_path = output_dir / "public.pem"
        public_path.write_bytes(private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ))

        self.stdout.write(self.style.SUCCESS(f"Clés générées : {private_path}, {public_path}"))
