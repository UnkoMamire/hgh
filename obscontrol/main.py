#!/usr/bin/env python3

import pyslobs as slobs
import asyncio


async def set_sceneitem_size(conn, scene_id, item_id, width, height):
    ss = slobs.ScenesService(conn)
    scene = await ss.get_scene(scene_id)
    item = await scene.get_item(item_id)
    source = await item.get_source()
    if source.width != 0 and source.height !=0:
        x_scale = float(width) / float(source.width)
        y_scale = float(height) / float(source.height)
        await item.set_scale(slobs.IVec2(x_scale, y_scale))
    await conn.close()


async def set_sceneitem_position(conn, scene_id, item_id, x_pos, y_pos):
    ss = slobs.ScenesService(conn)
    scene = await ss.get_scene(scene_id)
    item = await scene.get_item(item_id)

    old_transform = item.transform
    new_transform = slobs.ITransform(
            crop=old_transform.crop,
            scale=old_transform.scale,
            position=slobs.IVec2(
                x=x_pos,
                y=y_pos,
                ),
            rotation=old_transform.rotation,
            )

    await item.set_transform(new_transform)
    await conn.close()


async def stadio_mode(conn: slobs.SlobsConnection):
    ts = slobs.TransitionsService(conn)
    await ts.enable_studio_mode()
    await conn.close()


async def transiton(conn: slobs.SlobsConnection):
    ts = slobs.TransitionsService(conn)
    await ts.execute_studio_mode_transition()
    await conn.close()


async def make_active(conn: slobs.SlobsConnection, scene_id: str):
    ss = slobs.ScenesService(conn)
    await ss.make_scene_active(scene_id)
    await conn.close()


async def get_settings(conn: slobs.SlobsConnection, source_id: str):
    ss = slobs.SourcesService(conn)
    source = await ss.get_source(source_id)
    settings = await source.get_settings()
    print(settings)
    await conn.close()


async def change_source_file(conn: slobs.SlobsConnection, source_id: str, filename: str):
    ss = slobs.SourcesService(conn)
    source = await ss.get_source(source_id)
    await source.update_settings({'file': filename})
    await conn.close()


async def change_source_input(conn: slobs.SlobsConnection, source_id: str, inputname: str):
    ss = slobs.SourcesService(conn)
    source = await ss.get_source(source_id)
    await source.update_settings({'input': inputname})
    await conn.close()


async def print_settings(conn: slobs.SlobsConnection, source_id: str):
    ss = slobs.SourcesService(conn)
    source = await ss.get_source(source_id)
    settings = await source.get_settings()
    print(settings)
    await conn.close()


class ObsControl:

    def set_sceneitem_size(self, scene_id, item_id, width, height):
        conn = slobs.SlobsConnection(slobs.config_from_ini())
        async def main():
            await asyncio.gather(conn.background_processing(),
                    set_sceneitem_size(conn, scene_id, item_id, width, height))
        asyncio.run(main())

    def set_sceneitem_position(self, scene_id, item_id, x_pos, y_pos):
        conn = slobs.SlobsConnection(slobs.config_from_ini())
        async def main():
            await asyncio.gather(conn.background_processing(),
                    set_sceneitem_position(conn, scene_id, item_id, x_pos, y_pos))
        asyncio.run(main())

    def stadio_mode(self):
        conn = slobs.SlobsConnection(slobs.config_from_ini())
        async def main():
            await asyncio.gather(conn.background_processing(), stadio_mode(conn))
        asyncio.run(main())

    def transition(self):
        conn = slobs.SlobsConnection(slobs.config_from_ini())
        async def main():
            await asyncio.gather(conn.background_processing(), transiton(conn))
        asyncio.run(main())

    def make_active(self, scene_id: str):
        conn = slobs.SlobsConnection(slobs.config_from_ini())
        async def main():
            await asyncio.gather(conn.background_processing(), make_active(conn, scene_id))
        asyncio.run(main())

    def change_source_file(self, source_id: str, filename: str):
        conn = slobs.SlobsConnection(slobs.config_from_ini())
        async def main():
            await asyncio.gather(conn.background_processing(), change_source_file(conn, source_id, filename))
        asyncio.run(main())

    def change_source_input(self, source_id: str, inputname: str):
        conn = slobs.SlobsConnection(slobs.config_from_ini())
        async def main():
            await asyncio.gather(conn.background_processing(), change_source_input(conn, source_id, inputname))
        asyncio.run(main())

    def print_settings(self, source_id: str):
        conn = slobs.SlobsConnection(slobs.config_from_ini())
        async def main():
            await asyncio.gather(conn.background_processing(), print_settings(conn, source_id))
        asyncio.run(main())
