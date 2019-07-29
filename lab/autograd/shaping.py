# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import autograd.numpy as anp

from . import dispatch, B
from ..shaping import _vec_to_tril_shape_upper_perm
from ..types import AGNumeric, Int

__all__ = []


@dispatch(AGNumeric)
def length(a):
    return anp.size(a)


@dispatch(AGNumeric)
def expand_dims(a, axis=0):
    return anp.expand_dims(a, axis=axis)


@dispatch(AGNumeric)
def squeeze(a):
    return anp.squeeze(a)


@dispatch(AGNumeric)
def diag(a):
    return anp.diag(a)


@dispatch(AGNumeric)
def vec_to_tril(a):
    if B.rank(a) != 1:
        raise ValueError('Input must be rank 1.')
    m, upper, perm = _vec_to_tril_shape_upper_perm(a)
    a = anp.concatenate((a, anp.zeros(upper, dtype=a.dtype)))
    return anp.reshape(a[perm], (m, m))


@dispatch(AGNumeric)
def tril_to_vec(a):
    if B.rank(a) != 2:
        raise ValueError('Input must be rank 2.')
    n, m = B.shape(a)
    if n != m:
        raise ValueError('Input must be square.')
    return a[anp.tril_indices(n)]


@dispatch([AGNumeric])
def stack(*elements, **kw_args):
    return anp.stack(elements, axis=kw_args.get('axis', 0))


@dispatch(AGNumeric)
def unstack(a, axis=0):
    out = anp.split(a, anp.arange(1, a.shape[axis]), axis)
    return [x.squeeze(axis=axis) for x in out]


@dispatch(AGNumeric, [Int])
def reshape(a, *shape):
    return anp.reshape(a, shape)


@dispatch([AGNumeric])
def concat(*elements, **kw_args):
    return anp.concatenate(elements, axis=kw_args.get('axis', 0))


@dispatch(AGNumeric, [Int])
def tile(a, *repeats):
    return anp.tile(a, repeats)


@dispatch(AGNumeric, object)
def take(a, indices_or_mask, axis=0):
    if B.rank(indices_or_mask) != 1:
        raise ValueError('Indices or mask must be rank 1.')

    # Put axis `axis` first.
    if axis > 0:
        # Create a permutation to switch `axis` and `0`.
        perm = list(range(B.rank(a)))
        perm[0], perm[axis] = perm[axis], perm[0]
        a = anp.transpose(a, perm)

    # Take the relevant part.
    a = a[indices_or_mask, ...]

    # Put axis `axis` back again.
    if axis > 0:
        a = anp.transpose(a, perm)

    return a
