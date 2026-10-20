
import numpy as np
import trimesh


def export_negative_mold(
    x,
    y,
    z,
    filename="negative_mold.stl",
    wall_height=15.0,
    cavity_depth=5.0,
    base_thickness=5.0,
    rim_width=5.0,
    depth_scale=1.0,
):
    """
    Create an open-top, square mold box with:
      - raised perimeter walls
      - a hollow cavity
      - a textured negative floor
      - a flat solid bottom

    All dimensions use the same units as x and y.
    """

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    z = np.asarray(z, dtype=float)

    if not (x.shape == y.shape == z.shape):
        raise ValueError("x, y, z must have identical shapes.")

    if not np.isfinite(z).all():
        raise ValueError("z contains non-finite values.")

    if wall_height <= 0 or base_thickness <= 0:
        raise ValueError("Wall height and base thickness must be positive.")

    if cavity_depth <= 0 or depth_scale <= 0 or rim_width <= 0:
        raise ValueError("Cavity depth, depth scale, and rim width must be positive.")

    n_rows, n_cols = z.shape

    dx = float(np.median(np.diff(x[0, :])))
    dy = float(np.median(np.diff(y[:, 0])))

    if dx <= 0 or dy <= 0:
        raise ValueError("Grid spacing must be positive.")

    # Normalize the texture to a depth profile.
    # Original peaks become deep points in the negative mold.
    z_range = z.max() - z.min()

    if z_range == 0:
        depth = np.zeros_like(z)
    else:
        depth = (z.max() - z) * depth_scale

    # Keep the floor above the bottom and below the top rim.
    floor_z = base_thickness + depth

    if floor_z.max() >= wall_height:
        raise ValueError(
            "wall_height must exceed base_thickness + maximum cavity depth. "
            "Increase wall_height or reduce cavity_depth/depth_scale."
        )

    # Build floor coordinates.
    X = x.copy()
    Y = y.copy()

    floor_vertices = np.column_stack((
        X.ravel(),
        Y.ravel(),
        floor_z.ravel(),
    ))

    vertices = floor_vertices.tolist()
    faces = []

    # Triangulate the textured floor.
    for i in range(n_rows - 1):
        for j in range(n_cols - 1):
            a = i * n_cols + j
            b = a + 1
            c = a + n_cols
            d = c + 1

            faces.append([a, b, c])
            faces.append([b, d, c])

    # Walk around the floor perimeter in order.
    boundary = []

    for j in range(n_cols):
        boundary.append(j)

    for i in range(1, n_rows):
        boundary.append(i * n_cols + n_cols - 1)

    for j in range(n_cols - 2, -1, -1):
        boundary.append((n_rows - 1) * n_cols + j)

    for i in range(n_rows - 2, 0, -1):
        boundary.append(i * n_cols)

    # Inner top rim vertices, directly above the floor perimeter.
    inner_top = []

    for idx in boundary:
        px, py, _ = vertices[idx]
        inner_top.append(len(vertices))
        vertices.append([px, py, wall_height])

    # Outer top rim vertices, expanded outward by rim_width.
    outer_top = []

    for idx in boundary:
        px, py, _ = vertices[idx]

        if np.isclose(px, x.min()):
            px -= rim_width
        elif np.isclose(px, x.max()):
            px += rim_width

        if np.isclose(py, y.min()):
            py -= rim_width
        elif np.isclose(py, y.max()):
            py += rim_width

        outer_top.append(len(vertices))
        vertices.append([px, py, wall_height])

    # Flat bottom vertices directly below the outer perimeter.
    outer_bottom = []

    for idx in outer_top:
        px, py, _ = vertices[idx]
        outer_bottom.append(len(vertices))
        vertices.append([px, py, 0.0])

    # Close each section around the perimeter:
    # interior wall, flat rim, and exterior wall.
    n_boundary = len(boundary)

    for k in range(n_boundary):
        nxt = (k + 1) % n_boundary

        floor_a = boundary[k]
        floor_b = boundary[nxt]

        inner_a = inner_top[k]
        inner_b = inner_top[nxt]

        outer_a = outer_top[k]
        outer_b = outer_top[nxt]

        bottom_a = outer_bottom[k]
        bottom_b = outer_bottom[nxt]

        # Interior vertical wall.
        faces.append([floor_a, inner_a, inner_b])
        faces.append([floor_a, inner_b, floor_b])

        # Horizontal rim surrounding the hollow cavity.
        faces.append([inner_a, outer_a, outer_b])
        faces.append([inner_a, outer_b, inner_b])

        # Exterior vertical wall.
        faces.append([outer_a, bottom_a, bottom_b])
        faces.append([outer_a, bottom_b, outer_b])

    # Flat bottom cap, triangulated from its center.
    outer_xy = np.asarray([
        [vertices[idx][0], vertices[idx][1]]
        for idx in outer_bottom
    ])

    center_xy = outer_xy.mean(axis=0)
    center_idx = len(vertices)
    vertices.append([center_xy[0], center_xy[1], 0.0])

    for k in range(n_boundary):
        nxt = (k + 1) % n_boundary
        faces.append([
            center_idx,
            outer_bottom[nxt],
            outer_bottom[k],
        ])

    mesh = trimesh.Trimesh(
        vertices=np.asarray(vertices),
        faces=np.asarray(faces, dtype=np.int64),
        process=True,
    )

    mesh.fix_normals()

    if not mesh.is_watertight:
        raise RuntimeError(
            "The mold mesh is not watertight. "
            "Check the grid and perimeter geometry."
        )

    if mesh.volume < 0:
        mesh.invert()

    mesh.export(filename)

    print(f"Exported: {filename}")
    print(f"Watertight: {mesh.is_watertight}")
    print(f"Dimensions: {mesh.extents.round(2)}")
    print(f"Wall height: {wall_height}")
    print(f"Base thickness: {base_thickness}")
    print(f"Maximum cavity depth: {depth.max():.2f}")

    return mesh



x_vals = np.arange(0, 6 * np.pi +10.5, 0.1)
y_vals = np.arange(0, 6 * np.pi + 11.2, 0.1)
x, y = np.meshgrid(x_vals, y_vals)

# z1
A1 = 1
A2 = 0
f1 = 1
f2 = 1
phi = np.pi / 2
z1 = A1 * np.sin(f1 * x) + A2 * np.sin(f2 * y + phi)

# z2
A2 = 1
z2 = A1 * np.sin(f1 * x) + A2 * np.sin(f2 * y + phi)

# z3
z3 = np.zeros_like(x)
N = 25
for ii in range(1, N + 1, 2):
    A1 = (8 / np.pi**2) * ((-1)**((ii - 1) // 2)) / ii**2
    A2 = A1
    f1 = f2 = ii
    phi = 0
    z3 += A1 * np.sin(f1 * x) + A2 * np.sin(f2 * y + phi)

# z4
z4 = np.zeros_like(x)
N = 101
for ii in range(1, N + 1, 2):
    A1 = 4 / (np.pi * ii)
    A2 = A1
    f1 = f2 = ii
    phi = 0
    z4 += A1 * np.sin(f1 * x) + A2 * np.sin(f2 * y + phi)

# z5
z5 = np.zeros_like(x)
N = 25
for ii in range(1, N + 1, 2):
    A1 = (8 / np.pi**2) * ((-1)**((ii - 1) // 2)) / ii**2
    A2 = 0
    f1 = f2 = ii
    phi = 0
    z5 += A1 * np.sin(f1 * x) + A2 * np.sin(f2 * y + phi)

# z6
z6 = np.zeros_like(x)
N = 101
for ii in range(1, N + 1, 2):
    A1 = 4 / (np.pi * ii)
    A2 = 0
    f1 = f2 = ii
    phi = 0
    z6 += A1 * np.sin(f1 * x) + A2 * np.sin(f2 * y + phi)

# z8: Rippling Waves (Multi-frequency diagonal interference)
z8 = np.sin(x + y) + 0.5 * np.cos(2 * x - 2 * y)

# z9: Concentric Rings / Ripples (Seamlessly tiled using periodic trig inputs)
z9 = np.sin(np.sqrt(np.sin(x)**2 + np.cos(y)**2) * np.pi)

# z10: Diamond Grid (Absolute values of orthogonal waves)
z10 = np.abs(np.sin(x)) + np.abs(np.cos(y))

# z11: Woven Fabric / Basketweave (Phase shifted alternating blocks)
z11 = np.sin(x) * np.sin(y) + 0.3 * np.cos(3 * x) * np.cos(3 * y)

# z12: Hexagonal Tiling Approximation
z12 = np.cos(x) + np.cos(0.5 * x + np.sqrt(3)/2 * y) + np.cos(0.5 * x - np.sqrt(3)/2 * y)
# Note: To tile seamlessly, the Y range for hex must technically be scaled by sqrt(3), 
# but inside this 2pi domain it behaves as a beautiful modulated continuous mesh.

# z13: Sharp Ridges (Simulated volcanic or crystalline ridges)
z13 = 1.0 - np.abs(np.sin(x) * np.cos(y))

# z14: Chipped Rock / Voronoi-like facets (Using maximum intensity fields)
z14 = np.maximum(np.sin(x), np.cos(y)) + 0.5 * np.minimum(np.sin(2*x), np.cos(2*y))

# z15: Sand Dunes (Asymmetrical waves using exponentiation)
z15 = np.exp(np.sin(x)) * np.cos(y)

# z16: Cellular Dimples (Inverted egg-crate with a power curve for flat high plateaus)
z16 = -(np.sin(x/2)**2 * np.cos(y/2)**2)**0.5

# z17: Fish Scales / Scallops (Warped coordinate shifting)
z17 = np.sin(x + np.sin(y)) * np.cos(y)

# z18: Knurled Metal / Industrial Grip (Sharp diamond intersections)
z18 = np.arcsin(np.sin(x) * np.cos(y))

# z19: Swirling Fluid (Domain twisting via periodic cross-modulation)
z19 = np.sin(x + np.cos(y)) + np.cos(y + np.sin(x))

# z20: Chevron / Zig-Zag (Trigonometric triangle wave transformation)
z20 = np.arccos(np.cos(x + np.arcsin(np.sin(y))))

# z21: Organic Coral / Perlin-like Fourier synthesis (Layered octaves)
z21 = (np.sin(1*x) * np.cos(1*y) + 
       0.5 * np.sin(2*x + np.pi/4) * np.cos(2*y) + 
       0.25 * np.sin(4*x) * np.sin(4*y))


zs = [
    z1, z2, z3, z4, z5, z6, z8, z9, z10, z11, z12,
    z13, z14, z15, z16, z17, z18,
    z19, z20,z21
]
if __name__ == "__main__":
    import os

    os.makedirs("objects", exist_ok=True)

    for i, z in enumerate(zs, start=1):
        export_negative_mold(
            x,
            y,
            z,
            filename=f"/home/dexter/Documents/GitHub/3D-textures/Generator/objects_mold/z{i}_negative_mold.stl",
            wall_height=10.0,
        cavity_depth=5.0,
        base_thickness=5.0,
        rim_width=5.0,
        depth_scale=1.0,
    )
