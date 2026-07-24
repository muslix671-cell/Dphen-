"use strict";

const {
  FileSystemAdapter,
  ItemView,
  MarkdownRenderer,
  Modal,
  Notice,
  Plugin,
  PluginSettingTab,
  Setting,
  TFile,
  normalizePath,
  setIcon,
} = require("obsidian");
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

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
  return `${prefixes[timeline] || "session"}-${slugify(resident)}-${timestamp(
    date
  )}`;
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

const VIEW_TYPE = "holodeck-control-view";
const RUNTIME_ROOT = "docs/holodeck/meta/engine/runtime";
const DEFAULT_SETTINGS = {
  currentSession: "",
  resident: "Camille",
  program: "DPhen",
  timeline: "out_of_timeline",
  contextPack: "",
  reasoningEffort: "medium",
  pythonPath: "",
  openPublicAfterRun: false,
};

function addIconButton(parent, icon, label, onClick, className = "") {
  const button = parent.createEl("button", {
    cls: `holodeck-icon-button ${className}`.trim(),
    attr: { "aria-label": label, title: label },
  });
  setIcon(button, icon);
  button.addEventListener("click", onClick);
  return button;
}

function addLabeledButton(parent, icon, label, className = "") {
  const button = parent.createEl("button", {
    cls: className,
    attr: { "aria-label": label },
  });
  const iconEl = button.createSpan({ cls: "holodeck-button-icon" });
  setIcon(iconEl, icon);
  button.createSpan({ text: label });
  return button;
}

class ConfirmReplaceModal extends Modal {
  constructor(app, turnId, onConfirm) {
    super(app);
    this.turnId = turnId;
    this.onConfirm = onConfirm;
  }

  onOpen() {
    const { contentEl } = this;
    this.setTitle(`Remplacer le tour ${this.turnId}`);
    contentEl.createEl("p", {
      text:
        "L’ancien résultat sera archivé, puis la session reviendra à l’état " +
        "qui précédait ce tour. La scène et l’intervention seront replacées " +
        "dans les champs.",
    });

    new Setting(contentEl)
      .addButton((button) => {
        button.setButtonText("Annuler").onClick(() => this.close());
      })
      .addButton((button) => {
        button
          .setButtonText("Remplacer le tour")
          .setWarning()
          .onClick(async () => {
            this.close();
            await this.onConfirm();
          });
      });
  }

  onClose() {
    this.contentEl.empty();
  }
}

class SceneAdjustmentModal extends Modal {
  constructor(app, onSave) {
    super(app);
    this.onSave = onSave;
  }

  onOpen() {
    const { contentEl } = this;
    this.setTitle("Ajuster la scène");
    contentEl.createEl("p", {
      text:
        "Ajoute un fait qui était déjà vrai dans la scène. Cet ajustement " +
        "ne fait réagir personne et n’avance pas le tour.",
    });
    const input = contentEl.createEl("textarea", {
      cls: "holodeck-adjustment-textarea",
      attr: {
        rows: "6",
        placeholder:
          "Deux tableaux blancs se trouvent derrière la causeuse...",
      },
    });

    new Setting(contentEl)
      .addButton((button) => {
        button.setButtonText("Annuler").onClick(() => this.close());
      })
      .addButton((button) => {
        button
          .setButtonText("Enregistrer l’ajustement")
          .setCta()
          .onClick(async () => {
            const text = input.value.trim();
            if (!text) {
              new Notice("Décris d’abord l’ajustement de scène.");
              return;
            }
            this.close();
            await this.onSave(text);
          });
      });
  }

  onClose() {
    this.contentEl.empty();
  }
}

class HolodeckControlView extends ItemView {
  constructor(leaf, plugin) {
    super(leaf);
    this.plugin = plugin;
    this.draftScene = "";
    this.draftIntervention = "";
    this.sceneQuestion = "";
    this.sceneAnswer = "";
    this.sceneCertainty = "";
    this.sceneToolsOpen = false;
    this.lastOutput = "";
    this.statusMessage = "";
    this.statusKind = "idle";
    this.runningProcess = null;
    this.elapsedTimer = null;
    this.startedAt = 0;
    this.speechRequired = true;
    this.resources = {
      residents: [],
      programs: [],
      contextPacks: [],
      sessions: [],
    };
  }

  getViewType() {
    return VIEW_TYPE;
  }

  getDisplayText() {
    return "Holodeck";
  }

  getIcon() {
    return "theater";
  }

  async onOpen() {
    await this.refreshResources();
    if (this.currentSession) {
      await this.restorePendingDraft(this.currentSession);
      this.lastOutput = await this.readLatestPublicOutput(this.currentSession);
    }
    await this.render();
  }

  async onClose() {
    this.clearElapsedTimer();
  }

  get vaultRoot() {
    const adapter = this.app.vault.adapter;
    if (!(adapter instanceof FileSystemAdapter)) {
      throw new Error("Holodeck Control exige un coffre Obsidian local.");
    }
    return adapter.getBasePath();
  }

  get currentSession() {
    return this.plugin.settings.currentSession;
  }

  async refreshResources() {
    const files = this.app.vault.getMarkdownFiles();
    const calibrations = new Set(
      files
        .filter((file) =>
          file.path.startsWith("docs/holodeck/meta/resident_calibrations/")
        )
        .map((file) => file.basename)
    );
    this.resources.residents = files
      .filter((file) => {
        return (
          file.path.startsWith("docs/holodeck/residents/") &&
          file.parent?.path === "docs/holodeck/residents" &&
          !file.basename.startsWith("TEMPLATE") &&
          calibrations.has(file.basename)
        );
      })
      .map((file) => file.basename)
      .sort((a, b) => a.localeCompare(b, "fr"));

    this.resources.programs = files
      .filter(
        (file) =>
          file.parent?.path === "docs/holodeck/contexts" &&
          !file.basename.startsWith("TEMPLATE")
      )
      .map((file) => file.basename)
      .sort((a, b) => a.localeCompare(b, "fr"));

    const packRoot = "docs/holodeck/meta/engine/context_packs";
    this.resources.contextPacks = [];
    if (await this.app.vault.adapter.exists(packRoot)) {
      const listing = await this.app.vault.adapter.list(packRoot);
      this.resources.contextPacks = listing.folders
        .map((folder) => folder.split("/").pop())
        .filter(Boolean)
        .sort((a, b) => a.localeCompare(b, "fr"));
    }

    this.resources.sessions = [];
    if (await this.app.vault.adapter.exists(RUNTIME_ROOT)) {
      const listing = await this.app.vault.adapter.list(RUNTIME_ROOT);
      this.resources.sessions = listing.folders
        .map((folder) => folder.split("/").pop())
        .filter(Boolean)
        .sort((a, b) => b.localeCompare(a, "fr"));
    }

    if (
      !this.resources.residents.includes(this.plugin.settings.resident) &&
      this.resources.residents.length
    ) {
      this.plugin.settings.resident = this.resources.residents[0];
    }
    if (
      !this.resources.programs.includes(this.plugin.settings.program) &&
      this.resources.programs.length
    ) {
      this.plugin.settings.program = this.resources.programs[0];
    }
  }

  compatibleContextPacks() {
    const resident = this.plugin.settings.resident.toLowerCase();
    return this.resources.contextPacks.filter((pack) =>
      pack.toLowerCase().startsWith(resident)
    );
  }

  setStatus(message, kind = "idle") {
    this.statusMessage = message;
    this.statusKind = kind;
  }

  async render() {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.addClass("holodeck-control");

    const header = contentEl.createDiv({ cls: "holodeck-header" });
    const titleWrap = header.createDiv({ cls: "holodeck-title-wrap" });
    const titleIcon = titleWrap.createSpan({ cls: "holodeck-title-icon" });
    setIcon(titleIcon, "theater");
    titleWrap.createEl("h2", { text: "Holodeck" });
    addIconButton(header, "refresh-cw", "Actualiser", async () => {
      await this.refreshResources();
      await this.render();
    });

    const subtitle = contentEl.createEl("p", {
      cls: "holodeck-subtitle",
      text: "Entrevues locales, timelines isolées et sorties opérateur.",
    });
    subtitle.setAttr("aria-live", "polite");

    if (this.currentSession) {
      await this.renderActiveSession(contentEl);
      return;
    }

    this.renderNewSession(contentEl);
    await this.renderResume(contentEl);
  }

  renderNewSession(parent) {
    const section = parent.createDiv({ cls: "holodeck-section" });
    section.createEl("h3", { text: "Nouvelle entrevue" });

    new Setting(section)
      .setName("Résident")
      .setDesc("Seuls les résidents possédant une calibration peuvent être lancés.")
      .addDropdown((dropdown) => {
        for (const resident of this.resources.residents) {
          dropdown.addOption(resident, resident);
        }
        dropdown.setValue(this.plugin.settings.resident);
        dropdown.onChange(async (value) => {
          this.plugin.settings.resident = value;
          this.plugin.settings.contextPack = "";
          await this.plugin.saveSettings();
          await this.render();
        });
      });

    new Setting(section)
      .setName("Programme")
      .addDropdown((dropdown) => {
        for (const program of this.resources.programs) {
          dropdown.addOption(program, program);
        }
        dropdown.setValue(this.plugin.settings.program);
        dropdown.onChange(async (value) => {
          this.plugin.settings.program = value;
          await this.plugin.saveSettings();
        });
      });

    new Setting(section)
      .setName("Point de départ")
      .setDesc(
        "Aucune sortie du moteur ne devient canon automatiquement, peu importe ce choix."
      )
      .addDropdown((dropdown) => {
        dropdown
          .addOption("current", "Continuité actuelle")
          .addOption("out_of_timeline", "Hors timeline")
          .addOption("locked", "Contexte verrouillé");
        dropdown.setValue(this.plugin.settings.timeline);
        dropdown.onChange(async (value) => {
          this.plugin.settings.timeline = value;
          if (value !== "locked") this.plugin.settings.contextPack = "";
          await this.plugin.saveSettings();
          await this.render();
        });
      });

    if (this.plugin.settings.timeline === "locked") {
      const compatible = this.compatibleContextPacks();
      new Setting(section)
        .setName("Contexte verrouillé")
        .setDesc("Le dossier temporel chargé à la place du dossier cumulatif.")
        .addDropdown((dropdown) => {
          dropdown.addOption("", "Choisir...");
          for (const pack of compatible) dropdown.addOption(pack, pack);
          dropdown.setValue(this.plugin.settings.contextPack);
          dropdown.onChange(async (value) => {
            this.plugin.settings.contextPack = value;
            await this.plugin.saveSettings();
          });
        });
    }

    const suggested = buildSessionId(
      this.plugin.settings.resident,
      this.plugin.settings.timeline
    );
    let sessionInput = null;
    new Setting(section)
      .setName("Identifiant")
      .setDesc("Créé localement sous runtime; il ne modifie pas la continuité.")
      .addText((text) => {
        text.setValue(suggested);
        text.inputEl.addClass("holodeck-session-input");
        sessionInput = text.inputEl;
      });

    new Setting(section).addButton((button) => {
      button
        .setButtonText("Créer l’entrevue")
        .setCta()
        .setIcon("plus")
        .onClick(async () => {
          const sessionId = sessionInput?.value.trim() || suggested;
          await this.createSession(sessionId);
        });
    });
  }

  async renderResume(parent) {
    const section = parent.createDiv({ cls: "holodeck-section" });
    section.createEl("h3", { text: "Reprendre" });

    if (!this.resources.sessions.length) {
      section.createEl("p", {
        cls: "holodeck-muted",
        text: "Aucune session locale trouvée.",
      });
      return;
    }

    let selected = this.currentSession || this.resources.sessions[0];
    new Setting(section)
      .setName("Session locale")
      .addDropdown((dropdown) => {
        for (const session of this.resources.sessions) {
          dropdown.addOption(session, session);
        }
        dropdown.setValue(selected);
        dropdown.onChange((value) => {
          selected = value;
        });
      })
      .addButton((button) => {
        button
          .setButtonText("Reprendre")
          .setIcon("folder-open")
          .onClick(async () => {
            await this.resumeSession(selected);
          });
      });
  }

  async renderActiveSession(parent) {
    if (!this.currentSession) return;

    const metadata = await this.loadSessionMetadata(this.currentSession);
    const section = parent.createDiv({
      cls: "holodeck-section holodeck-active",
    });
    const heading = section.createDiv({ cls: "holodeck-active-heading" });
    heading.createEl("h3", { text: "Tour actif" });
    heading.createEl("code", { text: metadata.nextTurn });

    section.createEl("p", {
      cls: "holodeck-session-name",
      text: this.currentSession,
    });

    const contextLine = section.createEl("p", { cls: "holodeck-muted" });
    contextLine.setText(
      `${metadata.resident} · ${metadata.program} · ${this.timelineLabel(
        metadata.timeline
      )}`
    );

    if (this.lastOutput) {
      const output = section.createDiv({ cls: "holodeck-output" });
      const outputHeading = output.createDiv({
        cls: "holodeck-output-heading",
      });
      outputHeading.createEl("h4", { text: "Dernière réponse publique" });
      addIconButton(
        outputHeading,
        "copy",
        "Copier la réponse publique",
        async () => {
          try {
            await navigator.clipboard.writeText(this.lastOutput);
            new Notice("Réponse publique copiée.");
          } catch (error) {
            new Notice(
              `Impossible de copier la réponse : ${error.message || error}`,
              6000
            );
          }
        }
      );
      const rendered = output.createDiv({ cls: "holodeck-output-body" });
      await MarkdownRenderer.render(
        this.app,
        this.lastOutput,
        rendered,
        `${RUNTIME_ROOT}/${this.currentSession}/public.md`,
        this
      );

      const sceneTools = section.createEl("details", {
        cls: "holodeck-scene-tools",
      });
      sceneTools.open = this.sceneToolsOpen;
      sceneTools.createEl("summary", { text: "Outils de scène" });
      sceneTools.addEventListener("toggle", () => {
        this.sceneToolsOpen = sceneTools.open;
      });
      const sceneToolsBody = sceneTools.createDiv({
        cls: "holodeck-scene-tools-body",
      });
      const query = sceneToolsBody.createDiv({
        cls: "holodeck-scene-query",
      });
      const queryLabel = query.createEl("label", {
        cls: "holodeck-field-label",
        text: "Question sur la scène",
      });
      const queryRow = query.createDiv({ cls: "holodeck-scene-query-row" });
      const queryInput = queryRow.createEl("input", {
        cls: "holodeck-scene-query-input",
        attr: {
          type: "text",
          placeholder: "Où est Camille et dans quelle position?",
        },
      });
      queryInput.value = this.sceneQuestion;
      queryLabel.htmlFor = "holodeck-scene-query";
      queryInput.id = "holodeck-scene-query";
      queryInput.addEventListener("input", () => {
        this.sceneQuestion = queryInput.value;
      });
      const askButton = addIconButton(
        queryRow,
        "search",
        "Interroger la scène",
        async () => this.askSceneQuestion()
      );
      askButton.disabled = Boolean(this.runningProcess);
      const toolActions = query.createDiv({
        cls: "holodeck-scene-tool-actions",
      });
      const adjustButton = addLabeledButton(
        toolActions,
        "pencil",
        "Ajuster la scène"
      );
      adjustButton.disabled = Boolean(this.runningProcess);
      adjustButton.addEventListener("click", () => {
        new SceneAdjustmentModal(
          this.app,
          async (text) => this.addSceneAdjustment(text)
        ).open();
      });
      queryInput.addEventListener("keydown", async (event) => {
        if (event.key !== "Enter" || event.shiftKey) return;
        event.preventDefault();
        await this.askSceneQuestion();
      });

      if (this.sceneAnswer) {
        const answer = query.createDiv({
          cls: "holodeck-scene-query-answer",
        });
        const certaintyLabel =
          {
            established: "Établi",
            partially_inferred: "Partiellement déduit",
            unknown: "Indéterminé",
          }[this.sceneCertainty] || "";
        if (certaintyLabel) {
          answer.createSpan({
            cls: `holodeck-scene-certainty is-${this.sceneCertainty}`,
            text: certaintyLabel,
          });
        }
        answer.createEl("p", { text: this.sceneAnswer });
      }
    }

    const sceneLabel = section.createEl("label", {
      cls: "holodeck-field-label",
      text: "Scène observable",
    });
    const scene = section.createEl("textarea", {
      cls: "holodeck-textarea",
      attr: {
        rows: "7",
        placeholder:
          "Ce que le résident peut voir ou entendre avant ton intervention.",
      },
    });
    scene.value = this.draftScene;
    sceneLabel.htmlFor = "holodeck-scene";
    scene.id = "holodeck-scene";
    scene.addEventListener("input", () => {
      this.draftScene = scene.value;
    });

    const interventionLabel = section.createEl("label", {
      cls: "holodeck-field-label",
      text: "Intervention publique",
    });
    const intervention = section.createEl("textarea", {
      cls: "holodeck-textarea",
      attr: {
        rows: "6",
        placeholder: "Ton geste, ta réplique ou ta question.",
      },
    });
    intervention.value = this.draftIntervention;
    interventionLabel.htmlFor = "holodeck-intervention";
    intervention.id = "holodeck-intervention";
    intervention.addEventListener("input", () => {
      this.draftIntervention = intervention.value;
    });

    new Setting(section)
      .setName("Parole attendue")
      .setDesc("Désactive-la pour une attente ou une entrée silencieuse.")
      .addToggle((toggle) => {
        toggle.setValue(this.speechRequired);
        toggle.onChange((value) => {
          this.speechRequired = value;
        });
      });

    new Setting(section)
      .setName("Raisonnement")
      .addDropdown((dropdown) => {
        dropdown
          .addOption("low", "Léger")
          .addOption("medium", "Moyen")
          .addOption("high", "Élevé");
        dropdown.setValue(this.plugin.settings.reasoningEffort);
        dropdown.onChange(async (value) => {
          this.plugin.settings.reasoningEffort = value;
          await this.plugin.saveSettings();
        });
      });

    const actions = section.createDiv({ cls: "holodeck-actions" });
    const runButton = addLabeledButton(
      actions,
      "play",
      this.runningProcess ? "En cours..." : "Lancer le tour",
      "mod-cta"
    );
    runButton.disabled = Boolean(this.runningProcess);
    runButton.addEventListener("click", async () => {
      await this.launchTurn(metadata);
    });

    if (this.runningProcess) {
      const cancelButton = addLabeledButton(actions, "square", "Arrêter");
      cancelButton.addEventListener("click", () => this.cancelRun());
    }

    addIconButton(actions, "file-text", "Ouvrir la transcription publique", () =>
      this.openRuntimeFile(`${RUNTIME_ROOT}/${this.currentSession}/public.md`)
    );
    addIconButton(actions, "lock-keyhole", "Ouvrir la perspective privée", () =>
      this.openRuntimeFile(
        `${RUNTIME_ROOT}/${this.currentSession}/private/${metadata.resident}.md`
      )
    );

    const status = section.createDiv({
      cls: `holodeck-status is-${this.statusKind}`,
      text: this.statusMessage || "Prêt.",
    });
    status.setAttr("aria-live", "polite");

    const footer = section.createDiv({ cls: "holodeck-actions secondary" });
    const replaceTurn = addLabeledButton(
      footer,
      "rotate-ccw",
      "Remplacer le dernier tour"
    );
    replaceTurn.disabled = Boolean(this.runningProcess) || !metadata.latestTurn;
    replaceTurn.addEventListener("click", () => {
      new ConfirmReplaceModal(
        this.app,
        metadata.latestTurn,
        async () => this.replaceLastTurn()
      ).open();
    });
    const finish = addLabeledButton(
      footer,
      "flag",
      "Terminer la séquence"
    );
    finish.disabled = Boolean(this.runningProcess);
    finish.addEventListener("click", async () => {
      await this.finishSequence();
    });
    const leave = addLabeledButton(footer, "log-out", "Quitter la session");
    leave.disabled = Boolean(this.runningProcess);
    leave.addEventListener("click", async () => {
      this.plugin.settings.currentSession = "";
      this.draftScene = "";
      this.draftIntervention = "";
      this.sceneQuestion = "";
      this.sceneAnswer = "";
      this.sceneCertainty = "";
      this.sceneToolsOpen = false;
      this.speechRequired = true;
      this.lastOutput = "";
      this.setStatus("");
      await this.plugin.saveSettings();
      await this.render();
    });
  }

  timelineLabel(value) {
    return (
      {
        current: "continuité actuelle",
        out_of_timeline: "hors timeline",
        locked: "contexte verrouillé",
      }[value] || value
    );
  }

  async createSession(sessionId) {
    try {
      const safeSession = requireSafeComponent(sessionId, "session");
      if (
        this.plugin.settings.timeline === "locked" &&
        !this.plugin.settings.contextPack
      ) {
        throw new Error("Choisis un contexte verrouillé avant de continuer.");
      }
      const sessionRoot = `${RUNTIME_ROOT}/${safeSession}`;
      if (await this.app.vault.adapter.exists(sessionRoot)) {
        throw new Error(`La session ${safeSession} existe déjà.`);
      }

      fs.mkdirSync(path.join(this.vaultRoot, ...sessionRoot.split("/"), "inbox"), {
        recursive: true,
      });
      const control = {
        resident: this.plugin.settings.resident,
        program: this.plugin.settings.program,
        timeline: this.plugin.settings.timeline,
        context_pack: this.plugin.settings.contextPack || "",
        created_at: new Date().toISOString(),
      };
      await this.app.vault.adapter.write(
        `${sessionRoot}/control.json`,
        `${JSON.stringify(control, null, 2)}\n`
      );

      this.plugin.settings.currentSession = safeSession;
      this.draftScene = "";
      this.draftIntervention = "";
      this.sceneQuestion = "";
      this.sceneAnswer = "";
      this.sceneCertainty = "";
      this.sceneToolsOpen = false;
      this.speechRequired = true;
      this.lastOutput = "";
      this.setStatus("Entrevue créée. Le tour 001 est prêt.", "success");
      await this.plugin.saveSettings();
      await this.refreshResources();
      await this.render();
    } catch (error) {
      this.setStatus(error.message || String(error), "error");
      new Notice(this.statusMessage);
      await this.render();
    }
  }

  async resumeSession(sessionId) {
    try {
      requireSafeComponent(sessionId, "session");
      this.plugin.settings.currentSession = sessionId;
      const metadata = await this.loadSessionMetadata(sessionId);
      this.plugin.settings.resident = metadata.resident;
      this.plugin.settings.program = metadata.program;
      this.plugin.settings.timeline = metadata.timeline;
      this.plugin.settings.contextPack = metadata.contextPack;
      this.draftScene = "";
      this.draftIntervention = "";
      this.sceneQuestion = "";
      this.sceneAnswer = "";
      this.sceneCertainty = "";
      this.sceneToolsOpen = false;
      this.speechRequired = true;
      await this.restorePendingDraft(sessionId, metadata);
      this.lastOutput = await this.readLatestPublicOutput(sessionId);
      this.setStatus(
        `Session reprise. Le tour ${metadata.nextTurn} est prêt.`,
        "success"
      );
      await this.plugin.saveSettings();
      await this.render();
    } catch (error) {
      this.setStatus(error.message || String(error), "error");
      new Notice(this.statusMessage);
      await this.render();
    }
  }

  async loadSessionMetadata(sessionId) {
    const sessionRoot = `${RUNTIME_ROOT}/${sessionId}`;
    const controlPath = `${sessionRoot}/control.json`;
    let metadata = {};
    if (await this.app.vault.adapter.exists(controlPath)) {
      metadata = JSON.parse(await this.app.vault.adapter.read(controlPath));
    }

    const turnIds = [];
    const turnsRoot = `${sessionRoot}/turns`;
    if (await this.app.vault.adapter.exists(turnsRoot)) {
      const listing = await this.app.vault.adapter.list(turnsRoot);
      for (const folder of listing.folders) {
        const turnId = folder.split("/").pop();
        if (turnId) turnIds.push(turnId);
      }
    }

    if (!metadata.resident && turnIds.length) {
      const latestId = turnIds.slice().sort().pop();
      const inputPath = `${turnsRoot}/${latestId}/input.md`;
      if (await this.app.vault.adapter.exists(inputPath)) {
        const frontmatter = parseFrontmatter(
          await this.app.vault.adapter.read(inputPath)
        );
        metadata = {
          resident: frontmatter.resident,
          program: frontmatter.program,
          timeline: frontmatter.timeline || "out_of_timeline",
          context_pack: frontmatter.context_pack || "",
        };
      }
    }

    if (!metadata.resident) {
      throw new Error("Impossible de déterminer le résident de cette session.");
    }

    return {
      resident: metadata.resident,
      program: metadata.program || "DPhen",
      timeline: metadata.timeline || "out_of_timeline",
      contextPack: metadata.context_pack || "",
      nextTurn: nextNumericTurn(turnIds),
      latestTurn: turnIds.slice().sort().pop() || "",
    };
  }

  async restorePendingDraft(sessionId, metadata = null) {
    const sessionMetadata =
      metadata || (await this.loadSessionMetadata(sessionId));
    const inputPath = `${RUNTIME_ROOT}/${sessionId}/inbox/tour_${sessionMetadata.nextTurn}.md`;
    if (!(await this.app.vault.adapter.exists(inputPath))) return;

    const draft = parseTurnDraft(
      await this.app.vault.adapter.read(inputPath)
    );
    this.draftScene = draft.scene;
    this.draftIntervention = draft.intervention;
    this.speechRequired = draft.speechRequired;
  }

  async launchTurn(metadata) {
    if (this.runningProcess) return;
    try {
      const session = requireSafeComponent(this.currentSession, "session");
      const inputPath = normalizePath(
        `${RUNTIME_ROOT}/${session}/inbox/tour_${metadata.nextTurn}.md`
      );
      const note = buildTurnNote({
        resident: metadata.resident,
        session,
        turn: metadata.nextTurn,
        program: metadata.program,
        timeline: metadata.timeline,
        contextPack: metadata.contextPack,
        speechRequired: this.speechRequired,
        scene: this.draftScene,
        intervention: this.draftIntervention,
      });

      const existing = this.app.vault.getAbstractFileByPath(inputPath);
      if (existing instanceof TFile) {
        await this.app.vault.modify(existing, note);
      } else if (await this.app.vault.adapter.exists(inputPath)) {
        await this.app.vault.adapter.write(inputPath, note);
      } else {
        await this.app.vault.create(inputPath, note);
      }

      this.setStatus("Lancement du tour...", "running");
      const runPromise = this.runEngine([
        "run",
        inputPath,
        "--effort",
        this.plugin.settings.reasoningEffort,
      ]);
      await this.render();
      const result = await runPromise;
      this.lastOutput =
        (await this.readLatestPublicOutput(session)) ||
        extractPublicOutput(result.stdout);
      this.draftScene = "";
      this.draftIntervention = "";
      this.sceneQuestion = "";
      this.sceneAnswer = "";
      this.sceneCertainty = "";
      this.sceneToolsOpen = false;
      this.speechRequired = true;
      this.setStatus("Tour terminé. Le suivant est prêt.", "success");
      await this.refreshResources();
      await this.render();

      if (this.plugin.settings.openPublicAfterRun) {
        await this.openRuntimeFile(`${RUNTIME_ROOT}/${session}/public.md`);
      }
    } catch (error) {
      this.setStatus(error.message || String(error), "error");
      new Notice(this.statusMessage, 8000);
      await this.render();
    }
  }

  async replaceLastTurn() {
    if (this.runningProcess) return;
    try {
      this.setStatus("Restauration du tour précédent...", "running");
      const rewindPromise = this.runEngine([
        "rewind",
        "--session",
        this.currentSession,
      ]);
      await this.render();
      await rewindPromise;

      const metadata = await this.loadSessionMetadata(this.currentSession);
      this.draftScene = "";
      this.draftIntervention = "";
      this.sceneQuestion = "";
      this.sceneAnswer = "";
      this.sceneCertainty = "";
      this.sceneToolsOpen = false;
      this.speechRequired = true;
      await this.restorePendingDraft(this.currentSession, metadata);
      this.lastOutput = await this.readLatestPublicOutput(this.currentSession);
      this.setStatus(
        `Tour ${metadata.nextTurn} restauré. Modifie-le ou relance-le.`,
        "success"
      );
      await this.refreshResources();
      await this.render();
    } catch (error) {
      this.setStatus(error.message || String(error), "error");
      new Notice(this.statusMessage, 8000);
      await this.render();
    }
  }

  async askSceneQuestion() {
    if (this.runningProcess) return;
    const question = this.sceneQuestion.trim();
    if (!question) {
      new Notice("Écris d’abord une question sur la scène.");
      return;
    }

    try {
      this.sceneAnswer = "";
      this.sceneCertainty = "";
      this.setStatus("Lecture de la scène publique...", "running");
      const queryPromise = this.runEngine([
        "scene-query",
        "--session",
        this.currentSession,
        "--question",
        question,
      ]);
      await this.render();
      const result = await queryPromise;
      const parsed = JSON.parse(result.stdout.trim());
      this.sceneAnswer = parsed.answer || "";
      this.sceneCertainty = parsed.certainty || "";
      this.setStatus(
        "Question de scène répondue sans avancer le tour.",
        "success"
      );
      await this.render();
    } catch (error) {
      this.setStatus(error.message || String(error), "error");
      new Notice(this.statusMessage, 8000);
      await this.render();
    }
  }

  async addSceneAdjustment(text) {
    if (this.runningProcess) return;
    try {
      this.sceneToolsOpen = true;
      this.setStatus("Enregistrement de l’ajustement de scène...", "running");
      const adjustmentPromise = this.runEngine([
        "scene-adjust",
        "--session",
        this.currentSession,
        "--text",
        text,
      ]);
      await this.render();
      await adjustmentPromise;
      this.setStatus(
        "Scène ajustée sans faire avancer le tour.",
        "success"
      );
      new Notice("Ajustement de scène enregistré.");
      await this.render();
    } catch (error) {
      this.setStatus(error.message || String(error), "error");
      new Notice(this.statusMessage, 8000);
      await this.render();
    }
  }

  async finishSequence() {
    if (this.runningProcess) return;
    try {
      this.setStatus("Calcul du rapport de séquence...", "running");
      const usagePromise = this.runEngine([
        "usage",
        "--session",
        this.currentSession,
      ]);
      await this.render();
      const result = await usagePromise;
      this.lastOutput = `\`\`\`text\n${result.stdout.trim()}\n\`\`\``;
      this.setStatus(
        "Rapport produit. La session demeure locale et non canonique.",
        "success"
      );
      await this.render();
    } catch (error) {
      this.setStatus(error.message || String(error), "error");
      new Notice(this.statusMessage, 8000);
      await this.render();
    }
  }

  pythonExecutable() {
    if (this.plugin.settings.pythonPath.trim()) {
      const configured = this.plugin.settings.pythonPath.trim();
      return path.isAbsolute(configured)
        ? configured
        : path.join(this.vaultRoot, configured);
    }
    const windowsVenv = path.join(
      this.vaultRoot,
      ".venv",
      "Scripts",
      "python.exe"
    );
    if (fs.existsSync(windowsVenv)) return windowsVenv;
    const posixVenv = path.join(this.vaultRoot, ".venv", "bin", "python");
    if (fs.existsSync(posixVenv)) return posixVenv;
    return "python";
  }

  runEngine(args) {
    return new Promise((resolve, reject) => {
      const executable = this.pythonExecutable();
      const child = spawn(executable, ["-m", "holodeck_engine", ...args], {
        cwd: this.vaultRoot,
        windowsHide: true,
        shell: false,
        env: {
          ...process.env,
          PYTHONIOENCODING: "utf-8",
          PYTHONUTF8: "1",
        },
      });
      this.runningProcess = child;
      this.startedAt = Date.now();
      this.startElapsedTimer();

      let stdout = "";
      let stderr = "";
      child.stdout.setEncoding("utf8");
      child.stderr.setEncoding("utf8");
      child.stdout.on("data", (chunk) => {
        stdout += chunk;
      });
      child.stderr.on("data", (chunk) => {
        stderr += chunk;
      });
      child.on("error", (error) => {
        this.runningProcess = null;
        this.clearElapsedTimer();
        reject(error);
      });
      child.on("close", (code) => {
        this.runningProcess = null;
        this.clearElapsedTimer();
        if (code === 0) {
          resolve({ stdout, stderr });
          return;
        }
        const message = (stderr || stdout || `Processus terminé avec le code ${code}`)
          .trim()
          .replace(/^Erreur:\s*/i, "");
        reject(new Error(message));
      });
    });
  }

  startElapsedTimer() {
    this.clearElapsedTimer();
    this.elapsedTimer = window.setInterval(() => {
      const seconds = Math.round((Date.now() - this.startedAt) / 1000);
      const status = this.contentEl.querySelector(".holodeck-status");
      if (status) status.setText(`Calcul en cours · ${seconds} s`);
    }, 1000);
  }

  clearElapsedTimer() {
    if (this.elapsedTimer) window.clearInterval(this.elapsedTimer);
    this.elapsedTimer = null;
  }

  cancelRun() {
    if (!this.runningProcess) return;
    this.runningProcess.kill();
    this.setStatus("Arrêt demandé. Aucun tour incomplet ne sera canonisé.", "idle");
  }

  async readLatestPublicOutput(sessionId) {
    const turnsRoot = `${RUNTIME_ROOT}/${sessionId}/turns`;
    if (!(await this.app.vault.adapter.exists(turnsRoot))) return "";
    const listing = await this.app.vault.adapter.list(turnsRoot);
    const turnIds = listing.folders
      .map((folder) => folder.split("/").pop())
      .filter(Boolean)
      .sort();
    const latestId = turnIds.pop();
    if (!latestId) return "";

    const resultPath = `${turnsRoot}/${latestId}/result.json`;
    const inputPath = `${turnsRoot}/${latestId}/input.md`;
    if (
      !(await this.app.vault.adapter.exists(resultPath)) ||
      !(await this.app.vault.adapter.exists(inputPath))
    ) {
      return "";
    }

    const result = JSON.parse(await this.app.vault.adapter.read(resultPath));
    const metadata = parseFrontmatter(
      await this.app.vault.adapter.read(inputPath)
    );
    const resident = metadata.resident || "Résident";
    return (result.events || [])
      .filter((event) => event.visibility === "public")
      .map((event) => {
        if (event.kind === "action") return `*${event.text.trim()}*`;
        return `**${resident} :** « ${event.text.trim()} »`;
      })
      .join("\n\n");
  }

  async openRuntimeFile(filePath) {
    if (!(await this.app.vault.adapter.exists(filePath))) {
      new Notice("Ce document n’existe pas encore.");
      return;
    }
    let file = this.app.vault.getAbstractFileByPath(filePath);
    if (!(file instanceof TFile)) {
      await new Promise((resolve) => window.setTimeout(resolve, 500));
      file = this.app.vault.getAbstractFileByPath(filePath);
    }
    if (file instanceof TFile) {
      await this.app.workspace.getLeaf("tab").openFile(file);
      return;
    }
    new Notice("Obsidian indexe encore ce fichier. Réessaie dans un instant.");
  }
}

class HolodeckSettingTab extends PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display() {
    const { containerEl } = this;
    containerEl.empty();
    containerEl.createEl("h2", { text: "Holodeck Control" });

    new Setting(containerEl)
      .setName("Exécutable Python")
      .setDesc(
        "Laisse vide pour utiliser automatiquement .venv/Scripts/python.exe."
      )
      .addText((text) => {
        text
          .setPlaceholder(".venv/Scripts/python.exe")
          .setValue(this.plugin.settings.pythonPath)
          .onChange(async (value) => {
            this.plugin.settings.pythonPath = value.trim();
            await this.plugin.saveSettings();
          });
      });

    new Setting(containerEl)
      .setName("Raisonnement par défaut")
      .addDropdown((dropdown) => {
        dropdown
          .addOption("low", "Léger")
          .addOption("medium", "Moyen")
          .addOption("high", "Élevé")
          .setValue(this.plugin.settings.reasoningEffort)
          .onChange(async (value) => {
            this.plugin.settings.reasoningEffort = value;
            await this.plugin.saveSettings();
          });
      });

    new Setting(containerEl)
      .setName("Ouvrir la transcription après chaque tour")
      .addToggle((toggle) => {
        toggle
          .setValue(this.plugin.settings.openPublicAfterRun)
          .onChange(async (value) => {
            this.plugin.settings.openPublicAfterRun = value;
            await this.plugin.saveSettings();
          });
      });

    containerEl.createEl("p", {
      cls: "setting-item-description",
      text: "La clé API demeure dans .env. Le plugin ne la lit ni ne l’affiche.",
    });
  }
}

module.exports = class HolodeckControlPlugin extends Plugin {
  async onload() {
    await this.loadSettings();
    this.registerView(
      VIEW_TYPE,
      (leaf) => new HolodeckControlView(leaf, this)
    );

    this.addRibbonIcon("theater", "Ouvrir Holodeck", () =>
      this.activateView()
    );
    this.addCommand({
      id: "open-holodeck-control",
      name: "Ouvrir le panneau de contrôle",
      callback: () => this.activateView(),
    });
    this.addSettingTab(new HolodeckSettingTab(this.app, this));
  }

  onunload() {
    this.app.workspace.detachLeavesOfType(VIEW_TYPE);
  }

  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }

  async activateView() {
    let leaf = this.app.workspace.getLeavesOfType(VIEW_TYPE)[0];
    if (!leaf) {
      leaf = this.app.workspace.getLeaf("tab");
      await leaf.setViewState({ type: VIEW_TYPE, active: true });
    }
    await this.app.workspace.revealLeaf(leaf);
  }
};
