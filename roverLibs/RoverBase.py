import serial
import time

class RoverBase():

    def __init__(self):

        print("Initializing")
        self.uno = serial.Serial("/dev/ttyACM0", 115200, timeout=5)
        print("Awaiting serial communication bootup...")
        time.sleep(5)
        print("Serial communication established")

    def move(self, key):
        if key == "up":
            self.uno.write(b'w')
            print("Up pressed")

        elif key == 'down':
            self.uno.write(b's')
            print("Down pressed")

        elif key == 'left':
            self.uno.write(b'd')
            print("Left pressed")

        elif key == 'right':
            self.uno.write(b'a')
            print("Right pressed")

        elif key == 'shift':
            print("Shift key pressed")
            self.reset()

        else:
            self.uno.write(b"")

        self.uno.reset_input_buffer
        self.uno.reset_output_buffer

    def reset(self):
        self.uno.close()
        print("closing connection...")
        time.sleep(1)
        print("...")
        time.sleep(1)
        print("connection closed")
        print("restarting")
        self.__init__()

    def main(self):
        #with Listener(on_press=self.move) as l:
        #    l.join()
        pass


if __name__ == "__main__":
    gari = Gari()
    #gari.main()
