import sqlalchemy as sa
from database import metadata

contas = sa.Table(
    "contas", metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("saldo", sa.Numeric(12, 2), default=0),
    sa.Column("cliente_id", sa.Integer, sa.ForeignKey("clientes.id"), nullable=False, unique=True)
)