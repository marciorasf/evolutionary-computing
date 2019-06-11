import builtins as _mod_builtins

class RendererAgg(_mod_builtins.object):
    __class__ = RendererAgg
    def __init__(self, *args, **kwargs):
        pass
    
    @classmethod
    def __init_subclass__(cls):
        'This method is called when a class is subclassed.\n\nThe default implementation does nothing. It may be\noverridden to extend subclasses.\n'
        return None
    
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    def buffer_rgba(self):
        pass
    
    def clear(self):
        pass
    
    def copy_from_bbox(self):
        pass
    
    def draw_gouraud_triangle(self):
        pass
    
    def draw_gouraud_triangles(self):
        pass
    
    def draw_image(self):
        pass
    
    def draw_markers(self):
        pass
    
    def draw_path(self):
        pass
    
    def draw_path_collection(self):
        pass
    
    def draw_quad_mesh(self):
        pass
    
    def draw_text_image(self):
        pass
    
    def get_content_extents(self):
        pass
    
    def restore_region(self):
        pass
    

__doc__ = None
__file__ = '/home/marciorasf/github/ComputacaoEvolucionaria-2019.1/ce_venv/lib/python3.7/site-packages/matplotlib/backends/_backend_agg.cpython-37m-x86_64-linux-gnu.so'
__name__ = 'matplotlib.backends._backend_agg'
__package__ = 'matplotlib.backends'