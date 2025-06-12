from typing import Protocol, Generic, TypeVar, Optional, List, Dict, Any

T = TypeVar("T")
ID = TypeVar("ID")

class IRepository(Protocol, Generic[T, ID]):
    async def get(self, id: ID) -> Optional[T]:
        ...

    async def list(self, filters: Dict[str, Any] = None) -> List[T]:
        ...

    async def add(self, entity: T) -> T:
        ...

    async def update(self, entity: T) -> None:
        ...

    async def delete(self, id: ID) -> None:
        ...
