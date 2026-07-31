import fs from "node:fs";
import path from "node:path";
import process from "node:process";

import initSqlJs from "sql.js";

const [, , inputPath, outputPath] = process.argv;
if (!inputPath || !outputPath) {
  throw new Error("Usage: node scripts/generate-sqlite.mjs <distribution-json> <output-sqlite>");
}

const payload = JSON.parse(fs.readFileSync(inputPath, "utf8"));
const SQL = await initSqlJs({
  locateFile: (filename) => path.resolve("node_modules/sql.js/dist", filename),
});
const database = new SQL.Database();

database.run("PRAGMA page_size = 4096");
database.run(`
  CREATE TABLE tr_iban_providers (
    code TEXT PRIMARY KEY,
    raw_code TEXT NOT NULL,
    name_official TEXT NOT NULL,
    name_short TEXT NOT NULL,
    type TEXT NOT NULL,
    status TEXT NOT NULL,
    systems TEXT NOT NULL,
    code_evidence TEXT NOT NULL,
    aliases TEXT NOT NULL,
    sources_json TEXT NOT NULL,
    last_verified_at TEXT NOT NULL
  ) WITHOUT ROWID
`);

const insert = database.prepare(`
  INSERT INTO tr_iban_providers (
    code, raw_code, name_official, name_short, type, status, systems,
    code_evidence, aliases, sources_json, last_verified_at
  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
`);
for (const provider of payload.providers) {
  insert.run([
    provider.code,
    provider.rawCode,
    provider.nameOfficial,
    provider.nameShort,
    provider.type,
    provider.status,
    provider.systems.join("|"),
    provider.codeEvidence.join("|"),
    provider.aliases.join("|"),
    JSON.stringify(provider.sources),
    provider.lastVerifiedAt,
  ]);
}
insert.free();
database.run("PRAGMA user_version = 1");

const bytes = database.export();
database.close();
bytes.fill(0, 96, 100);
fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, bytes);
