from sqlalchemy.orm import Session
from app.models import Client


def set_client_models(db: Session, client_id: str, embedding_model: str, llm_model: str) -> Client:
    """
    Create a new client or update existing client's models.
    """
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if client:
        client.embedding_model = embedding_model
        client.llm_model = llm_model
    else:
        client = Client(client_id=client_id, embedding_model=embedding_model, llm_model=llm_model)
        db.add(client)

    db.commit()
    db.refresh(client)
    return client


def get_client(db: Session, client_id: str) -> Client | None:
    """
    Retrieve client by client_id.
    """
    return db.query(Client).filter(Client.client_id == client_id).first()


def update_client_models(
    db: Session,
    client_id: str,
    embedding_model: str | None = None,
    llm_model: str | None = None
) -> Client:
    """
    Update embedding/LLM models for an existing client.
    Raises ValueError if client does not exist.
    """
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        raise ValueError(f"Client '{client_id}' not found")

    if embedding_model:
        client.embedding_model = embedding_model
    if llm_model:
        client.llm_model = llm_model

    db.commit()
    db.refresh(client)
    return client
