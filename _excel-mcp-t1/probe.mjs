import { spawn } from 'node:child_process';
import { appendFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const LOG = fileURLToPath(new URL('./probe-log.txt', import.meta.url));
const log = (s) => appendFileSync(LOG, s + '\n');

const ROOT = 'D:\\workspace\\zcode研究\\_excel-mcp-t1';
const proc = spawn('npx', ['-y', 'excel-mcp-server@latest'], {
  shell: true,
  env: { ...process.env, EXCEL_FILES_PATH: ROOT },
  stdio: ['pipe', 'pipe', 'pipe'],
});

let buf = '';
const pending = new Map();
let nextId = 1;
proc.stdout.on('data', (d) => {
  buf += d.toString();
  let idx;
  while ((idx = buf.indexOf('\n')) >= 0) {
    const line = buf.slice(0, idx).trim();
    buf = buf.slice(idx + 1);
    if (!line) continue;
    let msg;
    try { msg = JSON.parse(line); } catch { log('NON-JSON-LINE: ' + line.slice(0, 300)); continue; }
    if (msg.id !== undefined && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  }
});
proc.stderr.on('data', (d) => log('[srv-stderr] ' + d.toString().trim()));
proc.on('error', (e) => log('[spawn-error] ' + e.message));

function request(method, params, tmo = 90000) {
  const id = nextId++;
  return new Promise((resolve, reject) => {
    pending.set(id, resolve);
    proc.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method, params }) + '\n');
    setTimeout(() => { if (pending.has(id)) { pending.delete(id); reject(new Error('timeout: ' + method)); } }, tmo);
  });
}
const notify = (method, params) => proc.stdin.write(JSON.stringify({ jsonrpc: '2.0', method, params }) + '\n');

try {
  const init = await request('initialize', {
    protocolVersion: '2024-11-05',
    capabilities: {},
    clientInfo: { name: 'arm-b-probe', version: '1.0.0' },
  }, 120000);
  log('INIT_SERVERINFO=' + JSON.stringify(init.result?.serverInfo));
  notify('notifications/initialized', {});

  const tools = await request('tools/list', {});
  const list = tools.result?.tools ?? [];
  log('TOOL_COUNT=' + list.length);
  log('TOOL_NAMES=' + list.map((t) => t.name).join(','));
  for (const t of list) log('SCHEMA ' + t.name + ' :: ' + JSON.stringify(t.inputSchema));
  log('PROBE_OK');
} catch (e) {
  log('PROBE_FAIL ' + e.message);
} finally {
  try { proc.kill(); } catch {}
  setTimeout(() => process.exit(0), 300);
}
