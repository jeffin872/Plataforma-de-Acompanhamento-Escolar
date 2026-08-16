"""
Abstração do "Serviço de armazenamento em nuvem" citado na documentação
do projeto. A ideia é que o resto do sistema nunca fale diretamente com
S3/Cloudinary/disco: ele só chama `storage.salvar(arquivo)` e recebe uma
URL de volta, então trocar o backend de armazenamento não exige mudar
nenhuma rota.

Backend padrão: "local" (grava em backend/instance/uploads/), que já
funciona sem nenhuma credencial extra - ótimo para desenvolvimento e para
a apresentação do MVP. Para produção, basta configurar STORAGE_BACKEND=s3
e as variáveis AWS_* no .env (é necessário instalar `boto3`, que não vem
no requirements.txt padrão para manter o setup local mais leve).
"""
import os
import uuid
from abc import ABC, abstractmethod

from flask import current_app
from werkzeug.utils import secure_filename

EXTENSOES_PERMITIDAS = {"pdf", "png", "jpg", "jpeg"}


def extensao_permitida(nome_arquivo: str) -> bool:
    return (
        "." in nome_arquivo
        and nome_arquivo.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS
    )


class StorageBackend(ABC):
    @abstractmethod
    def salvar(self, arquivo, nome_original: str) -> str:
        """Salva o arquivo e devolve a URL/caminho para acessá-lo depois."""
        raise NotImplementedError


class LocalStorage(StorageBackend):
    """Guarda o arquivo em disco, dentro da pasta instance/uploads."""

    def salvar(self, arquivo, nome_original: str) -> str:
        pasta = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(pasta, exist_ok=True)

        nome_seguro = secure_filename(nome_original)
        nome_unico = f"{uuid.uuid4().hex}_{nome_seguro}"
        caminho_completo = os.path.join(pasta, nome_unico)
        arquivo.save(caminho_completo)

        # Em desenvolvimento devolvemos um caminho servido pela própria API.
        return f"/api/documentos/arquivo/{nome_unico}"


class S3Storage(StorageBackend):
    """
    Implementação de referência para Amazon S3 (ou compatíveis, como
    Cloudinary/Wasabi/MinIO ajustando o endpoint_url). Requer `boto3`
    instalado e as credenciais no .env.
    """

    def __init__(self):
        import boto3  # import tardio: só é necessário se STORAGE_BACKEND=s3

        self.bucket = current_app.config["AWS_S3_BUCKET"]
        self.cliente = boto3.client(
            "s3",
            region_name=current_app.config["AWS_S3_REGION"],
            aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
        )

    def salvar(self, arquivo, nome_original: str) -> str:
        nome_seguro = secure_filename(nome_original)
        chave = f"documentos/{uuid.uuid4().hex}_{nome_seguro}"
        self.cliente.upload_fileobj(arquivo, self.bucket, chave)
        return (
            f"https://{self.bucket}.s3.{current_app.config['AWS_S3_REGION']}"
            f".amazonaws.com/{chave}"
        )


def get_storage() -> StorageBackend:
    backend = current_app.config.get("STORAGE_BACKEND", "local")
    if backend == "s3":
        return S3Storage()
    return LocalStorage()
