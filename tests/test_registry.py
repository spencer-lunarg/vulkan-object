
import pytest

# Since the package is installed in editable mode, we can import it directly.
from vulkan_object import get_vulkan_object, VulkanObject

def test_get_vulkan_object_successfully():
    """
    Tests that the main function runs without errors and returns the correct type.
    This is a basic "smoke test".
    """
    print("Running: test_get_vulkan_object_successfully")
    vk_object = get_vulkan_object()

    # Check that the function returned an object
    assert vk_object is not None, "get_vulkan_object() returned None"

    # Check that the returned object is of the expected class
    assert isinstance(vk_object, VulkanObject), f"Expected VulkanObject, but got {type(vk_object)}"
    print("Success: Returned object is a non-None VulkanObject.")


def test_registry_contains_expected_content():
    """
    Verifies that the parsed registry object contains some known, expected data.
    This confirms that the XML parsing logic is working correctly.
    """
    print("Running: test_registry_contains_expected_content")
    vk_object = get_vulkan_object()

    # Check for a well-known command
    assert 'vkCreateInstance' in vk_object.commands, "'vkCreateInstance' not found in commands"
    print("Success: Found 'vkCreateInstance' command.")

    # Check for a well-known struct
    assert 'VkApplicationInfo' in vk_object.structs, "'VkApplicationInfo' not found in structs"
    print("Success: Found 'VkApplicationInfo' struct.")

    # Check a detail within a struct
    app_info_struct = vk_object.structs['VkApplicationInfo']
    member_names = [member.name for member in app_info_struct.members]
    assert 'pApplicationName' in member_names, "'pApplicationName' not found in VkApplicationInfo members"
    print("Success: Found 'pApplicationName' in 'VkApplicationInfo' members.")


def test_caching_works():
    """
    Ensures that the lru_cache is working by verifying that subsequent calls
    to the function return the exact same object instance.
    """
    print("Running: test_caching_works")

    # Call the function twice
    vk_object_first_call = get_vulkan_object()
    vk_object_second_call = get_vulkan_object()

    # The `id()` function returns the memory address of an object.
    # If caching works, both variables should point to the same object.
    assert id(vk_object_first_call) == id(vk_object_second_call), "Caching failed: objects have different IDs"
    print("Success: Caching is working as expected.")


# TODO - Add VulkanSC as a test (not working currently)
@pytest.mark.parametrize("api_name", ["vulkan"])
def test_different_apis(api_name: str):
    """
    Tests that the function can be called with different `api_name` parameters.
    Note: This requires clearing the cache to get a fresh object.
    """
    # Clear the cache to ensure we are actually re-running the logic
    get_vulkan_object.cache_clear()

    print(f"Running: test_different_apis with api_name='{api_name}'")
    vk_object = get_vulkan_object(api_name=api_name)
    assert vk_object is not None
    assert isinstance(vk_object, VulkanObject)
    print(f"Success: Successfully loaded registry for '{api_name}'.")

