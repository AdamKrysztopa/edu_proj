# Early K0 items (draft for the physicist check)

**Status:** draft. A physicist who teaches first-year mechanics checks every item, answer and time estimate before registration. After registration, any change is a logged deviation (`prereg-early-k0.md`).

**Constraints the items meet:**
- The same principle structure as the Stage A problems: a perfectly inelastic collision, then energy conservation (gravity or spring).
- Different surfaces from every Stage A problem (A1–B2) and from E_A and E_B.
- The roadmap's illustrative items (`research/roadmap.md` step 4: skater and sled, bullet into a block on a spring, skaters pushing off) share surface or structure with K0-1 and K0-2. They are barred from the delayed test and from module materials.
- Form 1 is the registered K0 pair. The Stage B pretest reuses it unchanged.
- No item may repeat, or be isomorphic to, a delayed-test item. The delayed-test authors receive this file to check that.

Use g = 9.8 m/s². Friction and air resistance are negligible unless stated.

## Form 1 (registered K0 items)

Hand out on one sheet and collect it. Budget about 15 minutes.

**K0-1.** A 0.50 kg snowball moving horizontally at 8.0 m/s hits a 1.5 kg sled at rest on a level icy patch at the foot of a hill, and sticks to it. The level patch curves smoothly into the hill, and the sled slides up it. How high, measured vertically, does the sled rise? Show your reasoning.

**K0-2.** A 20 g dart moving at 15 m/s hits a 0.28 kg puck at rest on frictionless ice and embeds in it. The puck then slides straight into an ideal horizontal spring (k = 150 N/m), initially uncompressed, whose other end is fixed to a wall. What is the maximum compression of the spring? Show your reasoning.

## Form 2 (parallel form, about a week later)

The same structure with new surfaces, for the per-student agreement check only. Form 2 never enters the K0 decision. K0-1b pairs with K0-1 and K0-2b with K0-2. Budget about 15 minutes.

**K0-1b.** On level ground, a 2.0 kg toy truck moving at 3.6 m/s runs into a 1.0 kg toy car at rest, and the two couple together. The pair then moves onto a smoothly connected ramp. Neglect the energy of the spinning wheels. What maximum vertical height do they reach?

**K0-2b.** A 1.2 kg air-track glider moving at 2.5 m/s latches onto a 0.80 kg glider at rest. The pair then runs straight into an ideal bumper spring (k = 250 N/m) at the end of the level track, initially uncompressed, with its far end fixed. What is the maximum compression of the spring?

## Components (single principle)

On a separate sheet, handed out after Form 2 is collected, so that the split into stages is not taught between the forms. The order of the four items is randomized per student and recorded. Budget about 8 minutes.

- **C1a (momentum).** A 0.30 kg ball of putty moving at 6.0 m/s hits a 0.90 kg cart at rest on a level track and sticks to it. How fast does the cart move just afterwards?
- **C1b (energy, gravity).** A sled moving at 3.0 m/s reaches the bottom of an icy hill. How high does it rise?
- **C2a (momentum).** A 30 g dart moving at 12 m/s embeds in a 0.27 kg block at rest on frictionless ice. How fast does the block move just afterwards?
- **C2b (energy, spring).** A 0.40 kg puck sliding at 1.5 m/s on frictionless ice runs straight into an ideal horizontal spring (k = 90 N/m), initially uncompressed, whose other end is fixed to a wall. What is the maximum compression?

## Answer key (coders only)

| Item | Stage 1 (momentum) | Stage 2 (energy) | Answer |
|---|---|---|---|
| K0-1 | v = (0.50 × 8.0) / 2.0 = 2.0 m/s | h = v² / 2g = 4.0 / 19.6 | 0.20 m |
| K0-2 | v = (0.020 × 15) / 0.30 = 1.0 m/s | x = v √(m/k) = 1.0 × √(0.30/150) | 0.045 m (4.5 cm) |
| C1a | v = (0.30 × 6.0) / 1.2 | — | 1.5 m/s |
| C1b | — | h = 9.0 / 19.6 | 0.46 m |
| C2a | v = (0.030 × 12) / 0.30 | — | 1.2 m/s |
| C2b | — | x = 1.5 × √(0.40/90) | 0.10 m |
| K0-1b | v = (2.0 × 3.6) / 3.0 = 2.4 m/s | h = 5.76 / 19.6 | 0.29 m |
| K0-2b | v = (1.2 × 2.5) / 2.0 = 1.5 m/s | x = 1.5 × √(2.0/250) | 0.13 m |

Common wrong answers, for recognising errors quickly:
- K0-1: energy conserved across the collision gives h = 8.0² / 19.6 × (0.50/2.0) = 0.82 m or h = 3.3 m (which also keeps the snowball's speed after the collision).
- K0-2: energy conserved from the dart's kinetic energy gives x = √(0.020 × 15² / 150) = 0.17 m.
