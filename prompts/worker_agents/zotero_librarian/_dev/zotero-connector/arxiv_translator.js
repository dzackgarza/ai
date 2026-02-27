#!/usr/bin/env node
/**
 * arXiv translator CLI - wraps Zotero's arXiv.org translator
 * 
 * Usage: node arxiv_translator.js <arxiv_id>
 * 
 * Outputs JSON item data that can be imported into Zotero
 */

const https = require('https');
const { DOMParser } = require('xmldom');

// Read the translator file
const fs = require('fs');
const path = require('path');

const translatorPath = path.join(__dirname, 'arXiv.org.js');
const translatorCode = fs.readFileSync(translatorPath, 'utf-8');

// Extract JavaScript portion (skip JSON header)
const jsonHeaderEnd = translatorCode.indexOf('}\n\n/*');
const jsCode = translatorCode.substring(jsonHeaderEnd + 3);

// Stub implementations for Zotero runtime
const ZU = {
    trimInternal: (str) => str ? str.trim().replace(/\s+/g, ' ') : '',
    strToISO: (str) => {
        if (!str) return '';
        const date = new Date(str);
        return date.toISOString().split('T')[0];
    },
    cleanAuthor: (name, type, usePrefix) => {
        const parts = name.trim().split(',');
        if (parts.length === 2) {
            return {
                firstName: parts[1].trim(),
                lastName: parts[0].trim(),
                creatorType: type || 'author'
            };
        }
        const words = name.trim().split(/\s+/);
        if (words.length > 1) {
            const lastName = words.pop();
            return {
                firstName: words.join(' '),
                lastName: lastName,
                creatorType: type || 'author'
            };
        }
        return {
            firstName: '',
            lastName: name.trim(),
            creatorType: type || 'author'
        };
    }
};

// Global results array
const results = [];

const Zotero = {
    Item: function(itemType) {
        this.itemType = itemType;
        this.title = '';
        this.creators = [];
        this.date = '';
        this.abstractNote = '';
        this.notes = [];
        this.tags = [];
        this.url = '';
        this.DOI = '';
        this.extra = '';
        this.publisher = '';
        this.number = '';
        this.archiveID = '';
        this.volume = '';
        this.issue = '';
        this.pages = '';
        this.ISSN = '';
        this.publicationTitle = '';
        this.journalAbbreviation = '';
        this.attachments = [];
        
        this.complete = function() {
            results.push(this);
        };
    },
    loadTranslator: function(type) {
        // Stub for DOI lookup
        return {
            setTranslator: () => {},
            setSearch: () => {},
            setHandler: () => {},
            translate: () => {}
        };
    }
};

// HTTP request helper
function requestText(url) {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => resolve(data));
            res.on('error', reject);
        });
    });
}

async function requestAtom(url) {
    const text = await requestText(url);
    return new DOMParser().parseFromString(text, 'application/xml');
}

// Evaluate the translator code
eval(jsCode);

// Main function
async function fetchArxivMetadata(arxivId) {
    const apiURL = `https://export.arxiv.org/api/query?id_list=${encodeURIComponent(arxivId)}&max_results=1`;
    const doc = await requestAtom(apiURL);
    
    // Create stubs for text() and attr() functions
    global.text = function(parent, selector) {
        const el = parent.querySelector(selector);
        return el ? el.textContent : '';
    };
    
    global.attr = function(parent, selector, attr) {
        const el = parent.querySelector(selector);
        return el ? el.getAttribute(attr) : '';
    };
    
    // Parse the entry
    const entries = doc.querySelectorAll('feed > entry');
    if (entries.length === 0) {
        console.error(JSON.stringify({error: 'No entries found for arXiv ID: ' + arxivId}));
        process.exit(1);
    }
    
    parseSingleEntry(entries[0]);
    
    // Output result as JSON
    console.log(JSON.stringify(results[0], null, 2));
}

// Run
const arxivId = process.argv[2];
if (!arxivId) {
    console.error(JSON.stringify({error: 'Usage: node arxiv_translator.js <arxiv_id>'}));
    process.exit(1);
}

fetchArxivMetadata(arxivId).catch(err => {
    console.error(JSON.stringify({error: err.message}));
    process.exit(1);
});
