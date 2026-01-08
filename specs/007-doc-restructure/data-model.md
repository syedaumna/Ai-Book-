# Data Model for Documentation Restructuring Feature

This document defines the key entities and their attributes that are relevant to the documentation restructuring process. This data model helps formalize the input, intermediate states, and output of the restructuring operation.

## Key Entities

### 1. Module Folder

Represents an existing directory that contains documentation files for a specific module before restructuring.

-   **Attributes**:
    -   `id` (string): Unique identifier (e.g., "Module-1").
    -   `original_path` (string): Absolute path to the module directory (e.g., `docs/ros2-fundamentals/`).
    -   `content_files` (list of `DocumentationFile` entities): List of documentation files residing directly within this module folder or its subdirectories.
    -   `asset_files` (list of `DocumentationFile` entities): List of non-documentation asset files (e.g., images) residing directly within this module folder or its subdirectories.
    -   `sub_folders` (list of `ModuleFolder` entities): Nested module folders if the structure is deeper.

### 2. Chapter Folder

Represents a new directory that will contain documentation files for a specific chapter after restructuring.

-   **Attributes**:
    -   `id` (string): Unique identifier (e.g., "Chapter-1").
    -   `target_path` (string): Absolute path to the new chapter directory (e.g., `docs/The Physical Human Robotic AI/Chapter-1/`).
    -   `corresponding_module_id` (string): The ID of the `Module Folder` from which files will be moved.
    -   `documentation_files` (list of `DocumentationFile` entities): List of documentation files that will be moved into this chapter folder.
    -   `asset_files` (list of `DocumentationFile` entities): List of asset files that will be moved into this chapter folder.

### 3. Documentation File

Represents a single markdown file (`.md`, `.mdx`) or any other textual documentation file that might contain internal links.

-   **Attributes**:
    -   `original_path` (string): Absolute path to the file before moving (e.g., `docs/ros2-fundamentals/nodes.md`).
    -   `new_path` (string): Absolute path to the file after moving (e.g., `docs/The Physical Human Robotic AI/Chapter-2/nodes.md`).
    -   `content` (string): The complete text content of the file.
    -   `internal_links` (list of `InternalLink` entities): All identified internal relative links within this file.
    -   `is_empty` (boolean): True if the file contains no meaningful content.

### 4. Asset File

Represents a non-documentation file (e.g., image, video, PDF) that needs to be moved alongside documentation files and might be referenced by them.

-   **Attributes**:
    -   `original_path` (string): Absolute path to the asset file before moving (e.g., `docs/ros2-fundamentals/img/diagram.png`).
    -   `new_path` (string): Absolute path to the asset file after moving (e.g., `docs/The Physical Human Robotic AI/Chapter-2/img/diagram.png`).

### 5. Internal Link

Represents a relative link found within a `DocumentationFile` that needs to be updated.

-   **Attributes**:
    -   `file_path` (string): Path to the `DocumentationFile` containing this link.
    -   `original_link_text` (string): The original relative path as found in the markdown (e.g., `../images/diagram.png`).
    -   `original_target_path` (string): The absolute path that the original link points to.
    -   `new_link_text` (string): The calculated new relative path after restructuring.
    -   `new_target_path` (string): The absolute path that the updated link should point to.
    -   `start_index` (integer): The starting character index of the link in the `content` string for precise replacement.
    -   `end_index` (integer): The ending character index of the link in the `content` string.

### 6. Restructuring Plan

A high-level overview of the entire restructuring operation.

-   **Attributes**:
    -   `new_parent_folder_name` (string): "The Physical Human Robotic AI".
    -   `module_to_chapter_mapping` (map of string to string): Defines how each detected `Module Folder` maps to a `Chapter Folder`.
    -   `files_to_move` (list of `DocumentationFile` or `AssetFile` entities): All files slated for relocation.
    -   `links_to_update` (list of `InternalLink` entities): All internal links requiring modification.
