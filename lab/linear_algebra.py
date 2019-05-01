# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from . import dispatch, B
from .types import Numeric
from .util import abstract

__all__ = ['epsilon',
           'transpose', 'T',
           'matmul', 'mm', 'dot',
           'kron',
           'trace',
           'svd',
           'cholesky',
           'cholesky_solve',
           'trisolve',
           'outer',
           'reg']

epsilon = 1e-12  #: Magnitude of diagonal to regularise matrices with.


@dispatch(Numeric)
@abstract()
def transpose(a):  # pragma: no cover
    """Transpose a matrix.

    Args:
        a (tensor): Matrix to transpose.

    Returns:
        tensor: Transposition of `a`.
    """


T = transpose  #: Shorthand for `transpose`.


@dispatch(Numeric, Numeric)
@abstract()
def matmul(a, b, **kw_args):  # pragma: no cover
    """Matrix multiplication.

    Args:
        a (tensor): First matrix.
        b (tensor): Second matrix.
        tr_a (bool, optional): Transpose first matrix. Defaults to `False`.
        tr_b (bool, optional): Transpose second matrix. Defaults to `False`.

    Returns:
        tensor: Matrix product of `a` and `b`.
    """


mm = matmul  #: Shorthand for `matmul`.
dot = matmul  #: Also a shorthand for `matmul`.


@dispatch(Numeric)
@abstract()
def trace(a, **kw_args):  # pragma: no cover
    """Compute the trace of a tensor.

    Args:
        a (tensor): Tensor to compute trace of.
        axis1 (int, optional): First dimension to compute trace over. Defaults
            to `0`.
        axis2 (int, optional): Second dimension to compute trace over. Defaults
            to `1`.

    Returns:
        tensor: Trace.
    """


@dispatch(Numeric, Numeric)
@abstract()
def kron(a, b):  # pragma: no cover
    """Kronecker product.

    Args:
        a (tensor): First matrix.
        b (tensor): Second matrix.

    Returns:
        tensor: Kronecker product of `a` and `b`.
    """


@dispatch(Numeric)
@abstract()
def svd(a, **kw_args):  # pragma: no cover
    """Compute the singular value decomposition.

    Args:
        a (tensor): Matrix to decompose.
        compute_uv (bool, optional): Also compute `U` and `V`. Defaults to
            `True`.

    Returns:
        tuple: `(U, S, V)` is `compute_uv` is `True` and just `S` otherwise.
    """


@dispatch(Numeric)
@abstract()
def cholesky(a):  # pragma: no cover
    """Compute the Cholesky decomposition.

    Args:
        a (tensor): Matrix to decompose.

    Returns:
        tensor: Cholesky decomposition.
    """


@dispatch(Numeric, Numeric)
@abstract()
def cholesky_solve(a, b):  # pragma: no cover
    """Solve the linear system `a x = b` given the Cholesky factorisation of
    `a`.

    Args:
        a (tensor): Cholesky factorisation of `a`.
        b (tensor): RHS `b`.

    Returns:
        tensor: Solution `x`.
    """


@dispatch(Numeric, Numeric)
@abstract()
def trisolve(a, b, **kw_args):  # pragma: no cover
    """Solve the linear system `a x = b` where `a` is triangular.

    Args:
        a (tensor): Triangular matrix `a`.
        b (tensor): RHS `b`.
        lower_a (bool, optional): Indicate that `a` is lower triangular
            instead of upper triangular. Defaults to `True`.

    Returns:
        tensor: Solution `x`.
    """


@dispatch(Numeric, Numeric)
def outer(a, b):
    """Compute the outer product between two vectors.

    Args:
        a (vector): First vector.
        b (vector): Second vector.

    Returns:
        tensor: Outer product of `a` and `b`.
    """
    if B.rank(a) != 1 or B.rank(b) != 1:
        raise ValueError('Arguments must have rank 1.')
    return a[:, None] * b[None, :]


@dispatch(Numeric)
def outer(a):
    return outer(a, a)


def reg(a, diag=None, clip=True):
    """Add a diagonal to a matrix.

    Args:
        a (matrix): Matrix to add a diagonal to.
        diag (float, optional): Magnitude of the diagonal to add. Defaults to
            `.linear_algebra.epsilon`.
        clip (bool, optional): Let `diag` be at least `.linear_algebra.epsilon`.
            Defaults to `True`.

    Returns:
        matrix: Regularised version of `a`.
    """
    if diag is None:
        diag = epsilon
    elif clip:
        diag = B.maximum(diag, epsilon)
    return a + diag * B.eye(a)
