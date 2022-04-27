import torch

from . import B, dispatch
from ..types import TorchNumeric, TorchDType, Int, TorchRandomState

__all__ = []


@dispatch
def create_random_state(_: TorchDType, seed: Int = 0):
    state = torch.Generator(device=B.ActiveDevice.active_name)
    state.manual_seed(seed)
    return state


@dispatch
def global_random_state(_: TorchDType):
    if B.ActiveDevice.active_name in {None, "cpu"}:
        return torch.random.default_generator
    else:
        parts = B.ActiveDevice.active_name.lower().split(":")

        if len(parts) == 0 or parts[0] not in {"cuda", "gpu"}:
            raise RuntimeError(f'Unknown active device "{B.ActiveDevice.active_name}".')

        # Ensure that the generators are available.
        if len(torch.cuda.default_generators) == 0:
            torch.cuda.init()

        if len(parts) == 1:
            return torch.cuda.default_generators[0]
        else:
            return torch.cuda.default_generators[int(parts[1])]


@dispatch
def set_global_random_state(state: TorchRandomState):
    global_gen = global_random_state.invoke(TorchDType)(None)
    global_gen.set_state(state.get_state())


@dispatch
def rand(state: TorchRandomState, dtype: TorchDType, *shape: Int):
    return state, torch.rand(
        shape,
        dtype=dtype,
        device=B.ActiveDevice.active_name,
        generator=state,
    )


@dispatch
def rand(dtype: TorchDType, *shape: Int):
    return rand(global_random_state(dtype), dtype, *shape)[1]


@dispatch
def randn(state: TorchRandomState, dtype: TorchDType, *shape: Int):
    return state, torch.randn(
        shape,
        dtype=dtype,
        device=B.ActiveDevice.active_name,
        generator=state,
    )


@dispatch
def randn(dtype: TorchDType, *shape: Int):
    return randn(global_random_state(dtype), dtype, *shape)[1]


@dispatch
def choice(state: TorchRandomState, a: TorchNumeric, n: Int):
    choices = a[torch.randint(a.shape[0], (n,), generator=state)]
    return state, choices[0] if n == 1 else choices


@dispatch
def choice(a: TorchNumeric, n: Int):
    return choice(global_random_state(a), a, n)[1]


@dispatch
def randint(
    state: TorchRandomState, dtype: TorchDType, *shape: Int, lower: Int = 0, upper: Int
):
    dtype = B.dtype_int(dtype)
    return state, torch.randint(
        lower,
        upper,
        shape,
        dtype=dtype,
        device=B.ActiveDevice.active_name,
        generator=state,
    )


@dispatch
def randint(dtype: TorchDType, *shape: Int, lower: Int = 0, upper):
    state = global_random_state(dtype)
    return randint(state, dtype, *shape, lower=lower, upper=upper)[1]


@dispatch
def randperm(state: TorchRandomState, dtype: TorchDType, n: Int):
    dtype = B.dtype_int(dtype)
    return state, torch.randperm(
        n,
        dtype=dtype,
        device=B.ActiveDevice.active_name,
        generator=state,
    )


@dispatch
def randperm(dtype: TorchDType, n: Int):
    return randperm(global_random_state(dtype), dtype, n)[1]
