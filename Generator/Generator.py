import numpy as np
import trimesh
from scipy.spatial import Delaunay
# Create meshgrid
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
    z19, z20
]



def surface_to_stl(x, y, z, filename='output.stl', height_offset=0):
    # Flatten the meshgrid and shift z if needed
    vertices = np.column_stack((x.ravel(), y.ravel(), z.ravel() + height_offset))
    
    # Create faces using row and column indexing
    n_rows, n_cols = x.shape
    faces = []
    for i in range(n_rows - 1):
        for j in range(n_cols - 1):
            idx = i * n_cols + j
            faces.append([idx, idx + 1, idx + n_cols])
            faces.append([idx + 1, idx + n_cols + 1, idx + n_cols])
    
    # Convert to numpy arrays
    faces = np.array(faces)
    
    # Create mesh and export
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.export(filename)
    print(f"Exported {filename}")

def export_surface_to_solid_block(x, y, z, filename="solid_block.stl", thickness=7.0):
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    thickness=thickness-(np.max(z)-np.min(z))
    print(thickness)
    assert x.shape == y.shape == z.shape

    # Flatten to 1D for triangulation
    x_flat = x.ravel()
    y_flat = y.ravel()
    z_flat = z.ravel()
    top_vertices = np.column_stack((x_flat, y_flat, z_flat))

    # Triangulate x-y
    tri = Delaunay(np.column_stack((x_flat, y_flat)))
    top_faces = tri.simplices

    # Create bottom vertices (same x, y, but lowered z)
    bottom_vertices = np.column_stack((x_flat, y_flat, np.full_like(z_flat, z.min() - thickness)))

    # Join vertices
    vertices = np.vstack((top_vertices, bottom_vertices))
    n_points = len(top_vertices)

    # Top and bottom faces
    bottom_faces = tri.simplices[:, ::-1] + n_points  # flip to keep normal consistent

    # --- Find boundary edges (edges belonging to only 1 triangle) ---
    edge_count = {}
    for face in tri.simplices:
        for i in range(3):
            a, b = sorted((face[i], face[(i + 1) % 3]))
            edge = (a, b)
            edge_count[edge] = edge_count.get(edge, 0) + 1

    boundary_edges = [edge for edge, count in edge_count.items() if count == 1]

    # Side faces (two triangles per boundary edge)
    side_faces = []
    for a, b in boundary_edges:
        a_bot = a + n_points
        b_bot = b + n_points
        # Triangle 1: a, b, b_bot
        side_faces.append([a, b, b_bot])
        # Triangle 2: a, b_bot, a_bot
        side_faces.append([a, b_bot, a_bot])

    # Combine all faces
    faces = np.vstack((top_faces, bottom_faces, side_faces))

    # Export as mesh
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=True)
    mesh.export(filename)
    print(f"Exported watertight solid block to {filename}")

if __name__=="__main__":
    for i,_ in enumerate(zs):
        export_surface_to_solid_block(x, y, _, filename='objects/z'+str(i)+'_surface.stl')