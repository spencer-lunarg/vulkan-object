import functools
import importlib.resources
import tempfile
from xml.etree import ElementTree
from typing import Any

# Use relative imports to access sibling modules
from .reg import Registry
from .base_generator import BaseGenerator, BaseGeneratorOptions, SetOutputDirectory, SetOutputFileName, SetTargetApiName, SetMergedApiNames
from .vulkan_object import VulkanObject

# Define the public API for your package
__all__ = [
    'get_vulkan_object',
    'VulkanObject'  # Exposing the class is good for type-hinting
]

# Create the simplified, cached public function
@functools.lru_cache(maxsize=1)
def get_vulkan_object(api_name: str = 'vulkan') -> VulkanObject:
    """
    Parses the bundled Vulkan registry (vk.xml) and returns the populated
    VulkanObject.

    This function encapsulates all the setup logic. The result is cached,
    so subsequent calls are instantaneous.

    Args:
        api_name: The API name to parse from the registry, defaults to 'vulkan'.

    Returns:
        An initialized VulkanObject instance providing access to the
        Vulkan API registry data.
    """
    # This dummy generator class is required by the reg.py interface.
    # We don't need it to do anything, as we just want the parsed data object.
    class _InternalGenerator(BaseGenerator):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def generate(self):
            # This method is called by reg.apiGen() but we don't need to
            # generate any files, so we just pass. The real goal is to
            # populate self.vk (the VulkanObject).
            pass

    # The original script required setting an output directory, even if
    # it's not used. We'll use a temporary one that cleans itself up.
    with tempfile.TemporaryDirectory() as output_dir:
        SetOutputDirectory(output_dir)
        SetOutputFileName("unused.txt")
        SetTargetApiName(api_name)
        SetMergedApiNames(None) # Set to None if not merging APIs

        # Initialize the generator and the registry machinery
        generator = _InternalGenerator()
        base_options = BaseGeneratorOptions()
        reg = Registry(generator, base_options)

        # Reliably find and parse vk.xml
        try:
            with importlib.resources.path('vulkan_object', 'vk.xml') as xml_path:
                tree = ElementTree.parse(xml_path)
                reg.loadElementTree(tree)

        except FileNotFoundError:
            raise RuntimeError(
                "Could not find the bundled vk.xml - something has gone wrong with packaging."
            )

        # This invokes reg.py and will populate _InternalGenerator
        reg.apiGen()

        return generator.vk

