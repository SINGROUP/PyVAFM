# Python function to apply Gaussian smearing to data on a regular 3D grid
# Written by M. J. Wolf, Department of Chemistry, Uppsala University
# Finished on 26th Feb 2015

# real_dir2cart is a 3x3 matrix, the columns of which are the real space lattice vectors
# grid_dim is a 1x3 matrix, the entries of which are the numbers of grid points along each lattice vector
# real_grid_data is the data on the real space grid (3d Vector)
# sigma is the standard deviation of the Gaussian function in real space

import numpy as np


def gauss(real_dir2cart, grid_dim, real_grid_data, sigma):

    cent_point_grid = (np.floor(np.multiply(
        np.array([0.5, 0.5, 0.5]), grid_dim))).astype(int)

    dk = np.linalg.inv(real_dir2cart).T

    shift_filt_matrix = np.zeros(grid_dim)

    i = np.subtract(np.array(list(range(0, grid_dim[0]))), cent_point_grid[0])
    j = np.subtract(np.array(list(range(0, grid_dim[1]))), cent_point_grid[1])
    k = np.subtract(np.array(list(range(0, grid_dim[2]))), cent_point_grid[2])

    # NOTE STUPID ORDERING OF 3D MESHGRID OUTPUT !
    jj, ii, kk = np.meshgrid(i, j, k)

    xx = np.multiply(ii, dk[0, 0]) + np.multiply(jj,
                                                 dk[0, 1]) + np.multiply(kk, dk[0, 2])
    yy = np.multiply(ii, dk[1, 0]) + np.multiply(jj,
                                                 dk[1, 1]) + np.multiply(kk, dk[1, 2])
    zz = np.multiply(ii, dk[2, 0]) + np.multiply(jj,
                                                 dk[2, 1]) + np.multiply(kk, dk[2, 2])

    arg = np.multiply(np.multiply(xx, xx) + np.multiply(yy, yy) +
                      np.multiply(zz, zz), -2*np.pi**2*sigma**2)
    shift_filt_matrix = np.exp(arg)

    filt_matrix = np.fft.ifftshift(shift_filt_matrix)

    recip_grid_data = np.fft.fftn(real_grid_data)

    new_real_grid_data = np.fft.ifftn(
        np.multiply(recip_grid_data, filt_matrix))

    new_real_grid_data = np.multiply(
        np.sign(np.real(new_real_grid_data)), np.abs(new_real_grid_data))

    return new_real_grid_data
