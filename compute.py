"""
helper functions for computing input at different time t and scale n (i.e. z_n(t))
two dimensions involve:
- time, denoted by t
- scale, denoted by n

related formula refer to p.6 in:
http://openaccess.thecvf.com/content_ICCV_2019/supplemental/Shaham_SinGAN_Learning_a_ICCV_2019_supplemental.pdf
"""
import torch

import SinGAN.functions as functions
from SinGAN.imresize import imresize


def compute_z_curr(Z_opt, z_prev1, z_diff, alpha):
    """ compute z_n(t+1), t+1 means current """
    z_curr = alpha * Z_opt + (1 - alpha) * (z_prev1 + z_diff)
    return z_curr


def compute_z_prev(n, Z_opt, device):
    """
    compute z_n at previous time, i.e. z_n(t), z_n(t-1)

    :param:
        n -- int, indicate scale level (0 = first generator, i.e. coarest level)
        Z_opt -- input noise at the n-th scale (gaussian noise at first generator, elsewhere 0)
        device -- torch.device, CUDA / CPU
    """
    nzx, nzy = Z_opt.shape[2], Z_opt.shape[3]
    # no. of channel for noise input
    nc_z = 3 
    if n == 0:
        # z_rand is gaussian noise
        z_rand = functions.generate_noise([1, nzx, nzy], device= device) 
        z_rand = z_rand.expand(1, 3, Z_opt.shape[2], Z_opt.shape[3])
        z_prev1 = 0.95 * Z_opt +0.05 * z_rand
        z_prev2 = Z_opt
    else:
        z_prev1 = 0.95 * Z_opt +0.05 * functions.generate_noise([nc_z, nzx, nzy], device = device)
        z_prev2 = Z_opt
    return z_prev1, z_prev2


def compute_z_diff(n, Z_opt, z_prev1, z_prev2, beta, device):
    """ compute z_diff_n(t+1) """
    nzx, nzy = Z_opt.shape[2], Z_opt.shape[3]
    nc_z = 3
    if n == 0:
        z_rand = functions.generate_noise([1,nzx,nzy], device = device)
        # make z_rand same across channels
        z_rand = z_rand.expand(1,3, Z_opt.shape[2], Z_opt.shape[3])
        z_diff = beta * (z_prev1 - z_prev2) + (1 - beta) * z_rand
    else:
        z_diff = beta * (z_prev1 - z_prev2) + (1 - beta) * (functions.generate_noise([nc_z, nzx, nzy], device = device))
    return z_diff
