from karel.KarelWorld import KarelWorld
from karel.Karel import Karel

from CollectNewspaperKarel import main


class TestKarel:
    @staticmethod
    def test_newspaper_karel():
        world = KarelWorld("CollectNewspaperKarel.w")
        karel = Karel(world)

        main()

        print(world)
