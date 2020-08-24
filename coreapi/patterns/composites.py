
import asyncio
from typing import List


class Component:

    def __init__(self, *args, **kwargs):
        self._parent = str()
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def add(self, component) -> None:
        raise NotImplementedError("Please Implement this method")

    def remove(self, component) -> None:
        raise NotImplementedError("Please Implement this method")

    def is_composite(self) -> bool:
        return False

    async def run(self):
        raise NotImplementedError("Please Implement this method")


class Leaf(Component):
    async def run(self):
        raise NotImplementedError("Please Implement this method")


class Composite(Component):
    def __init__(self, *args, **kwargs) -> None:
        super(Composite, self).__init__(*args, **kwargs)
        self._children: List[Component] = []

    def add(self, component: Component) -> None:
        self._children.append(self.loop.create_task(component.run()))
        component.parent = self

    def is_composite(self) -> bool:
        return True

    async def run(self) -> List[str]:
        await asyncio.wait(self._children)
        return [item.result() for item in self._children]
