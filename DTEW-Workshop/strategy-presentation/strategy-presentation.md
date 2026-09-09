# Strategy Presentation, Team 13, DTEW Hamburg 2026

**Case 3:** Feed and recommender design against filter-bubble reinforcement (digi&demo e.V.).

Working product title: **"Perspective Compass"** (working title only, final name and logo are still a team decision).

> Draft consolidated ahead of the final presentation (10./11.09.). It pulls together the material already prepared during the workshop: problem and personas (Tuesday 01.09.), critical issues and problem statements (Wednesday 02.09.), Social Business Model Canvas, marketing strategy and onboarding concept (Friday 04.09., see [[DTEW 0409 - Social Business Model Canvas, Marketing und Onboarding]]), and the current prototype state (see [`Code/feed-diversity-prototype/README.md`](../../Code/feed-diversity-prototype/README.md)). The team still needs to trim this into the 1-minute pitch and design the stand poster/flyer separately.

The slide order below follows the structure from the "Final presentation" input (`Presenting prototypes_DTEW2026HH.pdf`, main board): problem/why, customer, solution/how, business model, team.

---

## Slide 1, Title

- **Team 13, BHH** (Felix, Erik, Dogan), International Design Thinking & Entrepreneurship Workshop Hamburg, 31.08.–12.09.2026
- **Case 3:** how can a recommender inform users in a way that is varied but still topically relevant, instead of reinforcing bubbles?
- Working title "Perspective Compass" (name and logo to be finalised by the team)

---

## Slide 2, The problem (the Why)

- "For You" feeds on the big platforms are optimised for engagement, not for a balanced picture. That reinforces filter bubbles and self-selected echo chambers.
- Two different failure modes in the same target group:
  - Some users do not notice they are in a bubble and consider their feed balanced.
  - Others do notice, try to break out, and the algorithm keeps pulling them back to similar content.
- Why it matters: reduced exposure to diverse but relevant perspectives weakens healthy democratic discourse. This is the core concern of digi&demo e.V. (their project "pleenum").

---

## Slide 3, Who it is for

- **Primary:** young adults (18–25) who consume political and societal content mainly through algorithmic feeds (Instagram, TikTok, X).
- **Persona "Mia", 20, "The Everyperson":** checks Instagram and TikTok many times a day, mostly follows accounts that match her views, sees herself as informed, does not connect the occasional surprise at a friend's opinion to her feed. Needs the bubble made visible without having to look for it.
- **Persona "Tom", 22, "The Seeker":** more media-literate, follows a few accounts on purpose to diversify, feels like he is fighting the algorithm. Needs a tool that reliably supplies topically relevant counter-perspectives without flooding him with irrelevant content.
- **Secondary:** educators, associations and initiatives (digi&demo e.V., "Netz Macht Politik") who could use the tool as demonstration and media-literacy material.
- Personas are a target-group description, not validated by interviews yet (see [`personas-mia-tom/`](../personas-mia-tom/personas-mia-tom.md)).

---

## Slide 4, The solution (the How)

One feed, two switchable modes in the same web frontend (Flask, classic content-based filtering with TF-IDF and cosine similarity, no self-trained ML model):

- **Standard mode:** bubble-reinforcing, like a typical "For You" feed. For a logged-in account it also reads the like history: the majority perspective of everything the account has liked so far steers the feed, so it self-reinforces with every further like, on purpose without a built-in way out. That is the key demo scene.
- **Diversity-aware mode:** same similarity basis, but every few positions it deliberately mixes in the closest post with the same topic and the opposing perspective, marked as "Suggested", and uses the same account tendency to break it rather than confirm it.
- **Two independent axes made visible:** pro/contra perspective on the topic, plus a self-declared political label (left/centre/right). The label is chosen by the author, not guessed by the app, which is itself a transparency argument.
- **Visible diversity score** per feed view, an answer to the "we need a metric" critical issue from Wednesday.
- **Real accounts, likes and comments** (Supabase Auth and Postgres), plus a read-only section showing public Mastodon posts on the current topic (no ActivityPub server of our own).

---

## Slide 5, What we deliberately left out

- No self-trained ML recommender. Classic content-based filtering is enough for the core question and realistic in two weeks without ML experience in the team.
- No automatic left/right classifier. Reliable political classification from free text is an unsolved, contested problem, and an app that silently claims "this is objectively left" would reproduce exactly the kind of invisible algorithmic judgement the case is about. Users self-label instead.
- Not a replacement for anyone's TikTok or Instagram feed. It is a standalone demonstrator that shows the mechanism.
- No full ActivityPub implementation (own actor, WebFinger, HTTP signatures). The Fediverse section is read-only via Mastodon's public API. A full client/server stays a concept sketch (feasibility note in the vault).

---

## Slide 6, Onboarding concept

Four steps, built so the user feels the bubble before the fix is named (important for "Mia" types who do not see the problem):

1. **Topic selection:** the user picks 2–3 topics from the curated example set to create a realistic starting feed.
2. **Standard feed first:** the "Standard" mode without any explanation, so the bubble effect is experienced rather than described.
3. **Perspective compass:** after a little interaction, a simple visualisation of how one-sided the feed has been so far (the diversity metric).
4. **Diversity mode offered:** only then the switch to "Diversity-aware", with visible marking of which posts were mixed in as counter-perspectives.

---

## Slide 7, Positioning and marketing strategy

- **Positioning:** not "another social media app" but a transparency and media-literacy tool. It shows the difference between bubble-reinforcing and diversity-aware ranking side by side instead of just claiming to be fair.
- **Core message:** "Your feed helps decide which opinions you see. We show you how, and what a fairer feed could look like instead."
- **Persona-split messaging:**
  - For "Mia" types: low-threshold and curiosity-driven ("test how one-sided your feed really is"), not lecturing.
  - For "Tom" types: concrete and tool-oriented ("finally a feed that does not pull you back").
- **Channels and reach:** digi&demo e.V. and their "pleenum" community as the first topically fitting multiplier, the "Netz Macht Politik" / Bürgerhaus Wilhelmsburg network, and the workshop's own visibility (Innovation Fair 10./11.09., blog post on designentrepreneurshipworkshop.org, market stand).
- **Honest reach framing:** the prototype is currently a standalone demo. Marketing promises "shows the mechanism", not "replaces your feed".

---

## Slide 8, Social Business Model Canvas (condensed)

- **Value proposition:** a feed comparison tool that makes visible how strongly a ranking algorithm reinforces your own bubble, and shows an alternative that stays topically relevant. Solves the visibility problem for Mia and the break-out problem for Tom.
- **Beneficiaries:** primary young adults (18–25) with mostly algorithmic news consumption, secondary educational institutions and associations such as digi&demo e.V.
- **Channels:** direct via digi&demo e.V., the Bürgerhaus action-day network, the workshop's own channels (Innovation Fair, blog post, market stand).
- **Customer relationship:** open and explanatory rather than engagement-optimising. Transparency as the core promise: it actively shows what the algorithm does instead of hiding it.
- **Key activities:** curating and labelling the example dataset, maintaining the two ranking modes, developing the comparison frontend, outreach and teaching.
- **Key resources:** the Flask stack and team know-how from the Pi-Dashboard project, the curated example dataset, the contact to digi&demo e.V.
- **Key partners:** digi&demo e.V. (content, expertise, reach), possibly Bürgerhaus Wilhelmsburg / "Netz Macht Politik" as a multiplier, the workshop organisation (ITECH-BS14) as the first test context.
- **Cost structure:** development time (unpaid within the workshop), hosting for a later demo version, dataset upkeep for long-term operation.
- **Funding:** no direct revenue planned for the prototype (non-profit and awareness character). For a real continuation: funding through digi&demo e.V. or similar media-literacy initiatives, or licensing the comparison logic to open platforms (Bluesky custom feeds).
- **Social impact:** makes filter-bubble mechanisms visible to a group that otherwise does not notice them (Mia), and gives the other group a concrete tool to break out (Tom). Contributes to media literacy and digital participation, in line with the digi&demo mission.

---

## Slide 9, Competition and differentiation

- **digi&demo e.V. "pleenum":** focuses on discourse format and moderation. We focus on the feed ranking itself. Communicate as a complement, not a competitor.
- **Community-Notes-style and "bridging" recommender experiments:** adjacent research direction. Our niche is making the mechanism visible plus offering a switchable alternative in the same interface.
- **Big platforms:** optimise for engagement by design. We deliberately show the opposite and make that legible.

---

## Slide 10, Roadmap and next steps

- **Near term:** apply the political-label migration against the live database, seed demo accounts with opposing like histories for the demo, verify the Fediverse section against the real Mastodon API, add a diversity-over-time view.
- **Medium term:** pilot with digi&demo e.V. as teaching and demonstration material, gather real user feedback, decide on a final name and visual identity.
- **Longer term:** explore integration as a Bluesky custom feed so the diversity-aware ranking can run on a real platform instead of only in the demo.

---

## Slide 11, The team

- **Team 13, BHH:** Felix, Erik, Dogan.
- Roles (Scrum Master, Product Owner) to be finalised and entered on the team board.
- "An A-team with a B-idea is better than a B-team with an A-idea." Everyone is involved in the presentation.

---

## Slide 12, Open decisions (team, not in this deck)

- Final product name and logo.
- The 1-minute pitch script (10./11.09., Room 23, no slides).
- Stand budget and material (poster, flyer) for the Innovation Fair.
- Final role assignment and the retrospective.
