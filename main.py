from SandBox import SandBox
import pygame as pg


if __name__ == "__main__":
    pg.init()
    simulation = SandBox(cols=120, rows=100, w=5)
    simulation.run_simulation()
    pg.quit()
