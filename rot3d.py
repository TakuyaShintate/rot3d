class Image3D:

    def __init__(self, tensor, dims):
        if len(dims) != 3:
            raise ValueError('dims must have format (x dim, y dim, z dim)')
        x, y, z = dims
        if x >= tensor.dims() or x < -tensor.dims():
            raise ValueError('x dim out of range')
        if y >= tensor.dims() or y < -tensor.dims():
            raise ValueError('y dim out of range')
        if z >= tensor.dims() or z < -tensor.dims():
            raise ValueError('z dim out of range')
        self.tensor = tensor
        self.dims = dims

    def get(self):
        return self.tensor

    def inv(self):
        self.tensor = self.tensor.flip(self.dims)
        return self

    def mirror(self, axis):
        x, y, z = self.dims
        axes1 = {
            'x': x,
            'y': y,
            'z': z,
        }
        axes2 = {
            ('x', 'y'): (True, x, y),
            ('x', '-y'): (False, x, y),
            ('x', 'z'): (True, x, z),
            ('x', '-z'): (False, x, z),
            ('y', 'z'): (True, y, z),
            ('y', '-z'): (False, y, z),
        }
        if axis in axes1:
            self.tensor = self.tensor.flip(to_dim[by])
        elif axis in axes2:
            rot, dim1, dim2 = axes2[axis]
            if rot:
                self.tensor = self.tensor.rot90(k=1, dims=(dim1, dim2))
            self.tensor = self.tensor.transpose(dim1, dim2)
            if rot:
                self.tensor = self.tensor.rot90(k=1, dims=(dim2, dim1))
        else:
            raise ValueError('Unexpected axis')
        return self

    def rot90(self, axis):
        """Rotate 90 degree anticlockwise along given axis"""
        x, y, z = self.dims
        axes = {
            'x': (y, z),
            'y': (z, x),
            'z': (x, y),
            '-x': (z, y),
            '-y': (x, z),
            '-z': (y, x),
        }
        if axis not in axes:
            raise ValueError('Unexpected axis')
        self.tensor = self.tensor.rot90(k=1, dims=axes[axis])
        return self

    def rot120(self, axis):
        return self.rot60_mirror(axis).rot60_mirror(axis)

    def rot180(self, axis):
        x, y, z = self.dims
        axes1 = {
            'x': (y, z),
            'y': (z, x),
            'z': (x, y),
        }
        axes2 = {
            ('x', 'y'): (z, ('x', '-y')),
            ('x', '-y'): (z, ('x', 'y')),
            ('x', 'z'): (y, ('x', '-z')),
            ('x', '-z'): (y, ('x', 'z')),
            ('y', 'z'): (x, ('y', '-z')),
            ('y', '-z'): (x, ('y', 'z')),
        }
        if axis in axes1:
            self.tensor = self.tensor.rot90(k=1, axes[axis])
            return self
        elif axis in axes2:
            flip_axis, mirror_axis = axes2[axis]
            self.tensor = self.tensor.flip(flip_axis)
            return self.mirror(mirror_axis)
        raise ValueError('Unexpected axis')

    def rot90_mirror(self, axis):
        return self.rot90(axis).mirror(axis[-1:])

    def rot60_mirror(self, axis):
        pass
