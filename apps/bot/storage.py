from typing import Any, Dict, Optional
from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType
from asgiref.sync import sync_to_async
from apps.models import BotState

class DjangoStorage(BaseStorage):
    """
    Storage adapter for Aiogram 3.x using Django ORM.
    Persists user state and data to the BotState model.
    """
    
    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        await sync_to_async(self._set_state_sync)(key, state)

    def _set_state_sync(self, key: StorageKey, state: StateType):
        obj, _ = BotState.objects.get_or_create(user_id=key.user_id, chat_id=key.chat_id)
        obj.state = state.state if state else None
        obj.save()

    async def get_state(self, key: StorageKey) -> Optional[str]:
        return await sync_to_async(self._get_state_sync)(key)

    def _get_state_sync(self, key: StorageKey) -> Optional[str]:
        try:
            obj = BotState.objects.get(user_id=key.user_id, chat_id=key.chat_id)
            return obj.state
        except BotState.DoesNotExist:
            return None

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        await sync_to_async(self._set_data_sync)(key, data)

    def _set_data_sync(self, key: StorageKey, data: Dict[str, Any]):
        obj, _ = BotState.objects.get_or_create(user_id=key.user_id, chat_id=key.chat_id)
        obj.data = data
        obj.save()

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        return await sync_to_async(self._get_data_sync)(key)

    def _get_data_sync(self, key: StorageKey) -> Dict[str, Any]:
        try:
            obj = BotState.objects.get(user_id=key.user_id, chat_id=key.chat_id)
            return obj.data if obj.data else {}
        except BotState.DoesNotExist:
            return {}

    async def close(self) -> None:
        pass
