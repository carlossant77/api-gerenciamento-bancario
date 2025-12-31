import sqlalchemy as sa
from database import metadata

transacoes = sa.Table(
    "transacoes", metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("tipo", sa.String(100), nullable=False),
    sa.Column("valor", sa.Numeric(12, 2), nullable=False),
    sa.Column("hora", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()),
    sa.Column("conta", sa.Integer, sa.ForeignKey("contas.id"), nullable=False),
)