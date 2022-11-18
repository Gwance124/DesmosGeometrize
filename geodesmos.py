import sys
from cli_parameters import get_cli_parameters
from frame_handler import create_frames
from config_handler import config_setup
from desmos_polygon_server import load_desmos_polygons
import subprocess
import time

def main(argv):
    # sets cli parameters as variables
    input, resolution, alpha, iterations, shapesPerStep, mutationsPerStep = get_cli_parameters(argv)

    # creates frames
    frames_dir = create_frames(input, resolution)[:-1]

    # sets up config settings
    config_setup(frames_dir, alpha, iterations, shapesPerStep, mutationsPerStep)

    # runs geometrize algorithm on frames
    start = time.time()
    print('Geometrize Processing ', end="\r", flush=True)
    subprocess.call(["geometrize", "--config", "config.json"])
    print(f'Geometrize Completed in {round(time.time() - start, 2)} seconds')

    # desmos polygon server
    load_desmos_polygons(f'{frames_dir}/jsons')


if __name__ == "__main__":
    main(sys.argv[1:])
