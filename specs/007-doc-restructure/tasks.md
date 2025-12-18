# Tasks for Documentation Restructuring

## Phase 1: Preparation and Inventory

- [ ] T001 [US1] Identify all existing "Module-X" directories under `docs/` that need to be restructured. (Assumed to be `docs/ros2-fundamentals` for now, but will need a mechanism to discover others).
- [ ] T002 [US1] Create a comprehensive manifest of all documentation files (`.md`, `.mdx`) and associated asset files (e.g., `img/` folders) within the identified module directories, including their current absolute paths.
- [ ] T003 [US1] Establish the explicit mapping from each identified "Module-X" to its corresponding "Chapter-Y" name and new relative path (e.g., `docs/ros2-fundamentals` -> `docs/The Physical Human Robotic AI/Chapter-2`). This will require a configuration file or internal data structure.

## Phase 2: New Structure Creation

- [ ] T004 [US1] Create the new top-level parent folder: `docs/The Physical Human Robotic AI/`.
- [ ] T005 [US1] For each entry in the module-to-chapter mapping, create the corresponding "Chapter-X" directory under `docs/The Physical Human Robotic AI/`.

## Phase 3: File Movement

- [ ] T006 [US1] Move all documentation files identified in the manifest from their original module paths to their new chapter paths.
- [ ] T007 [US1] Move all associated asset files (e.g., `img/` folders and their contents) identified in the manifest from their original module paths to their new chapter paths, maintaining their relative structure within the chapter.
- [ ] T008 [US1] Verify that all files have been successfully moved and no files are lost or inadvertently deleted. (This could involve comparing manifests and checking file existence).

## Phase 4: Internal Link Updating

- [ ] T009 [US1] Develop a script (`scripts/update_links.py`) to parse all moved `.md` and `.mdx` files.
- [ ] T010 [US1] Within the script, identify all internal relative markdown links `[text](path)` and image links `![alt](path)`.
- [ ] T011 [US1] For each identified internal relative link, calculate its new relative path based on the file's new location and the target's new location.
- [ ] T012 [US1] Update the content of each documentation file by replacing old relative links with their newly calculated paths.
- [ ] T013 [US1] Ensure external links and absolute links remain unchanged.

## Phase 5: Verification and Final Checks

- [ ] T014 [US1] Verify that no documentation files within the new chapter folders are empty after the restructuring. (If any are empty, generate a reasonable default section as per requirement).
- [ ] T015 [US1] Run Docusaurus build command (`npm run build`) to check for any broken links or structural errors introduced by the restructuring.
- [ ] T016 [US1] Manually review the generated Docusaurus output for visual correctness and navigation functionality.

## Phase 6: Docusaurus Integration (sidebars.ts)

- [ ] T017 [US1] Update `sidebars.ts` to reflect the new parent folder "The Physical Human Robotic AI" and the "Chapter-X" structure, replacing any old module-based entries.
- [ ] T018 [US1] Run Docusaurus local server (`npm run start`) and visually verify the new sidebar navigation.
