
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import boto3


def _load_dotenv_if_present(env_path: Optional[Path] = None) -> None:
    """
    Cargador muy liviano de .env (KEY=VALUE) para entornos donde docker-compose no inyecta.
    - No sobreescribe variables ya definidas en el entorno.
    - Soporta comentarios (#) y valores entre comillas simples o dobles.
    """
    if env_path is None:
        env_path = Path(__file__).parent / ".env"

    try:
        if not env_path.exists():
            return
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            if key and key not in os.environ:
                os.environ[key] = value
    except Exception:
        # Silencioso a propósito: si el .env está malformado, preferimos que falle boto3
        # con un error más claro de credenciales / región.
        return


def _get_region() -> str:
    return (
        os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or os.getenv("REGION_NAME")
        or "us-east-1"
    )


def _get_secrets_manager_secret_id() -> Optional[str]:
    return (
        os.getenv("AWS_SECRETS_MANAGER_SECRET_ID")
        or os.getenv("AWS_SECRET_ID")
        or os.getenv("AWS_SECRET_NAME")
    )


def _fetch_secret_json(secret_id: str, region_name: str) -> Dict[str, Any]:
    """
    Lee un secret desde AWS Secrets Manager. Se espera un JSON.
    Ejemplo:
      {
        "AWS_ACCESS_KEY_ID": "...",
        "AWS_SECRET_ACCESS_KEY": "...",
        "AWS_SESSION_TOKEN": "...(opcional)...",
        "AWS_REGION": "us-east-1"
      }
    """
    client = boto3.client("secretsmanager", region_name=region_name)
    res = client.get_secret_value(SecretId=secret_id)
    secret_str = res.get("SecretString")
    if not secret_str:
        raise RuntimeError(f"El secret '{secret_id}' no tiene SecretString (solo binario).")
    try:
        return json.loads(secret_str)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"El secret '{secret_id}' no es JSON válido: {e}") from e


def create_boto3_session() -> boto3.session.Session:
    """
    Crea una sesión boto3 usando:
    1) Secrets Manager (si se configura AWS_SECRETS_MANAGER_SECRET_ID / AWS_SECRET_NAME)
    2) En caso contrario, la cadena estándar de credenciales de AWS (env/profile/role)
    """
    _load_dotenv_if_present()
    region_name = _get_region()

    secret_id = _get_secrets_manager_secret_id()
    if not secret_id:
        return boto3.Session(region_name=region_name)

    secret = _fetch_secret_json(secret_id=secret_id, region_name=region_name)

    access_key = secret.get("AWS_ACCESS_KEY_ID") or secret.get("aws_access_key_id")
    secret_key = secret.get("AWS_SECRET_ACCESS_KEY") or secret.get("aws_secret_access_key")
    session_token = secret.get("AWS_SESSION_TOKEN") or secret.get("aws_session_token")
    region_from_secret = secret.get("AWS_REGION") or secret.get("AWS_DEFAULT_REGION")

    if not access_key or not secret_key:
        raise RuntimeError(
            f"El secret '{secret_id}' debe incluir AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY."
        )

    return boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token,
        region_name=region_from_secret or region_name,
    )


def get_dynamodb_resource() -> boto3.resources.base.ServiceResource:
    _load_dotenv_if_present()
    session = create_boto3_session()
    endpoint_url = os.getenv("DYNAMODB_ENDPOINT_URL") or None
    region_name = _get_region()
    return session.resource("dynamodb", region_name=region_name, endpoint_url=endpoint_url)


def get_dynamodb_client() -> boto3.client:
    _load_dotenv_if_present()
    session = create_boto3_session()
    endpoint_url = os.getenv("DYNAMODB_ENDPOINT_URL") or None
    region_name = _get_region()
    return session.client("dynamodb", region_name=region_name, endpoint_url=endpoint_url)

