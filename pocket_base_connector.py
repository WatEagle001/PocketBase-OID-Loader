"""Salva i log in pocketbase."""

from pocketbase import PocketBase
from pocketbase.utils import ClientResponseError

import httpx
class PocketBaseClient:
    """Classe per l'interfacciamento di Pocketbase."""

    def __init__(
        self,
        pb_email: str,
        pb_password: str,
        pb_url: str = "http://lldockerservice01.ll-service.local:8083/",
        verify_ssl: bool = True,
    ) -> None:
        """Classe PocketBaseClient.

        Params:
        ------
        pb_email: e-email utente pocketbase, str
        pb_password: password utente pocketbase, str
        pb_url: base url dove risiede pocketbase, str
        verify_ssl: verifica o meno il certificato SSL, bool

        Returns
        -------
        None
        """
        self._pb_client = PocketBase(base_url=pb_url, http_client=httpx.Client(headers={"User-Agent": "Python OID Loader"}))
        self._pb_email = pb_email
        self._pb_password = pb_password
        self._user_auth()
        self._pb_notification_id: str = ""
        self._status_ids: list = []

    def _user_auth(self) -> None:
        """Autentica a PocketBase."""
        try:
            self._pb_client.collection("users").auth_with_password(
                username_or_email=self._pb_email, password=self._pb_password
            )
        except ClientResponseError as cre:
            print(cre)

    def save_sqs_message(self, vendor,service, oid) -> None:
        """Salva il messaggio SQS.

        Questa è la creazione del record, quindi di base salva il primo stato
        di creazione.

        Params:
        ------
        vedor: str
        service: str
        oid: str

        Returns
        -------
            None
        """
        # crea il messaggio nella collection
        pb_notification = self._pb_client.collection("oid_database").create(
            body_params={
                "vendor": vendor,
                "service": service,
                "oid": oid
                
            }
        )