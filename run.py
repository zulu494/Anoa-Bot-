from yowsup.stacks import YowStackBuilder
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from layer import MainLayer

if __name__ == "__main__":
    try:
        stackBuilder = YowStackBuilder()
        stack = stackBuilder\
            .pushDefaultLayers()\
            .push(MainLayer)\
            .build()

        stack.setCredentials(("", None))
        stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        stack.loop()
    except KeyboardInterrupt:
        print("\Application exit.")
        exit(0)
