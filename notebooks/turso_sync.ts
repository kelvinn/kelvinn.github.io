#!/usr/bin/env node

import { connect } from "@tursodatabase/sync";
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, openSync, closeSync, readFileSync, readdirSync, renameSync, rmSync, unlinkSync, writeFileSync } from "node:fs";
import { mkdtempSync } from "node:fs";
import { homedir, tmpdir } from "node:os";
import { basename, dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const DEFAULT_DB_ROOT = "~/HealthData/DBs";
const DEFAULT_PREFIX = "health-";
const DEFAULT_CONFIG_DIR = "~/.config/turso-sync";
const DEFAULT_MAP_PATH = "~/.config/turso-sync/turso-sync-map.json";
const DEFAULT_STATE_PATH = "~/.config/turso-sync/turso-sync-state.json";
const DEFAULT_ENABLE_PATH = "~/.config/turso-sync/enabled.flag";
const DEFAULT_LOCK_PATH = "~/.config/turso-sync/sync.lock";
const DEFAULT_LABEL = "com.kelvinn.healthdata.turso-sync";
const DEFAULT_LAUNCHD_DEST = "~/Library/LaunchAgents/com.kelvinn.healthdata.turso-sync.plist";
const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));

interface Settings {
  dbRoot: string;
  dbPrefix: string;
  mapPath: string;
  statePath: string;
  enablePath: string;
  lockPath: string;
  group?: string;
  authToken?: string;
}

interface MappingEntry {
  local_filename: string;
  local_path: string;
  remote_name: string;
  url: string;
  created_at?: string;
  updated_at?: string;
}

interface MappingFile {
  databases: Record<string, MappingEntry>;
  updated_at?: string;
}

interface StateFile {
  databases: Record<string, Record<string, unknown>>;
  updated_at?: string;
}

class RunnerError extends Error {}

function nowIso(): string {
  return new Date().toISOString();
}

function expandPath(p: string): string {
  if (p.startsWith("~/")) return join(homedir(), p.slice(2));
  if (p === "~") return homedir();
  return p;
}

function ensureParent(path: string): void {
  mkdirSync(dirname(path), { recursive: true });
}

function readJson<T>(path: string, fallback: T): T {
  if (!existsSync(path)) return fallback;
  return JSON.parse(readFileSync(path, "utf-8")) as T;
}

function writeJson(path: string, data: unknown): void {
  ensureParent(path);
  writeFileSync(path, `${JSON.stringify(data, null, 2)}\n`, "utf-8");
}

function runCommand(cmd: string, args: string[], check = true): { stdout: string; stderr: string; status: number } {
  const result = spawnSync(cmd, args, { encoding: "utf-8" });
  const stdout = (result.stdout ?? "").trim();
  const stderr = (result.stderr ?? "").trim();
  const status = result.status ?? 1;
  if (check && status !== 0) {
    throw new RunnerError([
      `Command failed (${status}): ${cmd} ${args.join(" ")}`,
      stderr ? `stderr: ${stderr}` : "",
      stdout ? `stdout: ${stdout}` : "",
    ].filter(Boolean).join("\n"));
  }
  return { stdout, stderr, status };
}

function settingsFromEnv(): Settings {
  return {
    dbRoot: expandPath(process.env.TURSO_DB_ROOT ?? DEFAULT_DB_ROOT),
    dbPrefix: process.env.TURSO_DB_PREFIX ?? DEFAULT_PREFIX,
    mapPath: expandPath(process.env.TURSO_MAP_PATH ?? DEFAULT_MAP_PATH),
    statePath: expandPath(process.env.TURSO_STATE_PATH ?? DEFAULT_STATE_PATH),
    enablePath: expandPath(process.env.TURSO_ENABLE_PATH ?? DEFAULT_ENABLE_PATH),
    lockPath: expandPath(process.env.TURSO_SYNC_LOCK_PATH ?? DEFAULT_LOCK_PATH),
    group: process.env.TURSO_GROUP,
    authToken: process.env.TURSO_AUTH_TOKEN,
  };
}

function isValidUrl(url: string | undefined): boolean {
  return Boolean(url && (url.startsWith("libsql://") || url.startsWith("https://") || url.startsWith("http://")));
}

function sanitizeRemoteName(prefix: string, filename: string): string {
  const stem = filename.replace(/\.db$/, "");
  let safe = stem.toLowerCase().replace(/[^a-z0-9-]/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "");
  if (!safe) throw new RunnerError(`Cannot derive remote name from ${filename}`);
  return `${prefix}${safe}`.slice(0, 63);
}

function isLegacyMetadataError(message: string): boolean {
  const text = message.toLowerCase();
  return text.includes("unexpected metadata file format") || text.includes("deserialization error");
}

function backupLegacyInfoFile(dbPath: string): boolean {
  const infoPath = `${dbPath}-info`;
  if (!existsSync(infoPath)) return false;
  const backupPath = `${infoPath}.legacy-${Date.now()}`;
  renameSync(infoPath, backupPath);
  console.warn(`Backed up legacy metadata file: ${infoPath} -> ${backupPath}`);
  return true;
}

function discoverDatabases(root: string): string[] {
  if (!existsSync(root)) throw new RunnerError(`Database root missing: ${root}`);
  return readdirSync(root)
    .filter((name) => name.endsWith(".db"))
    .map((name) => join(root, name))
    .sort();
}

function acquireLock(lockPath: string): number {
  ensureParent(lockPath);
  const holder = `pid=${process.pid} started_at=${nowIso()}\n`;

  try {
    const fd = openSync(lockPath, "wx", 0o600);
    writeFileSync(fd, holder, { encoding: "utf-8" });
    return fd;
  } catch {
    if (!existsSync(lockPath)) throw new RunnerError(`Failed to acquire lock at ${lockPath}`);
    const current = readFileSync(lockPath, "utf-8").trim();
    const pidMatch = current.match(/pid=(\d+)/);
    if (pidMatch) {
      const pid = Number(pidMatch[1]);
      try {
        process.kill(pid, 0);
        throw new RunnerError(`Another sync is already running (lock: ${lockPath}). Holder: ${current}`);
      } catch {
        // stale lock
      }
    }
    unlinkSync(lockPath);
    const fd = openSync(lockPath, "wx", 0o600);
    writeFileSync(fd, holder, { encoding: "utf-8" });
    return fd;
  }
}

function releaseLock(fd: number, lockPath: string): void {
  try { closeSync(fd); } catch {}
  try { unlinkSync(lockPath); } catch {}
}

function listGroups(): string[] {
  const { stdout } = runCommand("turso", ["group", "list"]);
  const lines = stdout.split("\n").map((s) => s.trim()).filter(Boolean);
  return lines
    .filter((line) => !line.toUpperCase().startsWith("NAME"))
    .map((line) => line.split(/\s+/)[0]);
}

function resolveGroup(explicit?: string): string {
  const groups = listGroups();
  if (!groups.length) throw new RunnerError("No Turso groups found");
  if (explicit) {
    if (!groups.includes(explicit)) {
      throw new RunnerError(`TURSO_GROUP=${explicit} not found. Available: ${groups.join(", ")}`);
    }
    return explicit;
  }
  if (groups.length === 1) return groups[0];
  throw new RunnerError(`Multiple groups found. Set TURSO_GROUP. Available: ${groups.join(", ")}`);
}

function remoteExists(name: string): boolean {
  const result = runCommand("turso", ["db", "show", name, "--url"], false);
  return result.status === 0 && isValidUrl(result.stdout);
}

function remoteUrl(name: string): string {
  const { stdout } = runCommand("turso", ["db", "show", name, "--url"]);
  if (!isValidUrl(stdout)) throw new RunnerError(`Unexpected URL output for ${name}: ${stdout}`);
  return stdout;
}

function createSnapshotWal(sourcePath: string): string {
  const dir = mkdtempSync(join(tmpdir(), `${basename(sourcePath, ".db")}-`));
  const snapshot = join(dir, `${basename(sourcePath, ".db")}.snapshot.db`);
  runCommand("sqlite3", [sourcePath, `.backup ${snapshot}`]);
  runCommand("sqlite3", [snapshot, "PRAGMA journal_mode=WAL;"]);
  return snapshot;
}

function createRemoteFromFile(remoteName: string, sourcePath: string, group: string): void {
  const snapshot = createSnapshotWal(sourcePath);
  try {
    const result = runCommand("turso", ["db", "create", remoteName, "--from-file", snapshot, "--wait", "--group", group], false);
    if (result.status !== 0) {
      const txt = `${result.stderr}\n${result.stdout}`.toLowerCase();
      if (!txt.includes("already exists")) {
        throw new RunnerError([
          `Failed creating ${remoteName} from ${sourcePath}`,
          result.stderr ? `stderr: ${result.stderr}` : "",
          result.stdout ? `stdout: ${result.stdout}` : "",
        ].filter(Boolean).join("\n"));
      }
    }
  } finally {
    try { rmSync(dirname(snapshot), { recursive: true, force: true }); } catch {}
  }
}

function ensureMappingEntry(settings: Settings, map: MappingFile, localPath: string, allowCreate: boolean): MappingEntry {
  const filename = basename(localPath);
  const existing = map.databases[filename];
  if (existing && existing.remote_name && isValidUrl(existing.url)) {
    existing.local_path = localPath;
    existing.updated_at = nowIso();
    return existing;
  }

  const remoteName = sanitizeRemoteName(settings.dbPrefix, filename);
  if (!remoteExists(remoteName)) {
    if (!allowCreate) throw new RunnerError(`Missing remote database for ${filename}`);
    const group = resolveGroup(settings.group);
    createRemoteFromFile(remoteName, localPath, group);
  }

  const entry: MappingEntry = {
    local_filename: filename,
    local_path: localPath,
    remote_name: remoteName,
    url: remoteUrl(remoteName),
    created_at: existing?.created_at ?? nowIso(),
    updated_at: nowIso(),
  };
  map.databases[filename] = entry;
  return entry;
}

async function syncOne(entry: MappingEntry, authToken: string, options: { dryRun: boolean; pullAfterPush: boolean; checkpoint: boolean }): Promise<{ pendingBefore: number; pendingAfter: number }> {
  let db;
  try {
    db = await connect({
      path: entry.local_path,
      url: entry.url,
      authToken,
      clientName: `health-sync-${process.pid}`,
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    if (isLegacyMetadataError(msg) && backupLegacyInfoFile(entry.local_path)) {
      db = await connect({
        path: entry.local_path,
        url: entry.url,
        authToken,
        clientName: `health-sync-${process.pid}`,
      });
    } else {
      throw err;
    }
  }

  try {
    const before = await db.stats();
    if (options.dryRun) {
      console.log(`[dry-run] ${entry.local_filename} pending_cdc=${before.cdcOperations} main_wal=${before.mainWalSize} revert_wal=${before.revertWalSize}`);
      return { pendingBefore: before.cdcOperations, pendingAfter: before.cdcOperations };
    }
    await db.push();
    if (options.pullAfterPush) {
      await db.pull();
    }
    if (options.checkpoint) {
      await db.checkpoint();
    }
    const after = await db.stats();
    console.log(`Synced ${entry.local_filename} pending_cdc_before=${before.cdcOperations} pending_cdc_after=${after.cdcOperations}`);
    return { pendingBefore: before.cdcOperations, pendingAfter: after.cdcOperations };
  } finally {
    await db.close();
  }
}

function parseArgs(argv: string[]): { cmd: string; flags: Set<string>; kv: Map<string, string> } {
  if (argv.length === 0) return { cmd: "", flags: new Set(), kv: new Map() };
  const [cmd, ...rest] = argv;
  const flags = new Set<string>();
  const kv = new Map<string, string>();
  for (let i = 0; i < rest.length; i += 1) {
    const a = rest[i];
    if (a.startsWith("--")) {
      const nxt = rest[i + 1];
      if (nxt && !nxt.startsWith("--")) {
        kv.set(a, nxt);
        i += 1;
      } else {
        flags.add(a);
      }
    }
  }
  return { cmd, flags, kv };
}

function printHelp(): void {
  console.log(`Usage: npx tsx notebooks/turso_sync.ts <command> [options]

Commands:
  bootstrap
  sync [--dry-run] [--ignore-gate] [--pull-after-push] [--checkpoint]
  enable-sync [--env-file <path>]
  disable-sync [--env-file <path>]
  install-launchd [--env-file <path>] [--load]
`);
}

function parseEnvFile(path: string): Record<string, string> {
  if (!existsSync(path)) return {};
  const out: Record<string, string> = {};
  for (const raw of readFileSync(path, "utf-8").split("\n")) {
    const line = raw.trim();
    if (!line || line.startsWith("#") || !line.includes("=")) continue;
    const idx = line.indexOf("=");
    const key = line.slice(0, idx).trim();
    const value = line.slice(idx + 1).trim().replace(/^['\"]|['\"]$/g, "");
    out[key] = value;
  }
  return out;
}

function enablePathFromEnvFile(defaultPath: string, envFile?: string): string {
  if (!envFile) return defaultPath;
  const env = parseEnvFile(expandPath(envFile));
  return expandPath(env.TURSO_ENABLE_PATH ?? defaultPath);
}

function installLaunchd(envFile: string, load: boolean): void {
  const repoRoot = resolve(SCRIPT_DIR, "..");
  const scriptPath = resolve(SCRIPT_DIR, "turso_sync.ts");
  const tsxPath = resolve(SCRIPT_DIR, "node_modules/.bin/tsx");
  if (!existsSync(tsxPath)) {
    throw new RunnerError(`tsx not found at ${tsxPath}. Run: cd notebooks && npm install`);
  }

  const stdoutLog = expandPath("~/.config/turso-sync/logs/sync.out.log");
  const stderrLog = expandPath("~/.config/turso-sync/logs/sync.err.log");
  ensureParent(stdoutLog);
  ensureParent(stderrLog);

  const command = `cd ${repoRoot} && set -a; [ -f \"${envFile}\" ] && source \"${envFile}\"; set +a; ${tsxPath} ${scriptPath} sync`;
  const plist = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${DEFAULT_LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/zsh</string>
    <string>-lc</string>
    <string>${command.replace(/&/g, "&amp;")}</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>StartInterval</key><integer>3600</integer>
  <key>StandardOutPath</key><string>${stdoutLog}</string>
  <key>StandardErrorPath</key><string>${stderrLog}</string>
</dict>
</plist>\n`;

  const dest = expandPath(DEFAULT_LAUNCHD_DEST);
  ensureParent(dest);
  writeFileSync(dest, plist, "utf-8");
  console.log(`Installed LaunchAgent plist: ${dest}`);

  if (load) {
    runCommand("launchctl", ["unload", dest], false);
    runCommand("launchctl", ["load", dest], true);
    console.log("Loaded LaunchAgent");
  }
}

async function main(): Promise<number> {
  const parsed = parseArgs(process.argv.slice(2));
  if (!parsed.cmd || parsed.cmd === "--help" || parsed.cmd === "-h" || parsed.flags.has("--help") || parsed.flags.has("-h")) {
    printHelp();
    return 0;
  }

  const settings = settingsFromEnv();

  if (parsed.cmd === "enable-sync") {
    const envFile = parsed.kv.get("--env-file");
    const enablePath = enablePathFromEnvFile(settings.enablePath, envFile);
    ensureParent(enablePath);
    writeFileSync(enablePath, `enabled_at=${nowIso()}\n`, "utf-8");
    console.log(`Sync enabled: ${enablePath}`);
    return 0;
  }

  if (parsed.cmd === "disable-sync") {
    const envFile = parsed.kv.get("--env-file");
    const enablePath = enablePathFromEnvFile(settings.enablePath, envFile);
    try { unlinkSync(enablePath); } catch {}
    console.log(`Sync disabled (removed): ${enablePath}`);
    return 0;
  }

  if (parsed.cmd === "install-launchd") {
    const envFile = expandPath(parsed.kv.get("--env-file") ?? "notebooks/turso_sync.env");
    const load = parsed.flags.has("--load");
    installLaunchd(envFile, load);
    return 0;
  }

  if (parsed.cmd === "bootstrap") {
    const localDbs = discoverDatabases(settings.dbRoot);
    const mapping = readJson<MappingFile>(settings.mapPath, { databases: {} });
    let created = 0;
    let reused = 0;
    const failures: string[] = [];

    for (const dbPath of localDbs) {
      try {
        const before = mapping.databases[basename(dbPath)];
        const beforeValid = Boolean(before && before.remote_name && isValidUrl(before.url));
        const entry = ensureMappingEntry(settings, mapping, dbPath, true);
        if (beforeValid) {
          reused += 1;
          console.log(`Reused existing remote ${entry.remote_name} for ${basename(dbPath)}`);
        } else {
          created += 1;
          console.log(`Created/repaired remote ${entry.remote_name} for ${basename(dbPath)}`);
        }
      } catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        failures.push(`${basename(dbPath)}: ${msg}`);
        console.error(`ERROR ${basename(dbPath)}: ${msg}`);
      }
    }

    mapping.updated_at = nowIso();
    writeJson(settings.mapPath, mapping);
    console.log(`Wrote mapping: ${settings.mapPath}`);
    console.log(`Summary: created_or_repaired=${created}, reused=${reused}, failures=${failures.length}`);
    if (failures.length) {
      for (const f of failures) console.error(` - ${f}`);
      return 1;
    }
    return 0;
  }

  if (parsed.cmd === "sync") {
    const dryRun = parsed.flags.has("--dry-run");
    const ignoreGate = parsed.flags.has("--ignore-gate");
    const pullAfterPush = parsed.flags.has("--pull-after-push");
    const checkpoint = parsed.flags.has("--checkpoint");

    const lockFd = acquireLock(settings.lockPath);
    try {
      if (!dryRun && !ignoreGate && !existsSync(settings.enablePath)) {
        console.log(`Sync disabled: enable gate file not found at ${settings.enablePath}. Run enable-sync when ready.`);
        return 0;
      }

      if (!settings.authToken) {
        throw new RunnerError("TURSO_AUTH_TOKEN is required for sync.");
      }

      const mapping = readJson<MappingFile>(settings.mapPath, { databases: {} });
      const state = readJson<StateFile>(settings.statePath, { databases: {} });
      const localDbs = discoverDatabases(settings.dbRoot);

      let pendingBeforeTotal = 0;
      let pendingAfterTotal = 0;
      let syncedCount = 0;
      const failures: string[] = [];

      for (const dbPath of localDbs) {
        const name = basename(dbPath);
        try {
          const entry = ensureMappingEntry(settings, mapping, dbPath, !dryRun);
          const summary = await syncOne(entry, settings.authToken, { dryRun, pullAfterPush, checkpoint });
          pendingBeforeTotal += summary.pendingBefore;
          pendingAfterTotal += summary.pendingAfter;
          syncedCount += 1;
          state.databases[name] = {
            last_success_at: nowIso(),
            mode: "turso_sync_typescript",
          };
        } catch (err) {
          let msg = err instanceof Error ? err.message : String(err);
          if (msg.includes("auth role not found")) {
            msg = `${msg}\nHint: TURSO_AUTH_TOKEN is invalid for this DB/group. Regenerate a group token (e.g. turso group tokens create ${settings.group ?? "<group>"}) and update notebooks/turso_sync.env.`;
          }
          failures.push(`${name}: ${msg}`);
          console.error(`ERROR ${name}: ${msg}`);
        }
      }

      if (!dryRun) {
        mapping.updated_at = nowIso();
        state.updated_at = nowIso();
        writeJson(settings.mapPath, mapping);
        writeJson(settings.statePath, state);
      }

      console.log(`Sync summary: databases=${localDbs.length}, databases_synced=${syncedCount}, pending_before=${pendingBeforeTotal}, pending_after=${pendingAfterTotal}, failures=${failures.length}`);
      if (failures.length) {
        for (const f of failures) console.error(` - ${f}`);
        return 1;
      }
      return 0;
    } finally {
      releaseLock(lockFd, settings.lockPath);
    }
  }

  throw new RunnerError(`Unknown command: ${parsed.cmd}`);
}

main()
  .then((code) => {
    process.exitCode = code;
  })
  .catch((err) => {
    console.error(err instanceof Error ? err.message : String(err));
    process.exitCode = 1;
  });
