from abc import ABC
from abc import abstractmethod


class BaseUseCase(ABC):
    @abstractmethod
    async def execute(self, *args, **kwargs):
        pass
