from tortoise.models import Model
from tortoise import fields
from datetime import datetime

class User(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True, description="Telegram User ID")
    name = fields.CharField(max_length=100, null=True)
    surname = fields.CharField(max_length=100, null=True)
    company_name = fields.CharField(max_length=200, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    is_admin = fields.BooleanField(default=False)
    
    class Meta:
        table = "users"

