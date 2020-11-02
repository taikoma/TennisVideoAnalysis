import TennisCourtNet
import torch


net = TennisCourtNet.TennisCourtNet()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
net_weights = torch.load(filepath,map_location=device)
keys = list(net_weights.keys())
print('keys:',keys)
weights_load = {}

for i in range(len(keys)):
    weights_load[list(net.state_dict().keys())[i]
                ] = net_weights[list(keys)[i]]



state = net.state_dict()
state.update(weights_load)
net.load_state_dict(state)

# pytorch_model.train(False)

temp_input = torch.autograd.Variable(torch.randn(input_shape), requires_grad=True)

torch.onnx._export(net, temp_input, output_onnx_model_path, export_params=True, output_names=["output"])