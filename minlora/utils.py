from minlora import LoRAParametrization
from torch import nn


def apply_to_lora(fn):
    """
        apply a function to LoRAParametrization layers
        designed to be used with model.apply
    """

    def apply_fn(layer):
        if isinstance(layer, LoRAParametrization):
            fn(layer)

    return apply_fn

def enable_lora(model):
    return model.apply(apply_to_lora(lambda x: x.enable_lora()))

def disable_lora(model):
    return model.apply(apply_to_lora(lambda x: x.disable_lora()))


#                     ------------------- 
# helper function for collecting parameters for training/saving 
#                     -------------------


def name_is_lora(name):
    return (
        len(name.split(".")) >= 4
        and (name.split(".")[-4]) == "parametrizations"
        and name.split(".")[-1] in ["lora_A", "lora_B"]
    )


def name_is_bias(name):
    return name.split(".")[-1] == "bias"


def get_params_by_name(model,
                       print_shapes=False,
                       name_filter=None):
    for n, p in model.named_parameters():
        if name_filter is None or name_filter(n):
            if print_shapes:
                print(n, p.shape)
            yield p


def get_lora_params(model,
                    print_shapes=False):
    return get_params_by_name(model,
                              print_shapes=print_shapes,
                              name_filter=name_is_lora)


def get_bias_params(model,
                    print_shapes=False):
    return get_params_by_name(model,
                              print_shapes=print_shapes,
                              name_filter=name_is_bias)


def get_lora_state_dict(model):
    return {k: v for k, v in model.state_dict().items() if name_is_lora(k)}


#              ------------------- 
# helper function for inferencing with multiple lora
#              -------------------


def _prepare_for_multiple_lora(lora_layer):
    lora_layer.lora_As = []
    lora_layer.lora_Bs = []


def _append_lora(lora_layer):
    lora_layer.lora_As.append(nn.Parameter(lora_layer.lora_A.clone()))
    lora_layer.lora_Bs.append(nn.Parameter(lora_layer.lora_B.clone()))


def load_multiple_lora(model,
                       lora_state_dicts):
    model.apply(apply_to_lora(_prepare_for_multiple_lora))
    for state_dict in lora_state_dicts:
        _ = model.load_state_dict(state_dict, strict=False)
        model.apply(apply_to_lora(_append_lora))
    return model


def _select_lora(lora_layer,
                 index):
    lora_layer.lora_A = lora_layer.lora_As[index]
    lora_layer.lora_B = lora_layer.lora_Bs[index]


def select_lora(model,
                index):
    model.apply(apply_to_lora(lambda x: _select_lora(x, index)))
    return model


#            ------------------- 
# helper function for tying and untieing weights
#            -------------------


def tie_weights(linear: nn.Linear,
                embedding: nn.Embedding):
    """
        w = weights of the linear layer
        e = weights of the embedding layer
        tie w and e with same lora
    """
    # this line below is optional if the original is already tied
    linear_weight_orig = linear.parametrizations.weight.original
    linear_lora_B = linear.parametrizations.weight[0].lora_B
    linear_lora_A = linear.parametrizations.weight[0].lora_A
    embedding.parametrizations.weight.original = linear_weight_orig
    embedding.parametrizations.weight[0].lora_A = linear_lora_B
    embedding.parametrizations.weight[0].lora_B = linear_lora_A


def untie_weights(linear: nn.Linear,
                  embedding: nn.Embedding):
    """
        untie the weights of the linear layer and the embedding layer
    """
    embedding_orig = nn.Parameter(embedding.weight.original.clone())
    lora_A_clone = embedding.parametrizations.weight[0].lora_A.clone()
    embedding_lora_A = nn.Parameter(lora_A_clone)
    lora_B_clone = embedding.parametrizations.weight[0].lora_B.clone()
    embedding_lora_B = nn.Parameter(lora_B_clone)
    embedding.parametrizations.weight.original = embedding_orig
    embedding.parametrizations.weight[0].lora_A = embedding_lora_A
    embedding.parametrizations.weight[0].lora_B = embedding_lora_B
