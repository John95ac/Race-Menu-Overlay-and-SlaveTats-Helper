# 📜 Race Menu Overlay to SlaveTats Helper

Convert body paint mods RaceMenu Overlay to SlaveTats and vice versa, plus being able to create mods from scratch just with a texture folder, and organize with visual support and guidance. Includes Papyrus compilation tips and an SSEEdit script to create the ESPFE plugin with just a few clicks.

## Installation

### Prerequisites

- **Creation Kit**: Download from [Steam](https://store.steampowered.com/app/1946180/Skyrim_Special_Edition_Creation_Kit/). You only need the ...\Steam\steamapps\common\Skyrim Special Edition\Papyrus Compiler\ folder to compile PEX files. No need to open the Creation Kit itself.
- **SSEEdit**: Download from [Nexus Mods](https://www.nexusmods.com/skyrimspecialedition/mods/164). Required for automatic ESP/ESL plugin creation using the Pascal script.
- **Papyrus Compiler App**: Download from [Nexus Mods](https://www.nexusmods.com/skyrimspecialedition/mods/23852). Recommended for easy Papyrus compilation, but you can use any program you prefer.
- **Optional: 7-Zip**: For creating .7z archives (the tool falls back to .zip if not installed). Download from [7-zip.org](https://www.7-zip.org/).
- **For Generated Mods**:
- [RaceMenu](https://www.nexusmods.com/skyrimspecialedition/mods/19080)
- [SlaveTats](https://www.loverslab.com/topic/25398-slavetats/)

---

## What does it do?

The application uses a tabbed interface for organized workflows:

1. **SlaveTats → RaceMenu (.psc Generator)**: Drag or select a SlaveTats JSON file to parse overlay entries (name, section, texture, area). Generates a Papyrus PSC script with appropriate AddBodyPaint/AddWarpaint calls. Includes buttons to create an organized texture folder (`textures/Actors/Character/Overlays/<section>`) and copy DDS files, then pack into a ZIP/7z mod archive. Ideal for porting SlaveTats mods to RaceMenu.

   **Step-by-Step**:

   - Drag a JSON file onto the tab or click "Select JSON".
   - Preview the parsed data in the terminal (shows extracted entries).
   - Click "Generate .psc file" to create the script in a new `scripts/Source` folder.
   - Click "Create Texture Folder && Copy DDS" to organize DDS files into the Overlays structure (prompts for the source folder containing DDS).
   - Use "Create Mod zip" to package the mod. Watch the tutorial video via the "Video of final steps" button for post-generation steps (e.g., compiling PEX, creating ESP).
2. **RaceMenu → SlaveTats (.json Generator)**: Drag or select a RaceMenu PSC file to extract Add*Paint calls into a normalized JSON format. Previews the generated JSON and provides options to open the output folder, create mod folders (`textures/actors/character/slavetats/<section>`), and pack the mod into ZIP/7z with cleanup. Perfect for converting RaceMenu overlays to SlaveTats.

   **Step-by-Step**:

   - Drag a PSC file onto the tab or click "Select PSC".
   - Review the extracted entries (names, textures, areas) in the preview terminal.
   - Use "Create Mod folders" to copy DDS files (select the 'Overlays' folder or a subfolder containing DDS) and build the slavetats structure.
   - Click "Create Mod zip" to package the mod (automatically cleans up temporary JSON and textures folders).
3. **ST Creator (from DDS)**: Start from a DDS folder or existing JSON. Displays an editable table for each DDS file (File, Path, Section, Area, Name). Assign areas (Body/Feet/Hand/Face) and names, then export JSON. Supports loading existing JSON to edit/add entries. Create mod structure and ZIP package. Features auto-detection of new DDS files and backups.

   **Step-by-Step**:

   - Drag a DDS folder or JSON file onto the tab, or click "DRAG AND DROP JSON OR DDS FOLDER".
   - Edit the table: assign Section (group name for the overlay), Area (Body/Feet/Hand/Face), and Name (tattoo description) for each file.
   - Click "Export JSON" to generate the file (saved in the parent folder of the DDS directory).
   - Use "Create Mod zip" to build the `textures/actors/character/slavetats` structure and package into ZIP/7z.
   - Manage backups via the "Backups" button (creates/restores timestamped JSON copies).
4. **RM Creator (from DDS)**: Similar to ST Creator but tailored for RaceMenu. Editable table for DDS files (File, Path, Type: BodyPaint/Warpaint/HandPaint/FeetPaint/FacePaint, Name). Drag PSC to load and edit existing scripts. Export PSC to `scripts/Source` and create mod ZIP with Overlays structure.

   **Step-by-Step**:

   - Drag a DDS folder or PSC file onto the tab, or click "DRAG AND DROP PSC OR DDS FOLDER".
   - Edit the table: assign Type (BodyPaint/Warpaint/etc.) and Name for each file.
   - Click "Export .psc" to generate the script in the `scripts/Source` folder.
   - Use "Create Mod zip" to package with the `textures/Actors/Character/Overlays` structure.
5. **PCA Papyrus Compile Helper**: Assists with Papyrus compilation in Mod Organizer 2 (MO2) or standalone mode. Configurable paths via INI (e.g., Source, `overwrite/scripts`). Buttons to copy files to `overwrite/source/scripts`, select/copy .psc files, and move/clean .pex outputs. Includes quiet modes, auto-run on .pex detection, and MO2 emulator support. Terminal logs compilation steps.

   **Step-by-Step**:

   - Click the gear icon (⚙) to configure paths (supports MO2 integration or standalone emulator mode).
   - Click "Copy Files to Scripts" to copy all files from the Source folder to `overwrite/source/scripts`.
   - Select or drag .psc files with "Select and Copy .psc Files" to prepare for compilation.
   - Compile using PCA 2022.1 (the tool monitors .pex files in `overwrite/scripts`).
   - Click "Run Move and Clean" to move compiled .pex files to the destination and clean `source/scripts`.
   - Use checkboxes for quiet modes (reduces logs) and auto-run (triggers on .pex detection).
6. **Tips**: Displays random motivational tips from Advice.ini/tips.ini (supports bold, italic, links) and cute cat images/GIFs from `Data/CAT`. Refreshes on button click for quick breaks during modding. Click "Web Documents John95AC" for online documentation, advancements, and resources.

---

## Key Workflows

- **JSON to PSC Conversion (SlaveTats → RaceMenu)**: Import JSON → generate PSC script in `scripts/Source` → organize DDS into `Overlays/<section>` → pack ZIP/7z mod. Includes tutorial video link for final steps (compiling PEX, creating ESP).
- **PSC to JSON Conversion (RaceMenu → SlaveTats)**: Import PSC → parse to JSON → create `slavetats` structure → copy DDS → pack ZIP/7z with cleanup.
- **Mod Creation from DDS**: Select DDS folder → edit table (assign types/areas/names) → export JSON/PSC → build mod folder (`textures/actors/character/overlays` or `slavetats`) → ZIP/7z package. Supports previews (click DDS names) and backups.
- **DDS Preview**: Click DDS filenames in tables to open a dedicated window with zoom/pan (mouse wheel/middle-click drag), background color/image selection (from `Data/DDS`), and contrast adjustments via sliders.
- **Backups**: Automatic timestamped backups for JSON/PSC in a `Backups` subfolder. Dedicated manager dialog to create/restore/list backups (accessible via "Backups" button in creator tabs).
- **Compilation Assistance**: Copy to MO2 `overwrite/source/scripts` → compile with PCA → auto-move .pex and clean. Quiet modes reduce logs; emulator allows standalone use without MO2.

---

## Updates and Revisions

**Version 1.0.0**:

This is the first version of the tool, introducing core functionality for conversions between RaceMenu PSC and SlaveTats JSON, DDS mod creation from scratch, and Papyrus compilation assistance with PCA helper. It provides a dark-themed interface with drag-and-drop, DDS previews, backups, and mod packaging tools for streamlined Skyrim modding workflows.

---

## Acknowledgements

### Beta Testers

<table>
<tr>
<td><img src="Beta Testers/Wolfen09.png" width="100" height="100" alt="Wolfen09"></td>
</tr>
</table>

Special thanks to **Wolfen09**. From a casual conversation on Discord, we realized that converting a package from SlaveTats to RaceMenu was complicated because it requires not only a specific folder structure but also a compilation and a plugin. It was a casual conversation, so I put it on the back burner. However, since I had some free time and a great new mod for RaceMenu called [Overlay Distribution Framework](https://www.nexusmods.com/skyrimspecialedition/mods/155120) was released, I decided to create this program. This tool facilitates and structures the steps to make the conversion process from one to the other much easier.

Special thanks to **[SlaveTats](https://www.nexusmods.com/skyrimspecialedition/mods/19080)**, **[RaceMenu](https://www.nexusmods.com/skyrimspecialedition/mods/19080)**, and **[PCA Papyrus Helper](https://www.nexusmods.com/skyrimspecialedition/mods/23852)**. These are excellent mods and tools that have helped me a lot in my games, especially in Skyrim. Thank you so much for existing.

Special thanks to **[UBE 2.0 Ultimate Body](https://www.nexusmods.com/skyrimspecialedition/mods/92989)** and **[Bijin Skin UNP and CBBE SE](https://www.nexusmods.com/skyrimspecialedition/mods/20078)**. Thanks to these magnificent mods for their incredible body textures, which many use as a base for creating and aligning tattoos.

Special thanks to the **Modding Community**. For the constant feedback and ideas for improvements.

Special thanks to **[SSEEdit](https://www.nexusmods.com/skyrimspecialedition/mods/164)**. Through the use of its Pascal scripting capabilities, it's possible to create the necessary ESP plugin without ever touching the Creation Kit, even though it took months to create the correct code.

Special thanks to the **Python language**. This entire project was made possible by it. Thank you very much.

Special thanks to **[Mermaid](https://mermaid.js.org/)**, **[Excalidraw](https://excalidraw.com/)**, and **[Time.Graphics](https://time.graphics/)**. Thanks to these free and very useful tools for drawing and creating diagrams.

---

## Requirements

- **Core (Tool)** :RM_and_ST_Helper.exe or RM_and_ST_Helper_Python.pyw [Creation_Kit](https://store.steampowered.com/app/1946180/Skyrim_Special_Edition_Creation_Kit/): you can download it here, we'll only need the ...\Steam\steamapps\common\Skyrim Special Edition\Papyrus Compiler\ which is necessary to compile PEX, nothing else, no need to even open it, just download. [SSEEdit](https://www.nexusmods.com/skyrimspecialedition/mods/164). [Papyrus_Compiler_App](https://www.nexusmods.com/skyrimspecialedition/mods/23852).
- **For Generated Mods**:
- [RaceMenu](https://www.nexusmods.com/skyrimspecialedition/mods/19080)
- [SlaveTats](https://www.loverslab.com/topic/25398-slavetats/)
