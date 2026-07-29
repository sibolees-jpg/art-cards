/**
 * 艺术卡片 · 分析 Agent 代理(Cloudflare Worker)
 * 职责:替前端保管 DeepSeek API Key,收作品档案 → 返回 10 条公约 + 观众寄语。
 * 部署:见同目录《部署说明.md》。密钥存在 Worker 的环境变量 DEEPSEEK_KEY 里,不在代码中。
 */

const ALLOW_ORIGINS = [
  'https://sibolees-jpg.github.io',
  'http://127.0.0.1:8123',
  'http://localhost:8123',
];

const SYSTEM_PROMPT = `你是「艺术卡片」App 的驻馆分析员,服务于一个社会美育项目。用户会给你若干件艺术作品的三句话档案(背景/方式/意义),以及这位观众的兴趣画像。

你的任务:
1. 给出恰好 10 条这几件作品之间的「公约方式」——它们共同的题材、方法、材料、时代处境或精神气质。每条一句话,句首用【题材】【方法】【材料】【时代】【气质】之类的方括号标注维度。
2. 最后另起一段,写不超过 80 字的「给这位观众的话」:基于 TA 的画像和这次选择,指出 TA 兴趣里可能正在生长的方向。

铁律:
- 只依据给定档案和公认的艺术史常识,不虚构事实、不编造年代与收藏地。
- 语气克制、具体,不吹捧、不空话。
- 用中文,每条不超过 40 字。`;

export default {
  async fetch(req, env) {
    const origin = req.headers.get('Origin') || '';
    const okOrigin = ALLOW_ORIGINS.includes(origin);
    const cors = {
      'Access-Control-Allow-Origin': okOrigin ? origin : ALLOW_ORIGINS[0],
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };
    if (req.method === 'OPTIONS') return new Response(null, { headers: cors });
    if (req.method !== 'POST') return new Response('POST only', { status: 405, headers: cors });
    if (!okOrigin) return new Response('origin not allowed', { status: 403, headers: cors });

    let body;
    try { body = await req.json(); } catch (_) {
      return new Response('bad json', { status: 400, headers: cors });
    }
    const works = (body.works || []).slice(0, 8); // 最多 8 件,防滥用
    if (works.length < 2) return new Response('need >=2 works', { status: 400, headers: cors });

    const profile = body.profile || {};
    const userMsg =
      '这位观众的画像:核心关怀=' + (profile.concerns || []).join('、') +
      ';共收藏 ' + (profile.n || '?') + ' 件,其中爆灯(最爱)' + (profile.nf || 0) + ' 件。\n\n' +
      'TA 这次选中的作品:\n\n' +
      works.map(w =>
        '《' + w.t + '》' + (w.a || '') + '(' + (w.y || '') + ')\n' +
        '背景:' + (w.bg || '') + '\n方式:' + (w.how || '') + '\n意义:' + (w.why || '')
      ).join('\n\n');

    const r = await fetch('https://api.deepseek.com/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + env.DEEPSEEK_KEY,
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        max_tokens: 900,
        temperature: 0.8,
        messages: [
          { role: 'system', content: SYSTEM_PROMPT },
          { role: 'user', content: userMsg },
        ],
      }),
    });
    if (!r.ok) {
      return new Response(JSON.stringify({ error: 'upstream ' + r.status }), {
        status: 502, headers: { ...cors, 'Content-Type': 'application/json' },
      });
    }
    const data = await r.json();
    const text = (((data.choices || [])[0] || {}).message || {}).content || '';
    return new Response(JSON.stringify({ text }), {
      headers: { ...cors, 'Content-Type': 'application/json' },
    });
  },
};
