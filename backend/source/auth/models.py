from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True, description="Telegram User ID")

    user_name = fields.CharField(max_length=128, null=True)
    company_name = fields.CharField(max_length=256, null=True)
    company_info = fields.CharField(max_length=256, null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    is_admin = fields.BooleanField(default=False)

    class Meta:
        table = "users"
