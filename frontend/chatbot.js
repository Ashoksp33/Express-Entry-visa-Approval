/**
 * CanVisa AI — Atlas Visa Guide
 * Clean, lightweight, intuitive visa assistant with ready pre-questions.
 * Users can pick pre-questions with 1 click or type custom questions.
 * Supports English, Kannada, and Hindi.
 */

(function () {
    'use strict';

    // Localized UI Dictionary for the Chatbot Widget
    const CHAT_I18N = {
        en: {
            launcherText: "Ask Atlas",
            launcherTag: "Guide",
            headerTitle: "Atlas — Visa Guide",
            headerSub: "Instant Visa Rules & Answers",
            online: "ONLINE",
            startersLabel: "Pre-Questions",
            inputPlaceholder: "Ask a visa question or pick above...",
            sendTooltip: "Send Question (Enter)",
            clearTooltip: "Clear Conversation",
            resetTooltip: "Reset Position (Snap to Corner)",
            closeTooltip: "Close",
            dragHandleTitle: "Hold & drag to move window anywhere (Double-click to reset)",
            welcomeMsg: "**Hello! I am Atlas, your Visa Guide.**\n\nChoose any pre-question above or type your question below to get instant answers about visa rules, Medium Risk, and approval chances.",
            starters: [
                "Why does a profile get Medium Risk?",
                "How to move from Medium to Low Risk?",
                "What is Proof of Funds for Canada?",
                "What are Canada Express Entry requirements?",
                "What are the rules for Australia & UK?",
                "What is the Germany Opportunity Card?",
                "What factors decide my visa score?",
                "Assess my profile (Age 28, Master's, 3 yrs exp, IELTS 7.5)"
            ]
        },
        kn: {
            launcherText: "Atlas ಕೇಳಿ",
            launcherTag: "ಗೈಡ್",
            headerTitle: "Atlas — ವೀಸಾ ಗೈಡ್",
            headerSub: "ತ್ವರಿತ ವೀಸಾ ನಿಯಮಗಳು ಮತ್ತು ಉತ್ತರಗಳು",
            online: "ಸಕ್ರಿಯ",
            startersLabel: "ಸಿದ್ಧ ಪ್ರಶ್ನೆಗಳು",
            inputPlaceholder: "ವೀಸಾ ಪ್ರಶ್ನೆ ಕೇಳಿ ಅಥವಾ ಮೇಲಿನಿಂದ ಆರಿಸಿ...",
            sendTooltip: "ಪ್ರಶ್ನೆ ಕಳುಹಿಸಿ (Enter)",
            clearTooltip: "ಸಂಭಾಷಣೆ ಅಳಿಸಿ",
            resetTooltip: "ಮೂಲ ಸ್ಥಳಕ್ಕೆ ಮರುಹೊಂದಿಸಿ",
            closeTooltip: "ಮುಚ್ಚಿ",
            dragHandleTitle: "ಕಿಟಕಿಯನ್ನು ಎಲ್ಲಿಯಾದರೂ ಸರಿಸಲು ಎಳೆಯಿರಿ (ಮರುಹೊಂದಿಸಲು ಡಬಲ್ ಕ್ಲಿಕ್ ಮಾಡಿ)",
            welcomeMsg: "**ನಮಸ್ಕಾರ! ನಾನು Atlas, ನಿಮ್ಮ ವೀಸಾ ಗೈಡ್.**\n\nತ್ವರಿತ ಉತ್ತರಗಳನ್ನು ಪಡೆಯಲು ಮೇಲಿನ ಯಾವುದೇ ಪ್ರಶ್ನೆಯನ್ನು ಆರಿಸಿ ಅಥವಾ ಕೆಳಗೆ ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಟೈಪ್ ಮಾಡಿ.",
            starters: [
                "ಪ್ರೊಫೈಲ್‌ಗೆ Medium Risk ಏಕೆ ಬರುತ್ತದೆ?",
                "Medium ನಿಂದ Low Risk ಗೆ ಹೋಗುವುದು ಹೇಗೆ?",
                "ಕೆನಡಾ Proof of Funds (ಬ್ಯಾಂಕ್ ಉಳಿತಾಯ) ಎಷ್ಟು ಬೇಕು?",
                "ಕೆನಡಾ Express Entry ನಿಯಮಗಳು ಯಾವುವು?",
                "ಆಸ್ಟ್ರೇಲಿಯಾ ಮತ್ತು ಯುಕೆ ನಿಯಮಗಳು ಯಾವುವು?",
                "ಜರ್ಮನಿ Chancenkarte (ಅವಕಾಶ ಕಾರ್ಡ್) ನಿಯಮಗಳೇನು?",
                "ಫಲಿತಾಂಶ ನಿರ್ಧರಿಸುವ ಅಂಶಗಳು ಯಾವುವು?",
                "ಪ್ರೊಫೈಲ್ ಮೌಲ್ಯಮಾಪನ (Age 28, Master's, 3 yrs exp, IELTS 7.5)"
            ]
        },
        hi: {
            launcherText: "Atlas से पूछें",
            launcherTag: "गाइड",
            headerTitle: "Atlas — वीजा गाइड",
            headerSub: "तुरंत वीजा नियम एवं उत्तर",
            online: "सक्रिय",
            startersLabel: "तैयार प्रश्न",
            inputPlaceholder: "वीजा प्रश्न पूछें या ऊपर से चुनें...",
            sendTooltip: "प्रश्न भेजें (Enter)",
            clearTooltip: "बातचीत मिटाएं",
            resetTooltip: "प्रारंभिक स्थिति में रीसेट करें",
            closeTooltip: "बंद करें",
            dragHandleTitle: "विंडो को कहीं भी ले जाने के लिए ड्रैग करें (रीसेट करने के लिए डबल क्लिक करें)",
            welcomeMsg: "**नमस्ते! मैं Atlas हूँ, आपका वीजा गाइड।**\n\nतुरंत उत्तर पाने के लिए ऊपर दिए गए किसी भी प्रश्न को चुनें या नीचे अपना प्रश्न टाइप करें।",
            starters: [
                "प्रोफाइल को Medium Risk क्यों मिलता है?",
                "Medium से Low Risk में कैसे जाएं?",
                "कनाडा Proof of Funds (बैंक बैलेंस) कितना चाहिए?",
                "कनाडा Express Entry के नियम क्या हैं?",
                "ऑस्ट्रेलिया और यूके के मुख्य नियम क्या हैं?",
                "जर्मनी Chancenkarte के नियम क्या हैं?",
                "परिणाम तय करने वाले कारक क्या हैं?",
                "प्रोफाइल मूल्यांकन (Age 28, Master's, 3 yrs exp, IELTS 7.5)"
            ]
        }
    };

    // Chatbot State
    let currentLang = 'en';
    let isOpen = false;
    let isFetching = false;
    let messagesHistory = [];

    // Helper: Determine current language
    function getActiveLanguage() {
        if (typeof window.currentAppLanguage !== 'undefined' && window.currentAppLanguage) {
            return window.currentAppLanguage;
        }
        const stored = localStorage.getItem('canvisa_language');
        if (stored) return stored;
        return 'en';
    }

    // Helper: Escape HTML & format rich Markdown including tables & code
    function formatMessageText(text) {
        if (!text) return '';
        
        // Escape HTML tags to prevent XSS
        let safe = text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');

        // 1. Parse Markdown Tables before processing lines
        const tableBlockRegex = /((?:\|[^\n]+\|\r?\n){2,})/g;
        safe = safe.replace(tableBlockRegex, (tableBlock) => {
            const rows = tableBlock.trim().split(/\r?\n/).map(r => r.trim()).filter(Boolean);
            if (rows.length < 2) return tableBlock;

            // Check if second row is separator row (e.g. | :--- | :--- |)
            if (!rows[1].match(/^\|[\s:-|]+\|$/)) {
                return tableBlock;
            }

            const headerCells = rows[0].split('|').slice(1, -1).map(c => `<th>${c.trim()}</th>`).join('');
            const bodyRows = rows.slice(2).map(r => {
                const cells = r.split('|').slice(1, -1).map(c => `<td>${c.trim()}</td>`).join('');
                return `<tr>${cells}</tr>`;
            }).join('');

            return `\n<div class="cv-table-wrap"><table class="cv-table"><thead><tr>${headerCells}</tr></thead><tbody>${bodyRows}</tbody></table></div>\n`;
        });

        // 2. Bold **text**
        safe = safe.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // 3. Inline code `text`
        safe = safe.replace(/`([^`]+)`/g, '<span class="cv-code-inline">$1</span>');

        // 4. Highlight Currency & Test Scores
        safe = safe.replace(/(\b(?:IELTS\s*[\d\.]+|CLB\s*\d+|PTE\s*[\d\.]+|CAD\s*\$[\d,]+|AUD\s*\$[\d,]+|£[\d,]+(?:\s*GBP)?|€[\d,]+(?:\s*EUR)?|\$\d+[\d,]*\s*CAD)\b)/g, '<span class="cv-badge-stat">$1</span>');

        // 5. Bullet lists and paragraph formatting
        const lines = safe.split(/\r?\n/);
        let inList = false;
        let htmlLines = [];

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();

            // Pass-through table markup without wrapping in <p>
            if (line.startsWith('<div class="cv-table-wrap">') || line.startsWith('</div>') || line.startsWith('<table') || line.startsWith('</table') || line.startsWith('<tr') || line.startsWith('<td') || line.startsWith('<th')) {
                if (inList) { htmlLines.push('</ul>'); inList = false; }
                htmlLines.push(line);
                continue;
            }

            if (line.startsWith('• ') || line.startsWith('- ') || line.startsWith('* ')) {
                if (!inList) {
                    htmlLines.push('<ul>');
                    inList = true;
                }
                htmlLines.push(`<li>${line.substring(2)}</li>`);
            } else {
                if (inList) {
                    htmlLines.push('</ul>');
                    inList = false;
                }
                if (line.length > 0) {
                    htmlLines.push(`<p>${line}</p>`);
                }
            }
        }
        if (inList) htmlLines.push('</ul>');

        return htmlLines.join('');
    }

    // Build the Clean Chatbot DOM
    function initChatbotDOM() {
        if (document.getElementById('cvChatWindow')) return;

        // 1. Create Launcher Trigger
        const launcher = document.createElement('div');
        launcher.id = 'cvChatLauncher';
        launcher.className = 'cv-chat-launcher';
        launcher.innerHTML = `
            <div class="cv-chat-launcher-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 2l2.4 7.2L22 12l-7.6 2.8L12 22l-2.4-7.2L2 12l7.6-2.8z"/></svg>
                <span class="cv-chat-launcher-badge-pulse"></span>
            </div>
            <div class="cv-chat-launcher-text">
                <span id="cvLauncherLabel">Ask Atlas</span>
                <span id="cvLauncherTag" class="cv-chat-launcher-tag">Guide</span>
            </div>
        `;
        document.body.appendChild(launcher);

        // 2. Create Clean Chat Window (without unnecessary banners, tab bars, or footers)
        const win = document.createElement('div');
        win.id = 'cvChatWindow';
        win.className = 'cv-chat-window';
        win.innerHTML = `
            <!-- Header (Draggable Handle) -->
            <div class="cv-chat-header" title="Hold & drag to move window anywhere (Double click to reset)">
                <div class="cv-chat-header-brand">
                    <div class="cv-chat-avatar">A</div>
                    <div class="cv-chat-header-info">
                        <div class="cv-chat-header-title">
                            <span id="cvHeaderTitle">Atlas — Visa Guide</span>
                            <span class="cv-chat-status-pill">
                                <span class="cv-chat-status-dot"></span>
                                <span id="cvStatusText">ONLINE</span>
                            </span>
                            <span id="cvDragHandle" class="cv-chat-drag-handle" title="Hold & drag to move window anywhere (Double click to reset)">⠿ Move</span>
                        </div>
                        <div id="cvHeaderSub" class="cv-chat-header-sub">Instant Visa Rules & Answers</div>
                    </div>
                </div>
                <div class="cv-chat-header-actions">
                    <button id="cvBtnReset" class="cv-chat-btn-action" title="Reset Position (Snap to Corner)">⟲</button>
                    <button id="cvBtnClear" class="cv-chat-btn-action" title="Clear Conversation"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg></button>
                    <button id="cvBtnClose" class="cv-chat-btn-action" title="Close">✕</button>
                </div>
            </div>

            <!-- Pre-Questions Shelf (Simple & Clickable) -->
            <div class="cv-chat-starters">
                <div class="cv-chat-starters-label">
                    <span><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg></span>
                    <span id="cvStartersLabel">Pre-Questions</span>
                </div>
                <div id="cvStartersContainer" class="cv-chat-chips-scroll">
                    <!-- Populated dynamically -->
                </div>
            </div>

            <!-- Messages Area -->
            <div id="cvChatMessages" class="cv-chat-messages">
                <!-- Messages appended here -->
            </div>

            <!-- Input Area -->
            <div class="cv-chat-input-area">
                <div class="cv-chat-input-wrapper">
                    <input type="text" id="cvChatInput" class="cv-chat-input" placeholder="Ask a visa question or pick above..." autocomplete="off">
                </div>
                <button id="cvBtnSend" class="cv-chat-send-btn" title="Send Question (Enter)">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="22" y1="2" x2="11" y2="13"></line>
                        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                    </svg>
                </button>
            </div>
        `;
        document.body.appendChild(win);

        // Bind Drag & Drop for Window and Launcher
        const windowHeader = win.querySelector('.cv-chat-header');
        const winDraggable = makeDraggable(win, windowHeader, 'canvisa_chat_window_pos');

        let launcherMoved = false;
        const launcherDraggable = makeDraggable(launcher, launcher, 'canvisa_chat_launcher_pos', (didMove) => {
            if (didMove) {
                launcherMoved = true;
                setTimeout(() => { launcherMoved = false; }, 120);
            }
        });

        launcher.addEventListener('click', (e) => {
            if (launcherMoved) {
                e.preventDefault();
                e.stopPropagation();
                return;
            }
            toggleChatbot();
        });

        // Bind Header Action Buttons
        document.getElementById('cvBtnReset').addEventListener('click', (e) => {
            e.stopPropagation();
            winDraggable.resetPosition();
            launcherDraggable.resetPosition();
        });
        document.getElementById('cvBtnClose').addEventListener('click', (e) => {
            e.stopPropagation();
            closeChatbot();
        });
        document.getElementById('cvBtnClear').addEventListener('click', (e) => {
            e.stopPropagation();
            clearChatHistory();
        });
        document.getElementById('cvBtnSend').addEventListener('click', handleUserSend);
        
        const input = document.getElementById('cvChatInput');
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                handleUserSend();
            }
        });

        // Initialize Language and Starter Questions
        updateWidgetLanguage(getActiveLanguage());
        loadInitialMessages();
    }

    /**
     * Draggable helper for Widget Components
     */
    function makeDraggable(element, handle, storageKey, onDragEnd) {
        let startX = 0;
        let startY = 0;
        let initialLeft = 0;
        let initialTop = 0;
        let isDragging = false;
        let hasMoved = false;

        const saved = localStorage.getItem(storageKey);
        if (saved) {
            try {
                const parsed = JSON.parse(saved);
                if (typeof parsed.left === 'number' && typeof parsed.top === 'number') {
                    applyPosition(parsed.left, parsed.top);
                }
            } catch (err) {}
        }

        function applyPosition(x, y) {
            const rect = element.getBoundingClientRect();
            const width = rect.width || (element.id === 'cvChatWindow' ? 440 : 130);
            const height = rect.height || (element.id === 'cvChatWindow' ? 640 : 50);

            const maxLeft = Math.max(8, window.innerWidth - width - 8);
            const maxTop = Math.max(8, window.innerHeight - height - 8);

            const clampedX = Math.max(8, Math.min(x, maxLeft));
            const clampedY = Math.max(8, Math.min(y, maxTop));

            element.style.left = `${clampedX}px`;
            element.style.top = `${clampedY}px`;
            element.style.right = 'auto';
            element.style.bottom = 'auto';
            element.classList.add('cv-positioned');
            return { left: clampedX, top: clampedY };
        }

        function resetPosition() {
            element.style.left = '';
            element.style.top = '';
            element.style.right = '';
            element.style.bottom = '';
            element.classList.remove('cv-positioned');
            localStorage.removeItem(storageKey);
        }

        function onPointerDown(e) {
            if (e.type === 'mousedown' && e.button !== 0) return;
            if (e.target.closest('button') || e.target.closest('input')) return;

            const clientX = e.clientX || (e.touches && e.touches[0].clientX);
            const clientY = e.clientY || (e.touches && e.touches[0].clientY);
            if (typeof clientX !== 'number' || typeof clientY !== 'number') return;

            isDragging = true;
            hasMoved = false;
            startX = clientX;
            startY = clientY;

            const rect = element.getBoundingClientRect();
            initialLeft = rect.left;
            initialTop = rect.top;

            element.classList.add('cv-is-dragging');
            document.addEventListener('mousemove', onPointerMove, { passive: false });
            document.addEventListener('mouseup', onPointerUp);
            document.addEventListener('touchmove', onPointerMove, { passive: false });
            document.addEventListener('touchend', onPointerUp);
        }

        function onPointerMove(e) {
            if (!isDragging) return;
            const clientX = e.clientX || (e.touches && e.touches[0].clientX);
            const clientY = e.clientY || (e.touches && e.touches[0].clientY);
            if (typeof clientX !== 'number' || typeof clientY !== 'number') return;

            const deltaX = clientX - startX;
            const deltaY = clientY - startY;

            if (Math.abs(deltaX) > 3 || Math.abs(deltaY) > 3) {
                hasMoved = true;
                if (e.cancelable) e.preventDefault();
                applyPosition(initialLeft + deltaX, initialTop + deltaY);
            }
        }

        function onPointerUp() {
            if (!isDragging) return;
            isDragging = false;
            element.classList.remove('cv-is-dragging');
            document.removeEventListener('mousemove', onPointerMove);
            document.removeEventListener('mouseup', onPointerUp);
            document.removeEventListener('touchmove', onPointerMove);
            document.removeEventListener('touchend', onPointerUp);

            if (hasMoved) {
                const rect = element.getBoundingClientRect();
                localStorage.setItem(storageKey, JSON.stringify({ left: rect.left, top: rect.top }));
            }
            if (onDragEnd) onDragEnd(hasMoved);
        }

        handle.addEventListener('mousedown', onPointerDown);
        handle.addEventListener('touchstart', onPointerDown, { passive: true });

        return { resetPosition, applyPosition };
    }

    // Toggle Chat Window
    function toggleChatbot() {
        if (isOpen) {
            closeChatbot();
        } else {
            openChatbot();
        }
    }

    function openChatbot() {
        const win = document.getElementById('cvChatWindow');
        if (!win) return;
        win.classList.add('cv-active');
        isOpen = true;
        scrollToBottom();
        const input = document.getElementById('cvChatInput');
        if (input) setTimeout(() => input.focus(), 150);
    }

    function closeChatbot() {
        const win = document.getElementById('cvChatWindow');
        if (!win) return;
        win.classList.remove('cv-active');
        isOpen = false;
    }

    // Language Sync
    function updateWidgetLanguage(lang) {
        currentLang = ['en', 'kn', 'hi'].includes(lang) ? lang : 'en';
        const texts = CHAT_I18N[currentLang] || CHAT_I18N.en;

        const setTxt = (id, str) => {
            const el = document.getElementById(id);
            if (el) el.textContent = str;
        };

        setTxt('cvLauncherLabel', texts.launcherText);
        setTxt('cvLauncherTag', texts.launcherTag);
        setTxt('cvHeaderTitle', texts.headerTitle);
        setTxt('cvHeaderSub', texts.headerSub);
        setTxt('cvStatusText', texts.online);
        setTxt('cvStartersLabel', texts.startersLabel);

        const input = document.getElementById('cvChatInput');
        if (input) input.placeholder = texts.inputPlaceholder;

        renderStarters(texts.starters);
    }

    function renderStarters(list) {
        const container = document.getElementById('cvStartersContainer');
        if (!container || !Array.isArray(list)) return;
        container.innerHTML = '';

        list.forEach(item => {
            const chip = document.createElement('button');
            chip.className = 'cv-chip-btn';
            chip.innerHTML = `<span class="cv-chip-dot">•</span> <span>${item}</span>`;
            chip.addEventListener('click', () => {
                sendUserQuery(item);
            });
            container.appendChild(chip);
        });
    }

    // Append Message to UI (Clean: message content and time, no extra icon clutter)
    function appendMessage(role, text, scope = 'in_scope') {
        const messagesContainer = document.getElementById('cvChatMessages');
        if (!messagesContainer) return;

        const isBot = role === 'bot';
        const msgDiv = document.createElement('div');
        msgDiv.className = `cv-msg ${isBot ? 'cv-msg-bot' : 'cv-msg-user'} ${scope === 'out_of_scope' ? 'cv-out-of-scope' : ''}`;

        const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const avatar = isBot ? (scope === 'out_of_scope' ? '!' : 'A') : 'U';

        msgDiv.innerHTML = `
            <div class="cv-msg-avatar">${avatar}</div>
            <div class="cv-msg-bubble">
                <div class="cv-msg-content">${formatMessageText(text)}</div>
                <div class="cv-msg-time">${timeStr}</div>
            </div>
        `;

        messagesContainer.appendChild(msgDiv);
        scrollToBottom();

        // Save to session history
        messagesHistory.push({ role, text, scope, time: timeStr, lang: currentLang });
        saveChatHistory();
    }

    // Typing Indicator
    function showTypingIndicator() {
        const messagesContainer = document.getElementById('cvChatMessages');
        if (!messagesContainer || document.getElementById('cvTypingIndicator')) return;

        const ind = document.createElement('div');
        ind.id = 'cvTypingIndicator';
        ind.className = 'cv-msg cv-msg-bot';
        ind.innerHTML = `
            <div class="cv-msg-avatar">A</div>
            <div class="cv-typing-indicator">
                <span class="cv-typing-dot"></span>
                <span class="cv-typing-dot"></span>
                <span class="cv-typing-dot"></span>
            </div>
        `;
        messagesContainer.appendChild(ind);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        const ind = document.getElementById('cvTypingIndicator');
        if (ind) ind.remove();
    }

    function scrollToBottom() {
        const messagesContainer = document.getElementById('cvChatMessages');
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }

    // Handle User Send Event
    function handleUserSend() {
        const input = document.getElementById('cvChatInput');
        if (!input) return;
        const text = input.value.trim();
        if (!text) return;
        input.value = '';
        sendUserQuery(text);
    }

    // Core Send Query Routine
    async function sendUserQuery(userText) {
        if (isFetching || !userText) return;

        appendMessage('user', userText);
        showTypingIndicator();
        isFetching = true;

        const sendBtn = document.getElementById('cvBtnSend');
        if (sendBtn) sendBtn.disabled = true;

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: userText,
                    lang: currentLang
                })
            });

            removeTypingIndicator();

            if (!response.ok) {
                const errText = currentLang === 'kn' 
                    ? "ಕ್ಷಮಿಸಿ, ಸರ್ವರ್‌ನಿಂದ ಉತ್ತರ ಪಡೆಯುವಾಗ ದೋಷ ಸಂಭವಿಸಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೊಮ್ಮೆ ಪ್ರಯತ್ನಿಸಿ."
                    : currentLang === 'hi'
                    ? "क्षमा करें, सर्वर से उत्तर प्राप्त करने में त्रुटि हुई। कृपया पुनः प्रयास करें।"
                    : "Sorry, an error occurred while connecting to the visa assistant. Please try again.";
                appendMessage('bot', errText, 'error');
                return;
            }

            const data = await response.json();
            const botAnswer = data.response || "No response received.";
            const scope = data.scope || "in_scope";

            appendMessage('bot', botAnswer, scope);

            // If suggested questions returned, update the starters shelf
            if (data.suggested_questions && data.suggested_questions.length > 0) {
                renderStarters(data.suggested_questions);
            }

        } catch (error) {
            removeTypingIndicator();
            console.error('[CanVisa Chatbot Error]:', error);
            const errFallback = currentLang === 'kn'
                ? "ನೆಟ್‌ವರ್ಕ್ ದೋಷ: ಸರ್ವರ್ ಸಂಪರ್ಕ ವಿಫಲವಾಗಿದೆ."
                : currentLang === 'hi'
                ? "नेटवर्क त्रुटि: सर्वर से संपर्क नहीं हो सका।"
                : "Network error: Unable to communicate with the CanVisa backend.";
            appendMessage('bot', errFallback, 'error');
        } finally {
            isFetching = false;
            if (sendBtn) sendBtn.disabled = false;
            const input = document.getElementById('cvChatInput');
            if (input) input.focus();
        }
    }

    // Session Persistence
    function saveChatHistory() {
        try {
            sessionStorage.setItem('canvisa_chat_history', JSON.stringify(messagesHistory));
        } catch (err) {}
    }

    function clearChatHistory() {
        messagesHistory = [];
        sessionStorage.removeItem('canvisa_chat_history');
        const container = document.getElementById('cvChatMessages');
        if (container) container.innerHTML = '';
        loadInitialMessages();
    }

    function loadInitialMessages() {
        const saved = sessionStorage.getItem('canvisa_chat_history');
        if (saved) {
            try {
                const parsed = JSON.parse(saved);
                if (Array.isArray(parsed) && parsed.length > 0) {
                    messagesHistory = [];
                    parsed.forEach(m => appendMessage(m.role, m.text, m.scope));
                    return;
                }
            } catch (err) {}
        }
        // If empty history, display clean welcome greeting
        const texts = CHAT_I18N[currentLang] || CHAT_I18N.en;
        appendMessage('bot', texts.welcomeMsg, 'in_scope');
    }

    // Global listener for language switchers in main app
    window.addEventListener('canvisa_lang_changed', (e) => {
        if (e.detail && e.detail.lang) {
            updateWidgetLanguage(e.detail.lang);
        }
    });

    // Expose programmatic trigger to open chat with prefilled query
    window.openAtlasChatbot = function(prefillQuery) {
        openChatbot();
        if (prefillQuery) {
            const input = document.getElementById('cvChatInput');
            if (input) {
                input.value = prefillQuery;
                input.focus();
            }
        }
    };

    // DOM Ready Initialization
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initChatbotDOM);
    } else {
        initChatbotDOM();
    }

})();
