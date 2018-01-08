def create_patching_kernel(size):
    ii, jj = np.meshgrid(np.arange(-(size//2),size//2+1), np.arange(-(size//2),size//2+1), indexing='ij')
    return np.array([xy for xy in zip(jj.ravel(), ii.ravel())])

def create_image_grid(image):
    ii, jj = np.meshgrid(np.arange(image.shape[0]), np.arange(image.shape[1]), indexing='ij')
    image_grid = []
    for i in np.arange(image.shape[0]):
        image_grid.append([ij for ij in zip(ii[i].ravel(), jj[i].ravel())])
    return np.array(image_grid)

def create_patch_grid(img1, img2, size, M):
    index, column = img1.shape[0], img2.shape[1]
    patch_grid_coords = create_patching_kernel(size)
    final_patch_grid = []
    
    for i in np.arange(index):
        patch_space = [row for row in np.arange(i-(size//2),i+(size//2+1)) if row >= 0 and row <= index-1]
        patched_pixel_row = []
        for j in np.arange(column):
            patch_coords = np.array([np.array([i,j])+ij for ij in patch_grid_coords])
            patch_coords_adj = patch_coords[((patch_coords >= 0).all(axis=1))                                             & ((patch_coords < [index,column]).all(axis=1))]
            patched_pixel_row.append(patch_coords_adj)
        final_patch_grid.append(patched_pixel_row)
        
    return np.array(final_patch_grid)
            
