import sqlalchemy as sa
from database import metadata

clientes = sa.Table(
    "clientes", metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("nome", sa.String(100), nullable=False),
    sa.Column("cpf", sa.String(11), nullable=False, unique=True),
    sa.Column("data_nascimento", sa.String(10), nullable=False),
    sa.Column("endereco", sa.String(80), nullable=False),
)