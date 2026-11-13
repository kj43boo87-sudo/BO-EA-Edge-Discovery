// ==UserScript==
// @name         ChatGPT & Scout & Champ Persona Controller
// @namespace    http://tampermonkey.net/
// @version      5.1
// @description  ChatGPT専用タスクバー：Gemini版と完全同等のUIデザインおよび自動受信・ログ同期機能
// @match        https://chatgpt.com/*
// @grant        GM_xmlhttpRequest
// @grant        GM_addStyle
// @connect      127.0.0.1
// ==/UserScript==

(function () {
    'use strict';

    const personas = [
        { id: 'scout', name: 'Scout', icon: '🔭', filename: 'Scout_Role_Prompt_v2_2026-09-28' },
        { id: 'champ', name: 'Champ', icon: '🛡️', filename: 'Champ_Role_Prompt_v2_2026-09-28' }
    ];
    const projectKey = id => `ai_persona_project_url_chatgpt_${id}`;
    const chatKey = id => `active_chat_id_chatgpt_${id}`;

    let currentAgent = localStorage.getItem('active_chat_agent_chatgpt_type') || 'scout';
    if (!personas.some(p => p.id === currentAgent)) currentAgent = 'scout';

    let currentChatId = localStorage.getItem(chatKey(currentAgent)) || `${currentAgent}_session_${Date.now()}`;
    localStorage.setItem(chatKey(currentAgent), currentChatId);

    GM_addStyle(`
        #ai-persona-panel {
            position: fixed; top: 105px; right: 12px; z-index: 99999;
            background: #fff; color: #202124; padding: 6px; border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,.15);
            max-width: min(380px, calc(100vw - 24px)); font-family: sans-serif;
        }
        #ai-persona-panel .ai-toolbar, #ai-persona-panel .ai-details {
            display: flex; gap: 7px; align-items: center; flex-wrap: wrap;
        }
        #ai-persona-panel .ai-details { display: none; margin-top: 8px; }
        #ai-persona-panel .ai-details.open { display: flex; }
        #ai-persona-panel button, #ai-persona-panel select { font-family: inherit; cursor: pointer; }
        #ai-persona-panel .ai-icon-btn {
            background: #f1f3f4; border: 2px solid transparent; border-radius: 50%;
            width: 36px; height: 36px; font-size: 18px; display: flex;
            align-items: center; justify-content: center;
        }
        #ai-persona-panel .ai-icon-btn.active { border-color: #10a37f; background: #e6f4ea; }
        #ai-persona-panel .ai-toggle-btn {
            background: transparent; border: none; width: 30px; height: 36px; font-size: 17px;
        }
        #ai-persona-panel .ai-status-badge {
            font-size: 11px; color: #5f6368; max-width: 160px;
            overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
        }
        #ai-persona-panel .ai-register-select { padding: 5px; border-radius: 6px; }
        #ai-persona-panel .ai-register-btn, #ai-persona-panel .ai-prompt-btn,
        #ai-persona-panel .ai-sync-btn {
            border: none; border-radius: 6px; padding: 8px 10px;
            color: #fff; font-size: 12px; font-weight: bold;
        }
        #ai-persona-panel .ai-register-btn { background: #5f6368; }
        #ai-persona-panel .ai-prompt-btn { background: #34a853; }
        #ai-persona-panel .ai-sync-btn { background: #10a37f; }
    `);

    const panel = document.createElement('div');
    panel.id = 'ai-persona-panel';
    const toolbar = document.createElement('div');
    toolbar.className = 'ai-toolbar';
    panel.appendChild(toolbar);

    const details = document.createElement('div');
    details.className = 'ai-details';

    const statusBadge = document.createElement('span');
    statusBadge.className = 'ai-status-badge';
    statusBadge.textContent = '待機中（キュー監視中）';

    const currentPersona = () => personas.find(p => p.id === currentAgent);
    const projectUrl = id => localStorage.getItem(projectKey(id));

    function refreshIcons() {
        panel.querySelectorAll('.ai-icon-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.agent === currentAgent);
        });
    }


    function getEditor(){return document.querySelector('#prompt-textarea');}
    function collectMessages(){
        return [...document.querySelectorAll('[data-message-author-role]')].map((node,index)=>{
            const role=node.getAttribute('data-message-author-role');const content=node.querySelector('.markdown, .whitespace-pre-wrap')||node;
            const native=node.getAttribute('data-message-id')||node.closest('[data-message-id]')?.getAttribute('data-message-id');
            return {id:String(index).padStart(6,'0')+'_'+(native||role),role,text:content.innerText.trim()};
        }).filter(m=>['user','assistant'].includes(m.role)&&m.text);
    }

    const SERVER='http://127.0.0.1:5000';
    function api(path,body){return new Promise((resolve,reject)=>GM_xmlhttpRequest({method:body?'POST':'GET',url:SERVER+path,headers:{'Content-Type':'application/json; charset=utf-8'},...(body?{data:JSON.stringify(body)}:{}),timeout:15000,onload(r){try{const d=JSON.parse(r.responseText);if(r.status<200||r.status>=300)throw Error(d.message||'HTTP '+r.status);resolve(d);}catch(e){reject(e);}},onerror(){reject(Error('サーバー接続失敗'));},ontimeout(){reject(Error('タイムアウト'));}}));}
    const tabId=crypto.randomUUID();
    let pollBusy=false,syncBusy=false,lastSnapshot='',stableSnapshot='',stableSince=0;
    function refreshChat(){
        const key=chatKey(currentAgent)+'_'+location.pathname;
        currentChatId=localStorage.getItem(key);
        if(!currentChatId){currentChatId=currentAgent+'_chat_'+crypto.randomUUID();localStorage.setItem(key,currentChatId);}
        statusBadge.title='Chat ID: '+currentChatId;
    }
    function correctPage(){const u=projectUrl(currentAgent);return !!u&&new URL(u).pathname===location.pathname&&document.visibilityState==='visible';}
    function query(){return '?agent='+encodeURIComponent(currentAgent)+'&chat_id='+encodeURIComponent(currentChatId);}
    async function pollQueue(){
        refreshChat();if(pollBusy||!correctPage())return;
        // A short per-chat lease prevents duplicate insertion by multiple visible tabs.
        const leaseKey='trace_receiver_'+currentChatId,lease=JSON.parse(localStorage.getItem(leaseKey)||'null');
        if(lease&&lease.owner!==tabId&&Date.now()-lease.time<12000)return;
        localStorage.setItem(leaseKey,JSON.stringify({owner:tabId,time:Date.now()}));
        pollBusy=true;const agent=currentAgent,chat=currentChatId;
        try{const d=await api('/get_pending_message'+query());if(!d.message)return;
            if(agent!==currentAgent||chat!==currentChatId||!correctPage())return;
            const deliveredKey='trace_delivered_'+d.message_id;
            if(localStorage.getItem(deliveredKey)){await api('/ack_message',{agent,chat_id:chat,message_id:d.message_id});return;}
            const editor=getEditor();
            if(!editor||editor.getAttribute('aria-disabled')==='true'||editor.getAttribute('contenteditable')==='false'||editorText(editor).trim()||isGenerating()){
                statusBadge.textContent='受信待機（入力欄が空くまで保持）';return;
            }
            editor.focus();const ok=document.execCommand('insertText',false,d.message);
            if(!ok){if(editor.tagName==='TEXTAREA'){const setter=Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set;setter.call(editor,d.message);}else editor.textContent=d.message;}
            editor.dispatchEvent(new Event('input',{bubbles:true}));
            await new Promise(r=>setTimeout(r,150));
            if(editorText(editor).replace(/\r/g,'').trim()!==d.message.replace(/\r/g,'').trim())throw Error('入力確認失敗。キューは保持されています');
            localStorage.setItem(deliveredKey,'1');await api('/ack_message',{agent,chat_id:chat,message_id:d.message_id});statusBadge.textContent='受信・入力確認済み（送信は手動）';
        }catch(e){statusBadge.textContent=e.message;console.error('[Omni Trace]',e);}finally{pollBusy=false;}
    }
    function editorText(e){return e.tagName==='TEXTAREA'?e.value:e.innerText;}
    function isGenerating(){return !!document.querySelector('button[data-testid="stop-button"],button[aria-label*="Stop"],button[aria-label*="停止"],button[aria-label*="回答を停止"]');}
    async function syncLogs(manual=false){
        refreshChat();if(syncBusy||!correctPage())return;
        if(isGenerating()){if(manual)alert('回答生成中です。完了後に同期します。');return;}
        const messages=collectMessages();if(!messages.length){if(manual)alert('会話要素を取得できません。画面全体の保存は行いません。');return;}
        const snapshot=JSON.stringify({agent:currentAgent,chat_id:currentChatId,messages});
        if(!manual){if(snapshot!==stableSnapshot){stableSnapshot=snapshot;stableSince=Date.now();return;}if(Date.now()-stableSince<6000||snapshot===lastSnapshot)return;}
        syncBusy=true;
        try{const d=await api('/append',JSON.parse(snapshot));lastSnapshot=snapshot;statusBadge.textContent=`同期: 新規${d.added} 更新${d.updated} 同一${d.unchanged}`;if(manual)alert(statusBadge.textContent);}catch(e){statusBadge.textContent=e.message;if(manual)alert(e.message);}finally{syncBusy=false;}
    }
    setInterval(()=>{pollQueue();syncLogs();},3000);

    personas.forEach(persona => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'ai-icon-btn';
        btn.dataset.agent = persona.id;
        btn.textContent = persona.icon;
        btn.title = `${persona.name} チャットを開く`;
        btn.addEventListener('click', () => {
            const target = projectUrl(persona.id);
            if (!target) {
                statusBadge.textContent = `${persona.name} 未登録`;
                alert(`${persona.name} のチャット画面を開き、下の「⚙️」を開いて「📍 現在画面を登録」してください。`);
                return;
            }
            currentAgent = persona.id;
            refreshChat();
            localStorage.setItem('active_chat_agent_chatgpt_type', currentAgent);
            localStorage.setItem(chatKey(currentAgent), currentChatId);
            refreshIcons();
            if (location.href === target) {
                statusBadge.textContent = `${persona.name} 表示中`;
            } else {
                location.assign(target);
            }
        });
        toolbar.appendChild(btn);
    });

    refreshIcons();

    // Codex Desktop uses the existing local registration bridge, not browser DOM.
    const codexSyncBtn = document.createElement('button');
    codexSyncBtn.type = 'button';
    codexSyncBtn.className = 'ai-icon-btn';
    codexSyncBtn.id = 'codex-desktop-sync';
    codexSyncBtn.textContent = '🧩🔄';
    codexSyncBtn.style.width = '58px';
    codexSyncBtn.style.borderRadius = '18px';
    codexSyncBtn.title = 'Codex全ログ同期（デスクトップ版・チャット登録画面）';
    codexSyncBtn.setAttribute('aria-label', codexSyncBtn.title);
    codexSyncBtn.addEventListener('click', () => {
        const opened = window.open('http://127.0.0.1:5001/', '_blank', 'noopener,noreferrer');
        if (opened) opened.opener = null;
        statusBadge.textContent = 'Codex同期：登録画面で対象チャットを選択';
        statusBadge.title = '接続できない場合はcodex-desktop-bridge/start-background.ps1を起動してください。登録済みチャットは自動同期されます。';
    });
    toolbar.appendChild(codexSyncBtn);
    const toggleBtn = document.createElement('button');
    toggleBtn.type = 'button';
    toggleBtn.className = 'ai-toggle-btn';
    toggleBtn.textContent = '⚙️';
    toggleBtn.title = '設定・手動操作';
    toggleBtn.addEventListener('click', () => details.classList.toggle('open'));
    toolbar.appendChild(toggleBtn);

    details.appendChild(statusBadge);
    const idBox=document.createElement('input');idBox.readOnly=true;idBox.title='送信先Chat ID（クリックでコピー）';idBox.style.width='280px';
    idBox.addEventListener('click',()=>navigator.clipboard.writeText(currentChatId));details.appendChild(idBox);
    setInterval(()=>{refreshChat();idBox.value=currentChatId;},1000);


    const registerSelect = document.createElement('select');
    registerSelect.className = 'ai-register-select';
    personas.forEach(persona => {
        const option = document.createElement('option');
        option.value = persona.id;
        option.textContent = persona.name;
        registerSelect.appendChild(option);
    });
    registerSelect.value = currentAgent;
    details.appendChild(registerSelect);

    const registerBtn = document.createElement('button');
    registerBtn.type = 'button';
    registerBtn.className = 'ai-register-btn';
    registerBtn.textContent = '📍 現在画面を登録';
    registerBtn.addEventListener('click', () => {
        const persona = personas.find(p => p.id === registerSelect.value);
        const url = new URL(location.href);
        if (!url.hostname.includes('chatgpt.com')) {
            alert('ChatGPTの画面で実行してください。');
            return;
        }
        localStorage.setItem(projectKey(persona.id), url.href);
        currentAgent = persona.id;
        localStorage.setItem('active_chat_agent_chatgpt_type', currentAgent);
        currentChatId = localStorage.getItem(chatKey(currentAgent)) || `${currentAgent}_session_${Date.now()}`;
        localStorage.setItem(chatKey(currentAgent), currentChatId);
        refreshIcons();
        statusBadge.textContent = `${persona.name} 登録完了`;
    });
    details.appendChild(registerBtn);

    const promptBtn = document.createElement('button');
    promptBtn.type = 'button';
    promptBtn.className = 'ai-prompt-btn';
    promptBtn.textContent = '📋 プロンプト読込';
    promptBtn.addEventListener('click', () => {
        const persona = currentPersona();
        GM_xmlhttpRequest({
            method: 'GET',
            url: `http://127.0.0.1:5000/get_role_prompt?agent=${encodeURIComponent(persona.id)}&filename=${encodeURIComponent(persona.filename)}`,
            onload(response) {
                try {
                    const res = JSON.parse(response.responseText);
                    if (res.status === 'ok') {
                        navigator.clipboard.writeText(res.prompt);
                        alert(`${persona.name} のプロンプトをクリップボードにコピーしました！`);
                    } else {
                        alert(`取得エラー: ${res.message}`);
                    }
                } catch(e) { alert('解析エラー'); }
            }
        });
    });
    details.appendChild(promptBtn);

    const syncBtn = document.createElement('button');
    syncBtn.type = 'button';
    syncBtn.className = 'ai-sync-btn';
    syncBtn.textContent = '🔄 全ログ同期';
    syncBtn.addEventListener('click', () => syncLogs(true));
    details.appendChild(syncBtn);
    panel.appendChild(details);

    refreshChat();
    function mount() {
        if (!document.body || document.getElementById(panel.id)) return;
        document.body.appendChild(panel);
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, { once: true });
    else mount();
})();