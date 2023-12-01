"""Salva i log in pocketbase."""

from dataclasses import asdict

from pocketbase import PocketBase
from pocketbase.utils import ClientResponseError


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
            :pb_email: e-email utente pocketbase, str
            :pb_password: password utente pocketbase, str
            :pb_url: base url dove risiede pocketbase, str
            :verify_ssl: verifica o meno il certificato SSL, bool

        Returns
        -------
            None
        """
        self._pb_client = PocketBase(base_url=pb_url)
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
            :sqs_message: messaggio SQS già preparato, SQSMessage

        Returns
        -------
            None
        """
        # prepara i campi base
        '''
        object_id: str = sqs_message.object_id
        vendor: str = sqs_message.vendor
        service: str = sqs_message.service
        oid :str = sqs_message.oid

        # converte in dizionario per l'inserimento nel DB
        # la funzione `__dict__` non è abbastanza
        body: dict = asdict(sqs_message.body)
        '''
        # crea il messaggio nella collection
        pb_notification = self._pb_client.collection("oid_database").create(
            body_params={
                "vendor": vendor,
                "service": service,
                "oid": oid
            }
        )
    '''
        # creami i vari stati nella collection
        # TODO: farlo più bello
        status_id_list: list = []
        for status in ["created", "processing", "notification_sent", "deleted"]:
            is_done: bool = False
            if status == "created":
                is_done = True
                # mettimi il creato già a True
            id_status = self._pb_client.collection("sqs_status").create(
                body_params={"message_id": message_id, "status_name": status, "is_done": is_done}
            )
            status_id_list.append(id_status.id)
            self._status_ids.append({"status_name": status, "id": id_status.id})

        self._pb_client.collection("sqs_notifications").update(
            id=pb_notification.id, body_params={"status": status_id_list}
        )

        self._pb_notification_id = pb_notification.id
            '''