from .blur_effect import apply_blur
from .grayscale_effect import apply_grayscale
from .edge_detection_effect import apply_edges as apply_edge_detection
from .sepia_effect import apply_sepia
from .inversion_effect import apply_inversion
from .blue_boost_effect import apply_blue_boost
from .warm_filter_effect import apply_warm_filter
from .stable_diffusion_effect import apply_stable_diffusion  # Оставляем нетронутым
from .detection_effect import apply_object_detection  # Оставляем нетронутым

EFFECTS = {
    "blur": apply_blur,
    "grayscale": apply_grayscale,
    "edges": apply_edge_detection,
    "sepia": apply_sepia,
    "inversion": apply_inversion,
    "blue_boost": apply_blue_boost,
    "warm_filter": apply_warm_filter,
    "stable_diffusion": apply_stable_diffusion,  # Оставляем нетронутым
    "object_detection": apply_object_detection   # Оставляем нетронутым
}
