from tortoise.models import Model
from tortoise import fields

class Chat(Model):
    id = fields.IntField(pk=True)
    type = fields.IntField()  # 0-5
    user = fields.ForeignKeyField("models.User", related_name="chats")
    
    class Meta:
        table = "chats"

class Message(Model):
    id = fields.IntField(pk=True)
    chat = fields.ForeignKeyField("models.Chat", related_name="messages")
    text = fields.TextField()
    is_user = fields.IntField()  # 0 - модель, 1 - пользователь
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "messages"

