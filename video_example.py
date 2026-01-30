#!/usr/bin/env python3
# Copyright 2026 The Khronos Group Inc.
#
# SPDX-License-Identifier: Apache-2.0

from src.vulkan_object import get_vulkan_object, VulkanObject

vk = get_vulkan_object(video=True)

# Example 1
print("VideoStdHeader")
for headers in vk.videoStd.headers.values():
    print(f'- {headers.name}')

print("\n----------------------------------------------------\n")

# Example 2
print("VideoCodec")
for codec in vk.videoCodecs.values():
    print(f'- {codec.name}')
    print('  Profiles:')
    for profile in codec.profiles.values():
        print(f'  - {profile.name}')
    print('  Formats:')
    for format in codec.formats.values():
        print(f'  - {format.name}')

print("\n----------------------------------------------------\n")
