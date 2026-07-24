"use strict";

const assert = require("assert");
const {
  buildSessionId,
  buildTurnNote,
  extractPublicOutput,
  nextNumericTurn,
  parseFrontmatter,
  parseTurnDraft,
  requireSafeComponent,
} = require("../.obsidian/plugins/holodeck-control/core");

const fixedDate = new Date(2026, 6, 23, 21, 7);
assert.strictEqual(
  buildSessionId("Camille", "out_of_timeline", fixedDate),
  "hors-timeline-camille-20260723-2107"
);
assert.strictEqual(nextNumericTurn([]), "001");
assert.strictEqual(nextNumericTurn(["001", "002f", "010"]), "011");
assert.throws(() => requireSafeComponent("../escape", "session"));

const note = buildTurnNote({
  resident: "Camille",
  session: "hors-timeline-camille-test",
  turn: "001",
  program: "DPhen",
  timeline: "out_of_timeline",
  contextPack: "",
  speechRequired: false,
  scene: "Camille entre.",
  intervention: "Aucune.",
});
const metadata = parseFrontmatter(note);
assert.deepStrictEqual(metadata, {
  resident: "Camille",
  session: "hors-timeline-camille-test",
  turn: "001",
  program: "DPhen",
  timeline: "out_of_timeline",
  speech_required: "false",
});
assert.match(note, /## Scene observable\n\nCamille entre\./);
assert.match(note, /## Intervention publique\n\nAucune\./);
assert.deepStrictEqual(parseTurnDraft(note), {
  scene: "Camille entre.",
  intervention: "Aucune.",
  speechRequired: false,
});

assert.strictEqual(
  extractPublicOutput(
    "*Camille attend.*\n\n**Camille :** « Bonjour. »\n\nPublic : C:\\test\\public.md"
  ),
  "*Camille attend.*\n\n**Camille :** « Bonjour. »"
);

console.log("Holodeck Control core tests: OK");
