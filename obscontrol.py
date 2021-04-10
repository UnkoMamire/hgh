#!/usr/bin/env python3

import pyslobs as slobs
import asyncio


async def set_sceneitem_scale(conn, scene_id, item_id, width, height):
    ss = slobs.ScenesService(conn)
    scene = await ss.get_scene(scene_id)
    item = await scene.get_item(item_id)
    print(item.name)
    await item.set_scale(slobs.IVec2(width, height))
    await conn.close()

class ObsContorol:

    def set_sceneitem_scale(self, scene_id, item_id, width, height):
        conn = slobs.SlobsConnection(slobs.config_from_ini())
        async def main():
            await asyncio.gather(conn.background_processing(),
                    set_sceneitem_scale(conn, scene_id, item_id, width, height))
        asyncio.run(main())

