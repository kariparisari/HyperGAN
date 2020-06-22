import torch.nn as nn

class Add(nn.Module):
    def __init__(self, layers, layer_names):
        super(Add, self).__init__()
        self.layers = layers
        self.layer_names = layer_names
        for i, (layer, layer_name) in enumerate(zip(self.layers, self.layer_names)):
            self.add_module('layer_'+str(i)+"_"+layer_name, layer)

    def forward(self, net, context):
        output = None
        for layer, layer_name in zip(self.layers, self.layer_names):
            if layer_name == "modulated_conv2d":
                layer_output = layer(net, context['w'])
            elif layer_name == "self":
                layer_output = net
            else:
                layer_output = layer(net)
            if output is None:
                output = layer_output
            else:
                output = output + layer_output
        return output
