import { spawn } from 'node:child_process';
import { appendFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const LOG = fileURLToPath(new URL('./drive-log.txt', import.meta.url));
const log = (s) => appendFileSync(LOG, s + '\n');
writeFileSync(LOG, '');

const ROOT = 'D:\\workspace\\zcode研究\\_excel-mcp-t1';
const XLSX = '销售流水-2026-09.xlsx';

const proc = spawn('excel-mcp-server', ['stdio'], {
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
    try { msg = JSON.parse(line); } catch { log('NON-JSON: ' + line.slice(0, 200)); continue; }
    if (msg.id !== undefined && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  }
});
proc.stderr.on('data', (d) => log('[srv-stderr] ' + d.toString().trim()));

function request(method, params, tmo = 60000) {
  const id = nextId++;
  return new Promise((resolve, reject) => {
    pending.set(id, resolve);
    proc.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method, params }) + '\n');
    setTimeout(() => { if (pending.has(id)) { pending.delete(id); reject(new Error('timeout: ' + method)); } }, tmo);
  });
}
const notify = (m, p) => proc.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: m, params: p }) + '\n');

async function call(name, args) {
  const r = await request('tools/call', { name, arguments: args });
  log(`CALL ${name} args=${JSON.stringify(args)}`);
  log(`  => isError=${r.result?.isError} content=${JSON.stringify(r.result?.content ?? r.error ?? r)}`);
  return r;
}

try {
  const init = await request('initialize', {
    protocolVersion: '2024-11-05',
    capabilities: {},
    clientInfo: { name: 'arm-b-driver', version: '1.0.0' },
  });
  log('INIT_SERVERINFO=' + JSON.stringify(init.result?.serverInfo));
  notify('notifications/initialized', {});

  const tools = await request('tools/list', {});
  const list = tools.result?.tools ?? [];
  log('TOOL_NAMES=' + list.map((t) => t.name).join(','));
  for (const t of list) log('SCHEMA ' + t.name + ' :: ' + JSON.stringify(t.inputSchema));

  await call('create_workbook', { path: XLSX, sheets: ['流水'], overwrite: true });
  await call('write_range', {
    path: XLSX, sheet: '流水', start_cell: 'A1',
    rows: [['日期', '品名', '数量', '单价', '金额']],
  });
  await call('write_range', {
    path: XLSX, sheet: '流水', start_cell: 'A2',
    rows: [
      ['2026-09-01', '笔记本', 3, 45, 135],
      ['2026-09-01', '签字笔', 20, 2.5, 50],
      ['2026-09-02', 'A4纸', 10, 18, 180],
      ['2026-09-03', '订书机', 2, 25, 50],
      ['2026-09-05', '笔记本', 5, 45, 225],
      ['2026-09-08', '便利贴', 8, 6, 48],
      ['2026-09-10', '签字笔', 15, 2.5, 37.5],
      ['2026-09-12', '文件夹', 12, 9, 108],
      ['2026-09-15', 'A4纸', 6, 18, 108],
      ['2026-09-18', '白板笔', 9, 5, 45],
      ['2026-09-22', '订书钉', 4, 8, 32],
      ['2026-09-26', '便利贴', 10, 6, 60],
    ],
  });
  await call('write_range', {
    path: XLSX, sheet: '流水', start_cell: 'E14', rows: [['=SUM(E2:E13)']],
  });
  await call('read_range', { path: XLSX, sheet: '流水' });
  await call('read_range', { path: XLSX, sheet: '流水', range: 'E14', mode: 'formulas' });
  await call('find_cells', { path: XLSX, query: 'SUM' });
  log('DRIVE_OK');
} catch (e) {
  log('DRIVE_FAIL ' + (e.stack || e.message));
} finally {
  try { proc.kill(); } catch {}
  setTimeout(() => process.exit(0), 500);
}
