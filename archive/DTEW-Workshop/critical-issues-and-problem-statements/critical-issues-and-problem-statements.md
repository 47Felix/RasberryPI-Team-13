# Wednesday 02.09. – Critical Issues, Problem Statements & Ideation

**Team 13 – Case 3: Feed/Recommender Design against Bubble Reinforcement**

> Draft prepared ahead of the live session, to be confirmed/trimmed with the team, then transferred to the official `Critical_Issues.pdf` from the main board and shared on the Team Board. Full background: see `DTEW 0209 - Kritische Punkte, Problem Statements und Ideation.md` in the vault.

## Critical Issues (draft, trim to 5–10 with the team)

1. **Unconscious problem for part of the target group:** users like "Mia" often don't realize they're in a bubble; hard to address without feeling patronizing.
2. **Conflict with the underlying business model:** real platforms optimize feeds for engagement, not diversity. Our prototype deliberately does the opposite and needs to make that legible.
3. **Hard balance of "varied but still relevant":** too many counter-perspectives feel like spam/irrelevant, too few change nothing. The core difficulty of the whole brief.
4. **No prior ML experience in the team:** building a "real" ML recommender in 2 weeks is risky. Using an existing framework is a precondition.
5. **No example dataset yet:** a credible demo needs content with recognizable perspectives/"camps" (synthetic vs. real data, licensing questions still open).
6. **No metric yet:** how do we measure/show "perspective diversity" at all, rather than just claiming it subjectively?
7. **Differentiation from digi&demo's own product "pleenum":** what makes our prototype different/complementary instead of a duplicate?
8. **User acceptance:** will users accept a deliberately "disruptive" counter-opinion in their feed, or will they just close the app?

*(Points 9/10 to be added on-site if peer feedback or the daily surfaces new angles, e.g. technical room/WebEx constraints, time pressure until Friday.)*

## Problem Statements (draft, pick/sharpen one before ideation)

**PS1 – for persona "Mia" (doesn't notice the bubble):**
> How might we help young adults (18–25), who consider their "For You" feed balanced, recognize unconscious filter bubbles and encounter topically relevant counter-perspectives, without feeling patronized or disrupted?

**PS2 – for persona "Tom" (wants out, can't find a way):**
> How might we enable young adults, who actively want to break out of their filter bubble but keep getting pulled back to similar content by the algorithm, to get a feed that deliberately shows diverse but still topically relevant perspectives, without having to search for them themselves?

## Ideation draft (Walt-Disney method: Dreamer / Realist / Critic)

Starting point for the real 3-person round, not a finished result.

- **Dreamer:** A feed that openly shows which "bubble" you're currently in (e.g. a visible "perspective compass") and proactively weaves in well-curated counter-perspectives on a regular basis. Playful, not preachy.
- **Realist:** Test environment based on an existing open-source recommender framework (e.g. a simple content-based or collaborative-filtering sample project), fed with a small, self-assembled example dataset (articles/posts with roughly labeled perspectives). Show two ranking modes side by side in the same Flask frontend: "Standard" (pure similarity, bubble-reinforcing) vs. "Diversity-aware" (deliberately mixes in topically related counter-perspectives).
- **Critic:** Open risks: (1) Where does a credible, non-trivial example dataset come from in the available time? (2) How objectively can "perspectives" even be labeled without introducing our own bias? (3) Will a demo with sample/synthetic data be convincing enough for peer feedback and the final presentation, or does it need real content? (4) Is the difference from "pleenum" clear enough to outsiders?

## Peer Feedback (12:45), talking points

> [!warning] Update von der Orga
> Zeit auf 12:45 verschoben (vorher 11:30). Pitch an 3-4 andere Gruppen. Raumliste nennt Team 13 zweimal (Raum 217 bei Marius und Raum 127 bei Heiko), das vor Ort unbedingt gegenchecken.

- **Core problem:** "For You" feeds reinforce filter bubbles. Some don't notice it (Mia), some notice but can't escape it (Tom).
- **Target group:** young adults (18–25) who mainly consume political/societal content through algorithmic feeds.
- **Solution idea:** a recommender test environment showing two feed variants side by side (bubble-reinforcing vs. diversity-aware), built on an existing framework.
- **Key features for the prototype:**
  - Two feed modes shown side by side in the same interface: "Standard" (pure similarity) vs. "Diversity-aware" (deliberately mixes in topically related counter-perspectives)
  - Built on an existing open-source recommender framework, no self-trained ML model
  - Small example dataset with roughly labeled perspectives/topics
  - Simple Flask web frontend to switch between/compare both modes directly
  - Optional (if time allows): visible marking of which posts were deliberately mixed in as counter-perspectives in the diversity-aware mode
- **Question for other groups:** do you know similar approaches/tools? How would you measure "varied but still relevant"?

## Still open after the live session

- [ ] Critical issues (5–10) confirmed/adjusted by the team, transferred to `Critical_Issues.pdf`
- [ ] One or both problem statements finalized
- [ ] Walt-Disney (or 6-3-5) round actually run with the team, outcome documented here
- [ ] Peer feedback results (12:45) captured
- [ ] Team Board card updated with today's status
- [ ] Facilitator role (open since Tuesday) resolved
- [ ] Example dataset for the recommender demo decided
- [ ] Room for peer feedback confirmed on-site (217 vs. 127)
