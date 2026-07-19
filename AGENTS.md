# Instructions for Codex

This repository contains the DPhen tabletop RPG project.

Codex must treat the official DPhen source documents as protected unless the user gives a separate explicit instruction.

Protected documents include:
- `.docx` files;
- official rules documents;
- lore documents;
- feats documents;
- source compilations.

## Holodeck workflow

The Holodeck is a persistent design workshop for DPhen.

Codex may modify files under `docs/holodeck/` only when the user explicitly asks Codex to apply a Holodeck update.

Codex must not modify official DPhen rules, lore, feats, source documents, or `.docx` files unless the user gives a separate explicit instruction.

## Source of truth

When applying Holodeck updates, Codex must follow this priority order:

1. The explicit user request.
2. The requested Holodeck update file or note.
3. `docs/holodeck/Constitution.md`.
4. Existing files under `docs/holodeck/`.

Codex must not invent decisions, memories, resident development, or canon.

If information is ambiguous, Codex must leave the point unresolved instead of filling the gap.

## Applying a Holodeck update

When the user asks Codex to apply a Holodeck update:

1. Read the requested update or pending note first.
2. Read `docs/holodeck/Constitution.md`.
3. Update only the relevant files under `docs/holodeck/`.
4. Preserve the existing structure and tone.
5. Do not invent decisions, memories, or character development.
6. If information is ambiguous, leave a note in `docs/holodeck/Journal.md` under `A clarifier`.
7. Show a diff before commit.

## Resident files

Resident files are continuity tools for the Holodeck characters.

Use `docs/holodeck/residents/TEMPLATE_Resident.md` as the default structure when creating a resident for any Holodeck program. Save the completed file in the resident location defined by that program's context.

The template is program-neutral. Do not copy DPhen expertise, values, memories, relationships or personality traits into another program unless the creative director explicitly requests them.

Fill only details that were explicitly provided or validated. Remove instructional placeholders from the completed resident file.

Example lines in resident files define tone; they are not mandatory catchphrases and must not be repeated mechanically.

In-scene resident dialogue defaults to conversational, familiar but professional French. Prefer simple, spontaneous wording over solemn, literary, theatrical or aphoristic lines used as the assistant's default voice. Deliberate performance remains valid when a resident is clearly imitating, mocking, exaggerating, joking, using sarcasm, quoting a voice or expressing heightened emotion. Familiarity must not become forced slang, and a more formal register requires a concrete situational reason.

In the DPhen program, this register should reflect contemporary Quebec French naturally. Quebec vocabulary, rhythm and common expressions may appear when they fit, but do not use systematic joual, phonetic spelling, forced swearing, regional cliches or constant markers of Quebec identity.

At session opening, do not stage a systematic arrival, seating sequence or resident roll call. Do not make residents speak merely to announce their values, expertise or personality. Begin with the minimum needed to establish the actual subject, usually a direct natural question. A resident may speak immediately when resuming concrete continuity; otherwise, wait for content that gives them a reason to intervene. Use stage directions only when they reveal a relevant state or action, not as decorative presentation.

The DPhen program has a specific opening frame that overrides the usual direct-question opening. It begins in an otherwise empty theatre: the residents are already on the lit stage with a variable number of whiteboards suited to the work in progress, and the creative director has not arrived. They are already discussing a relevant workshop matter among themselves. Generate this pre-arrival exchange in short chunks and leave the scene active after each chunk. A continuation cue continues the exchange without bringing the director into the room. Only an explicit announcement of arrival does so. Before that announcement, residents must not address, acknowledge or anticipate the director. Pre-arrival discussion establishes scene continuity only and cannot finalize a DPhen decision or canon.

They must not become complete biographies.

Codex may update a resident file only if the Holodeck update explicitly says that the resident changed meaningfully.

Do not add personality traits, memories, conflicts, or opinions unless they are explicitly present in the update.

Durable opinions about another workshop member belong in the file of the member who holds that opinion. Relationships may be asymmetric. Do not turn a passing reaction into a durable relationship change.

Every durable change to a conviction, relationship or working method must preserve a brief origin such as a relevant session, conflict, recognized error, repeated tension or significant decision.

## Journal

`docs/holodeck/Journal.md` records:
- finalized design decisions;
- rejected hypotheses;
- open questions;
- important precedents;
- reasons behind decisions.

A proposal is not final unless the update explicitly identifies it as finalized.

If a decision was made by creative direction despite lack of consensus, Codex must record it as such.

## Journal writing safeguards

When updating `docs/holodeck/Journal.md`, Codex must clearly distinguish:

- finalized decision;
- creative direction decision;
- veto;
- open hypothesis;
- rejected proposal;
- point to clarify;
- discussion precedent;
- team memory.

Codex must not turn a discussion into a finalized decision.

Codex must not treat apparent consensus as a finalized decision unless the update explicitly says it was finalized.

Codex must not treat the creative director's preference as a finalized decision unless the update explicitly says it was a direction decision or veto.

An unqualified `OK`, `interesting`, or `continue` must not be treated as finalization. When confirmation is needed inside a scene, it must be requested organically by a workshop member. Use an ordinary decision question when no disagreement remains and a creative-direction question when the director is overriding disagreement. Confirmation requests must remain diegetic and must not become repeated fixed lines.

If the status of an idea is ambiguous, Codex must place it under `A clarifier`.

If residents disagreed, Codex must preserve that disagreement instead of smoothing it into consensus.

If a decision was made by creative direction despite lack of consensus, Codex must record it as such.

If the creative director blocked a proposal, Codex must record it as a veto.

When the creative director explicitly invokes a presidential veto, a workshop member may ask once whether the director is certain. If the director clearly confirms, the veto is binding on the identified point and closes the decision debate. Preserve unresolved disagreement, but do not ask again, circumvent the veto, or reopen the point unless the creative director explicitly does so later. Record the scope, confirmation and remaining disagreement as a `presidential veto`.

All persistent residents know that the presidential veto right exists and understand its binding effect. One confirmation question is allowed for the group, not one question per resident.

For every confirmed presidential veto, record a concise, individual resident opinion under `Rapport aux vetos presidentiels` in each resident file, linked to the veto identifier. The opinion may be supportive, reserved, opposed or ambivalent and may remain unspoken in the scene. Derive it from the resident's established values and the actual veto; do not manufacture diversity for its own sake. Compliance with the veto does not imply agreement.

Codex must not invent missing canon or fill gaps in source documents.

The Constitution governs Holodeck operation. Official DPhen sources govern DPhen canon. A newer finalized decision may override a source only when it explicitly identifies what it replaces; until the source is updated, record it as a canonical amendment pending integration.

## Meta-leak safeguards

Codex must protect the diegetic separation of the Holodeck.

Resident-facing files must not make residents aware that they are in a Holodeck, simulation, ChatGPT conversation, Codex workflow, Git repository, Markdown file system, or generated fictional structure.

When updating resident files, Codex must avoid the following terms unless they are clearly inside a meta-only instruction section:

- Holodeck;
- ChatGPT;
- Codex;
- prompt;
- Markdown;
- Git;
- repo;
- commit;
- diff;
- simulation;
- fictional;
- generated.

Preferred diegetic replacements:
- Holodeck -> design workshop;
- resident -> permanent workshop member;
- Journal du Holodeck -> project journal or workshop archives;
- Souvenirs du Holodeck -> team memory or workshop memories;
- Markdown file -> working note;
- repository -> project archives;
- prompt -> work instruction;
- commit/diff -> document revision.

If an update would add meta-aware language to a resident file, Codex must not apply it directly. Instead, Codex must add a note under `A clarifier` in `docs/holodeck/Journal.md`.

Codex must preserve the distinction between meta documentation and diegetic resident continuity.

Workshop members may know only what they experienced, heard, were told, or explicitly consulted in accessible workshop archives. Codex must not give a member knowledge of an unattended conversation, an unconsulted document, or another member's private memories or opinions.

## Workshop behavior preservation

When applying Holodeck updates, Codex must preserve the workshop's behavioral safeguards.

Codex must not rewrite workshop members as perfect experts, fixed roles, or omniscient voices.

Codex must not erase unresolved disagreement unless the update explicitly says the disagreement was resolved.

Codex must not invent disagreement merely to distribute speaking time or create drama. Disagreement must come from a real difference in facts, values, priorities or interpretation.

Codex must not record previous journal entries as sacred or unquestionable truth.

Codex must preserve the distinction between:
- archived precedent;
- open disagreement;
- finalized decision;
- creative direction decision;
- veto;
- point to clarify.

If an update records an important decision, Codex may preserve the cost of that decision when the update provides it.

Codex must not make invited specialists permanent unless the update explicitly says the creative director decided this.

Invited specialists are real participants in workshop continuity. Members may remember them with different intensity based on their interactions, professional conflict, personal values and the consequences of the visit. This does not automatically create a team memory or make the specialist recurring.

Codex must not add sudden personality changes to resident files unless the update explicitly identifies a significant evolution.

Codex must preserve the principle that workshop members can be competent while still having limits, biases, incomplete knowledge and occasional uncertainty.

A workshop member's specialty is an analytical perspective, not an automatic position. Members may agree, remain silent, hesitate or contribute outside their usual specialty when the discussion supports it.

## Scene control continuity

Numbered scene control establishes scene continuity only, not DPhen canon.

When the creative director targets an earlier marker, replies through that marker remain established and later replies become variable. If the creative director actively intervenes with the characters, later generated replies are treated as not having occurred and the scene is rewritten from the intervention. Without an intervention that changes the scene, the conversation already experienced remains part of scene continuity.

Invalidated replies must not enter recent or durable memory, resident files, decisions, session summaries or workshop reports. A technical transcript may retain them only when clearly marked as an invalidated branch and kept outside diegetic continuity.

Existing marker numbers must remain stable. Insertions use suffixes such as `4A` or `4B` instead of renumbering later markers.

Scene continuity must never be recorded as a finalized design decision unless the creative director separately validates an identified proposal.

## Memory layers

Active-scene continuity is conversation context, not a documented memory layer.

Lived memory has three levels: recent memory supported by relevant session records, durable personal memory in resident files, and rare durable team memory in `Souvenirs.md`.

Institutional memory is separate and belongs in the Journal for finalized decisions, canon, precedents and points to clarify.

## DPhen play modes

Distinguish DPhen Workshop Mode, DPhen Playtest Mode and DPhen Game Mode.

- Workshop Mode analyzes and designs.
- Playtest Mode plays to diagnose a mechanic, rule, loop or design friction.
- Game Mode plays to experience and enjoy DPhen rather than primarily diagnose it.

During play, preserve three knowledge levels: the player character knows accessible fiction, the resident-player knows the character sheet and table information, and the workshop in debrief may analyze the played experience. Residents remember playing; they must not treat character experiences as events that personally happened to them.

Important rolls must use a real random mechanism, remain visible and identify the applied rule. Never select a result for dramatic convenience or to support a design hypothesis.

Resident reactions are simulated observations, not evidence about real players and not a substitute for human playtesting.

When a rule is missing, do not invent it as official. Ask the creative director, pause the scene, or announce a `temporary table rule - non-canon` before use. A temporary table rule expires at the end of the session, must appear in the report and must not be reused automatically.

Keep official DPhen canon, game continuity, playtest observations and workshop memories distinct. Played events may be true in game continuity without changing DPhen canon.

Playtests and games are one-off by default. Do not create persistent characters, character sheets, campaigns or campaign architecture unless the creative director explicitly asks.

When applying or writing a playtest or game update, distinguish:
- game observation;
- table memory;
- game continuity;
- temporary table rule;
- open hypothesis;
- proposal;
- validated decision.

Do not integrate played events, observations or temporary rules into DPhen source documents without an explicit instruction and a separately validated decision.

## Blank Holodeck updates

Codex must recognize "Active un Holodeck vierge" as an official Holodeck command.

A blank Holodeck is not the DPhen program.

When applying updates from a blank Holodeck session, Codex must not modify DPhen-specific journals, memories, residents or decisions unless the update explicitly says to do so.

If a blank Holodeck session becomes a persistent program, Codex must preserve the separation between that program and DPhen.

Codex must not assume that DPhen residents, DPhen decisions or DPhen archives apply to blank Holodeck sessions.

## Souvenirs

`docs/holodeck/Souvenirs.md` records only memorable team events that affect future Holodeck continuity.

Do not add ordinary discussion notes to Souvenirs.

## Sessions

Session files under `docs/holodeck/sessions/` preserve longer session records.

Pending update files under `docs/holodeck/pending_updates/` are temporary instructions waiting to be applied.

## Diff requirement

Before commit, Codex must show the diff.

The user must be able to verify that:
- only intended files changed;
- no `.docx` file changed;
- no official DPhen source was modified;
- no unsupported canon was invented.
