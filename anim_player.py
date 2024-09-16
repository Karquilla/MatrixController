from utils import *

#from digitalio import DigitalInOut, Pull
#from adafruit_matrixportal.matrix import Matrix
#from adafruit_debouncer import Debouncer

SPRITESHEET_FOLDER = "/bmps"
DEFAULT_FRAME_DURATION = 0.1  # 100ms
AUTO_ADVANCE_LOOPS = 3
FRAME_DURATION_OVERRIDES = {
}

auto_advance = False
# --- Display setup ---
class AnimPlayer:
    def __init__(self,matrix):
        
        self.matrix = matrix
        self.sprite_group = displayio.Group()
        self.setup_ = False
        
        self.current_image = None
        self.current_frame = 0
        self.current_loop = 0
        self.frame_count = 0
        self.totalLoops = 0
        self.frame_duration = DEFAULT_FRAME_DURATION

    def setup(self,totalLoops = 1):
        if not self.setup_:
            self.matrix.display.root_group = self.sprite_group
            self.setup_ = True
        if self.totalLoops != totalLoops:
            self.totalLoops = totalLoops

    def load_image(self):
        """
        Load an image as a sprite
        """
        # pylint: disable=global-statement
        while self.sprite_group:
            self.sprite_group.pop()

        bitmap = displayio.OnDiskBitmap(
            open(self.current_image,"rb")
        )
        
        self.frame_count = int(bitmap.height / self.matrix.display.height)
        self.frame_duration = DEFAULT_FRAME_DURATION
        if self.current_image in FRAME_DURATION_OVERRIDES:
            self.frame_duration = FRAME_DURATION_OVERRIDES[self.current_image]

        self.sprite = displayio.TileGrid(
            bitmap,
            pixel_shader=displayio.ColorConverter(),
            width=1,
            height=1,
            tile_width=bitmap.width,
            tile_height=self.matrix.display.height,
        )

        self.sprite_group.append(self.sprite)
        self.current_frame = 0
        self.current_loop = 0


    def change_anim(self,name):
        """
        Advance to the next image in the list and loop back at the end
        """
        
        self.current_image = prompt.anims.get(name)

        # pylint: disable=global-statement
        #if self.current_image is not None:
        #    self.current_image += 1
        #if self.current_image is None or self.current_image >= len(file_list):
        #    self.current_image = 0
        self.load_image()


    def advance_frame(self):
        """
        Advance to the next frame and loop back at the end
        """
        # pylint: disable=global-statement
        self.current_frame = self.current_frame + 1
        print(self.current_frame)
        if self.current_frame >= self.frame_count:
            self.current_frame = 0
            self.current_loop = self.current_loop + 1
        self.sprite[0] = self.current_frame

    def run(self,anim, loops):
        self.setup(totalLoops = loops)
        if self.current_image == None or self.current_image != anim:
            self.change_anim(anim)
            print ("ani changef")

        while self.current_loop < self.totalLoops:
            if (auto_advance and self.current_loop >= AUTO_ADVANCE_LOOPS) and self.current_image != self.current_image:
                self.change_anim(anim)
            self.advance_frame()

            time.sleep(self.frame_duration)