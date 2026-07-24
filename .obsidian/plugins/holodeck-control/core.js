"use strict";

const SAFE_COMPONENT = /^[A-Za-z0-9._-]+$/;

function requireSafeComponent(value, label = "valeur") {
  const normalized = String(value || "").trim();
  if (!normalized || !SAFE_COMPONENT.test(normalized)) {
    throw new Error(
      `${label} doit contenir seulement lettres ASCII, chiffres, point, tiret ou soulignement.`
    );
  }
  return normalized;
}

function slugify(value) {
  const slug = String(value || "")
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
  return slug || "resident";
}

function timestamp(date = new Date()) {
  const pad = (value) => String(value).padStart(2, "0");
  return [
    date.getFullYear(),
    pad(date.getMonth() + 1),
    pad(date.getDate()),
    "-",
    pad(date.getHours()),
    pad(date.getMinutes()),
  ].join("");
}

function buildSessionId(resident, timeline, date = new Date()) {
  const prefixes = {
    current: "session",
    out_of_timeline: "hors-timeline",
    locked: "contexte-verrouille",
  };
  const prefix = prefixes[timeline] || "session";
  return `${prefix}-${slugify(resident)}-${timestamp(date)}`;
}

function formatTurn(value) {
  return String(Number(value)).padStart(3, "0");
}

function nextNumericTurn(ids) {
  const numbers = (ids || [])
    .map((id) => String(id).match(/^(\d+)/))
    .filter(Boolean)
    .map((match) => Number(match[1]))
    .filter(Number.isFinite);
  return formatTurn((numbers.length ? Math.max(...numbers) : 0) + 1);
}

function parseFrontmatter(text) {
  const lines = String(text || "").split(/\r?\n/);
  if (lines[0] !== "---") return {};
  const result = {};
  for (let index = 1; index < lines.length; index += 1) {
    const line = lines[index];
    if (line === "---") break;
    const separator = line.indexOf(":");
    if (separator < 0) continue;
    const key = line.slice(0, separator).trim();
    const value = line
      .slice(separator + 1)
      .trim()
      .replace(/^['"]|['"]$/g, "");
    if (key) result[key] = value;
  }
  return result;
}

function readMarkdownSection(text, heading) {
  const source = String(text || "");
  const marker = `## ${heading}`;
  const markerIndex = source.indexOf(marker);
  if (markerIndex < 0) return "";
  const contentStart = source.indexOf("\n", markerIndex + marker.length);
  if (contentStart < 0) return "";
  const nextHeading = source.indexOf("\n## ", contentStart + 1);
  return source
    .slice(contentStart + 1, nextHeading < 0 ? source.length : nextHeading)
    .trim();
}

function parseTurnDraft(text) {
  const metadata = parseFrontmatter(text);
  return {
    scene: readMarkdownSection(text, "Scene observable"),
    intervention: readMarkdownSection(text, "Intervention publique"),
    speechRequired: metadata.speech_required !== "false",
  };
}

function buildTurnNote({
  resident,
  session,
  turn,
  program,
  timeline,
  contextPack,
  speechRequired,
  scene,
  intervention,
}) {
  const lines = [
    "---",
    `resident: ${requireSafeComponent(resident, "resident")}`,
    `session: ${requireSafeComponent(session, "session")}`,
    `turn: ${requireSafeComponent(turn, "turn")}`,
    `program: ${requireSafeComponent(program, "program")}`,
    `timeline: ${requireSafeComponent(timeline, "timeline")}`,
  ];
  if (contextPack) {
    lines.push(
      `context_pack: ${requireSafeComponent(contextPack, "context_pack")}`
    );
  }
  lines.push(
    `speech_required: ${speechRequired ? "true" : "false"}`,
    "---",
    "",
    `# Tour ${turn} - ${resident}`,
    "",
    "## Scene observable",
    "",
    String(scene || "").trim() || "Aucun changement observable.",
    "",
    "## Intervention publique",
    "",
    String(intervention || "").trim() || "Aucune.",
    ""
  );
  return lines.join("\n");
}

function extractPublicOutput(stdout) {
  return String(stdout || "")
    .split(/\r?\nPublic\s*:/, 1)[0]
    .trim();
}

module.exports = {
  buildSessionId,
  buildTurnNote,
  extractPublicOutput,
  formatTurn,
  nextNumericTurn,
  parseFrontmatter,
  parseTurnDraft,
  requireSafeComponent,
  slugify,
  timestamp,
};
