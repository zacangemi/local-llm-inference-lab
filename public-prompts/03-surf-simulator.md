Build a polished third-person 3D surfing game that runs in a desktop browser.

This is not a menu mock-up, a 2D side-view game, or a feature checklist. The
finished result must make the player feel like they are standing on a board and
riding a powerful breaking ocean wave. The wave is the star; the surfer,
camera, controls, physics, and effects must all make that single fantasy
convincing.

## Product target

Create one focused, replayable surf session in stylized realism. The camera
follows slightly above and behind a recognizable surfer as they ride across the
face of a large wave. The player should be able to see the trough below, the
crest and pitching lip above, clean face ahead, and turbulent whitewater
chasing from behind. Movement on the face must be readable: dropping generates
speed, pumping and carving preserve or build it, stalling sacrifices it, and
the lip can launch the rider into the air.

Spend your effort in this order:

1. A convincing, readable breaking wave.
2. A recognizable surfer, board, and useful chase camera.
3. Satisfying surf movement and interaction with the wave.
4. A complete playable loop with wipeouts and restart.
5. Visual, audio, and interface polish.

One excellent wave and one satisfying rider are more valuable than additional
modes, menus, locations, or loosely implemented features.

## Required experience

### The ocean and wave

- Render a continuous 3D ocean with depth, lighting, a horizon, and surface
  motion. It must read as water rather than a flat opaque sheet.
- Build one dominant rideable wave with an identifiable trough, rising face,
  crest, breaking lip, foam line, and turbulent whitewater zone. Its form and
  break must evolve over time.
- The clean face and broken section must be visually different. Foam, spray,
  mist, transparency, color, highlights, and shadow should communicate where
  the energy is.
- The visible water surface and the surface used by board physics must agree;
  the board cannot visibly float above or cut through an unrelated wave.
- A repeated sine ribbon, a row of identical hills, a static plane with a
  scrolling texture, or a rectangle labeled as whitewater does not satisfy the
  wave requirement.

### The surfer and camera

- Create a clearly recognizable procedural surfer with a head, torso, arms,
  and legs standing on a distinct surfboard. Simple low-poly geometry is fine;
  a rectangle or board with no rider is not.
- Animate the stance so the rider bends, leans, and reacts to pumping,
  carving, airtime, landing, and wipeout states.
- Use a smooth third-person chase camera positioned above and behind the
  surfer. It should frame the rider and enough of the wave to read the pocket,
  lip, and approaching line without producing disorienting jumps.

### Controls and surf feel

Use a compact keyboard scheme and show it on the title screen:

- `W` or `ArrowUp`: pump and drive for speed.
- `A` / `D` or `ArrowLeft` / `ArrowRight`: carve and use the rail; rotate in
  the air.
- `S` or `ArrowDown`: stall and move deeper toward the pocket.
- `Space`: kick out or launch from the lip when the position and speed allow.
- `R`: reset after a wipeout or recover from an unrecoverable state.
- `Enter`: start or restart the run.

The rider must not move at one constant automatic speed. Height on the face,
downslope motion, pumping, carving load, drag, and whitewater pressure should
matter. Leaving the lip produces an airborne ballistic arc. A landing succeeds
only when the board reconnects near the water surface with a plausible angle;
a bad landing or capture by whitewater causes a visible wipeout.

### Playable loop

- Provide title, riding, wipeout, and run-complete states with no dead ends.
- Show a restrained HUD with speed, score, combo, and wipeouts remaining.
- Reward near-pocket riding, controlled carving, airtime, rotations, and clean
  landings. Reset the combo on wipeout. Persist a local high score.
- Make the session intensify over time through wave energy, break behavior, or
  whitewater pressure—not merely by multiplying the camera scroll speed.
- Include procedural spray, foam, landing impact, and at least subtle camera
  response. Generate a small ocean/surf soundscape and action cues with the Web
  Audio API; use no audio files.

## Visual direction

Aim for a modern stylized surf game: sunlit atmosphere, blue-green water with
visible depth, bright foam, a readable human silhouette, convincing scale, and
smooth motion. It may be low-poly, but it must look intentionally composed and
three-dimensional. Do not fall back to flat 2D shapes, retro placeholder art,
or debug geometry as the final presentation.

## Scope boundary

Do not build an open world, beach exploration, character selector, multiple
boards, multiplayer, online leaderboard, database, or account system. Do not
spend the session on stretch features before the core ride looks and feels
convincing. A barrel is welcome only if the core wave, rider, and controls are
already strong.

## Technical constraints

- Use the pinned local Three.js ES modules already supplied under
  `vendor/three-0.185.1/`. Do not modify the vendor directory.
- The final project may use `index.html`, local JavaScript modules, and local
  CSS. It does not need to be a single file.
- Vanilla JavaScript and the supplied Three.js runtime only. Do not install
  packages and do not use the internet, CDNs, external APIs, models, textures,
  images, audio, fonts, or other assets.
- Generate all geometry, materials, textures, particles, animation, and sound
  procedurally in code.
- Target a smooth 60 fps at 1600×1000 in a current WebGL2 desktop browser.
- Make resize handling and device-pixel-ratio limits sensible.

## Validation contract

You cannot rely on the user to debug the result. Work autonomously through an
implementation, test, repair, and polish loop:

1. Build the smallest complete vertical slice centered on the wave, surfer,
   camera, and controls.
2. Serve it locally and launch the supplied headless Chrome against it.
3. Check that the page loads without uncaught JavaScript or WebGL errors and
   that the animation loop advances.
4. Exercise start, movement, launch, wipeout, and restart behavior. Add a
   lightweight deterministic debug or self-check interface if needed to make
   those states testable.
5. Capture both the title state and an active gameplay state at 1600×1000.
6. Inspect what can be established from the browser results and captured
   state, repair defects, and perform at least one additional browser pass
   before finishing.

Do not declare completion immediately after writing the initial files. Do not
list a required core behavior as a known issue instead of fixing it. If a
feature remains incomplete, say so accurately.

## Deliverables

- A runnable project rooted at `index.html`.
- `captures/title.png` and `captures/gameplay.png`, created by the browser from
  the final implementation and not placeholder image files.
- `NOTES.md` containing controls, architecture, tests actually run, what works,
  honest known limitations, and the next improvements you would make.

There is no time limit. Ship only after the surf session is playable, the
browser validation passes, and the final result represents your best work.
