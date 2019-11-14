import argparse
import nbt


def delete_biome_data(world_path, from_x, from_z, to_x, to_z):
    if from_x >= to_x or from_z >= to_z:
        raise Exception("Invalid range.")

    world = nbt.world.AnvilWorldFolder(world_path)

    for x in range(from_x, to_x + 1):
        for z in range(from_z, to_z + 1):
            rx, cx = divmod(x, 32)
            rz, cz = divmod(z, 32)

            if (rx, rz) not in world.regions and (rx, rz) not in world.regionfiles:
                continue

            region = world.get_region(rx, rz)

            try:
                chunk = region.get_nbt(cx, cz)
            except nbt.region.InconceivedChunk:
                continue

            if "Biomes" not in chunk["Level"]:
                continue

            print(f"deleting biome data at {x},{z}")

            del chunk["Level"]["Biomes"]

            region.write_chunk(cx, cz, chunk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Delete biome data for a range of chunks in a world"
    )
    parser.add_argument("world_path", type=str, help="path to the world directory")
    parser.add_argument("from_x", type=int, help="from X chunk coordinate")
    parser.add_argument("from_z", type=int, help="from Z chunk coordinate")
    parser.add_argument("to_x", type=int, help="to X chunk coordinate")
    parser.add_argument("to_z", type=int, help="to Z chunk coordinate")

    args = parser.parse_args()

    delete_biome_data(args.world_path, args.from_x, args.from_z, args.to_x, args.to_z)
