/**
 * Claude Artifact Saver - Content Script
 * Detekuje a pridáva save tlačítka k artifacts
 */

console.log('🚀 Claude Artifact Saver - Loaded');

const CONFIG = {
    serverUrl: 'http://localhost:8765',
    checkInterval: 2000, // Check každé 2 sekundy
    projectRoot: 'D:/NEX_Automat_v2.0'
};

class ArtifactSaver {
    constructor() {
        this.processedArtifacts = new Set();
        this.serverAvailable = false;

        this.init();
    }

    async init() {
        console.log('🔧 Inicializujem Artifact Saver...');

        // Kontrola servera
        await this.checkServer();

        if (this.serverAvailable) {
            console.log('✅ Server je dostupný');
            this.startObserving();
        } else {
            console.warn('⚠️ Artifact server nie je dostupný na', CONFIG.serverUrl);
            console.warn('   Spusti: python artifact-server.py');
        }
    }

    async checkServer() {
        try {
            const response = await fetch(`${CONFIG.serverUrl}/ping`, {
                method: 'GET',
                mode: 'cors'
            });

            this.serverAvailable = response.ok;
            return response.ok;
        } catch (error) {
            console.warn('Server check failed:', error);
            this.serverAvailable = false;
            return false;
        }
    }

    startObserving() {
        // Observer pre zmeny v DOM
        const observer = new MutationObserver((mutations) => {
            this.detectArtifacts();
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        // Prvá detekcia
        this.detectArtifacts();

        // Pravidelná kontrola (fallback)
        setInterval(() => this.detectArtifacts(), CONFIG.checkInterval);

        console.log('👀 Sledujem artifacts...');
    }

    detectArtifacts() {
        // Hľadaj artifact elementy (môže sa líšiť podľa Claude UI)
        const artifactSelectors = [
            'pre code',                    // Code blocks
            '[data-testid="code-block"]',  // Možný selector
            '.code-block',                 // Generic
            'article pre'                  // Article code blocks
        ];

        let foundArtifacts = [];

        for (const selector of artifactSelectors) {
            const elements = document.querySelectorAll(selector);
            foundArtifacts.push(...elements);
        }

        foundArtifacts.forEach(artifact => {
            const artifactId = this.getArtifactId(artifact);

            if (!this.processedArtifacts.has(artifactId)) {
                this.addSaveButton(artifact, artifactId);
                this.processedArtifacts.add(artifactId);
            }
        });
    }

    getArtifactId(element) {
        // Vytvor unikátne ID pre artifact
        const content = element.textContent.substring(0, 50);
        return `artifact_${this.hashCode(content)}`;
    }

    hashCode(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash).toString(36);
    }

    addSaveButton(artifact, artifactId) {
        // Nájdi container
        let container = artifact.closest('pre') || artifact.parentElement;

        if (!container) return;

        // Check či už nemá save button
        if (container.querySelector('.artifact-save-btn')) return;

        // Vytvor save button
        const saveBtn = document.createElement('button');
        saveBtn.className = 'artifact-save-btn';
        saveBtn.innerHTML = '💾 Uložiť';
        saveBtn.title = 'Uložiť artifact do projektu';

        saveBtn.onclick = (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.saveArtifact(artifact, artifactId);
        };

        // Pridaj button (pozícia závisí od štruktúry)
        if (container.style.position !== 'relative') {
            container.style.position = 'relative';
        }

        container.appendChild(saveBtn);
    }

    async saveArtifact(artifact, artifactId) {
        // Získaj kód
        const code = artifact.textContent;

        if (!code || code.trim().length === 0) {
            this.showNotification('❌ Žiadny obsah na uloženie', 'error');
            return;
        }

        // Opýtaj sa na filename
        const filename = this.promptForFilename();

        if (!filename) {
            this.showNotification('❌ Zrušené', 'warning');
            return;
        }

        // Validácia filename
        if (!this.validateFilename(filename)) {
            this.showNotification('❌ Neplatný názov súboru', 'error');
            return;
        }

        try {
            // Pošli na server
            const response = await fetch(`${CONFIG.serverUrl}/save-artifact`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filename: filename,
                    content: code
                })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const result = await response.json();

            this.showNotification(
                `✅ Uložené: ${result.filename} (${this.formatBytes(result.size)})`,
                'success'
            );

            console.log('✅ Artifact uložený:', result);

        } catch (error) {
            console.error('❌ Chyba pri ukladaní:', error);
            this.showNotification(`❌ Chyba: ${error.message}`, 'error');
        }
    }

    promptForFilename() {
        const defaultPath = 'tools/';
        const filename = prompt(
            'Zadaj názov súboru (relatívna cesta k projektu):',
            defaultPath + 'script.py'
        );

        return filename ? filename.trim() : null;
    }

    validateFilename(filename) {
        // Bezpečnostné kontroly
        if (filename.includes('..')) return false;
        if (filename.startsWith('/') || filename.startsWith('\\')) return false;
        if (filename.includes('//') || filename.includes('\\\\')) return false;

        return true;
    }

    showNotification(message, type = 'info') {
        // Vytvor notifikáciu
        const notification = document.createElement('div');
        notification.className = `artifact-notification artifact-notification-${type}`;
        notification.textContent = message;

        document.body.appendChild(notification);

        // Animácia
        setTimeout(() => notification.classList.add('show'), 10);

        // Odstránenie
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    formatBytes(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }
}

// Inicializuj po načítaní stránky
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new ArtifactSaver();
    });
} else {
    new ArtifactSaver();
}