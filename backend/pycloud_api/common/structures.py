# -*- coding: utf-8 -*-
class Struct(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    async def dict(self):
        return await self.dump()

    async def dump(self):
        dump_object = vars(self)

        async def assign_to_index(k, i, v):
            k[i] = v
            return v

        async def reassign(k, v):
            dump_object[k] = await v.dump()

        # TODO: This is overly complicated. Attempt to simplify in the future.
        _ = [
            await reassign(k, v)
            for k, v in dump_object.items()
            if isinstance(v, Struct)
        ]
        _ = [
            await assign_to_index(v, x, await y.dump())
            for k, v in dump_object.items()
            if isinstance(v, list)
            for x, y in enumerate(v)
            if isinstance(y, Struct)
        ]
        return dump_object

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError(f"{self.__class__}, object has no attribute {name}")

    def __repr__(self):
        return (
            f"<object {self.__class__.__name__}"
            f"({', '.join('{k}={v}'.format(k=k, v=self.__dict__[k]) for k in sorted(self.__dict__.keys()))})>"
        )
