from PIL import Image
import json, math

class Agent():
    def __init__(self, name):
        self.frames = Image.open("resources/%s/map.png" % name)
        t_width, t_height = self.frames.size
        self.total_height = t_height

        with open("resources/%s/agent.json" % name, 'r') as handle:
            data = json.load(handle)
            self.frame_width = data['framesize'][0]
            self.frame_height = data['framesize'][1]

            self.frame_x_count = math.floor(t_width / self.frame_width)
            self.frame_y_count = math.floor(t_height / self.frame_height)
            self.animations = data['animations']

    def get_frame(self, x1, y1):
        x2 = x1 + self.frame_width
        y2 = y1 + self.frame_height

        return self.frames.crop((x1, y1, x2, y2))

    def get_animation(self, name):
        return self.animations[name]