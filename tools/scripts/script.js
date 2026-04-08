(function () {
  const KNOWN_TXT_FILES = [
    '../../working-documents/genesis_restorative_translation.txt',
    '../../working-documents/exodus_to_ecclesiastes_restorative_translation.txt',
    '../../working-documents/rest_of_old_testament_restorative_translation.txt',
    '../../working-documents/matthew_restorative_translation.txt',
    '../../working-documents/mark_restorative_translation.txt',
    '../../working-documents/luke_restorative_translation.txt',
    '../../working-documents/john_restorative_translation.txt',
    '../../working-documents/acts_restorative_translation.txt',
    '../../working-documents/rest_of_new_testament_restorative_translation.txt'
  ];

  const state = {
    loadedFiles: [],
    parsedBooks: []
  };

  const fileInput = document.getElementById('fileInput');
  const loadKnownBtn = document.getElementById('loadKnown');
  const exportJsonBtn = document.getElementById('exportJsonBtn');
  const exportEbookBtn = document.getElementById('exportEbookBtn');
  const exportZipBtn = document.getElementById('exportZipBtn');
  const convertJsonBtn = document.getElementById('convertJsonBtn');
  const logEl = document.getElementById('log');

  function log(msg) {
    logEl.textContent += `\n${msg}`;
    logEl.scrollTop = logEl.scrollHeight;
  }

  function resetLog(msg) {
    logEl.textContent = msg || 'Ready.';
  }

  function slugify(value) {
    return value
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)+/g, '');
  }

  function saveBlob(filename, blob) {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
      URL.revokeObjectURL(a.href);
      a.remove();
    }, 200);
  }

  function parseBibleText(raw, sourceName) {
    const lines = raw.replace(/\r/g, '').split('\n');
    const books = [];

    let currentBook = null;
    let currentChapter = null;
    let currentVerse = null;

    for (const originalLine of lines) {
      const line = originalLine.trim();
      if (!line) continue;

      const headingMatch = line.match(/^([1-3]?\s?[A-Za-z][A-Za-z'\-\s]+?)\s+(\d+)$/);
      if (headingMatch) {
        const bookName = headingMatch[1].trim().replace(/\s+/g, ' ');
        const chapterNumber = Number(headingMatch[2]);

        if (!currentBook || currentBook.book !== bookName) {
          currentBook = { book: bookName, chapters: [] };
          books.push(currentBook);
        }

        currentChapter = { chapter: chapterNumber, verses: [] };
        currentBook.chapters.push(currentChapter);
        currentVerse = null;
        continue;
      }

      const verseMatch = line.match(/^(\d+)\.\s*(.+)$/);
      if (verseMatch && currentChapter) {
        currentVerse = {
          verse: Number(verseMatch[1]),
          text: verseMatch[2].trim()
        };
        currentChapter.verses.push(currentVerse);
        continue;
      }

      if (currentVerse) {
        currentVerse.text += ` ${line}`;
      } else {
        log(`Skipped line in ${sourceName}: ${line.slice(0, 120)}`);
      }
    }

    return books;
  }

  function normalizeBooks(books) {
    return books
      .map((book) => ({
        book: book.book,
        chapters: book.chapters
          .sort((a, b) => a.chapter - b.chapter)
          .map((chapter) => ({
            chapter: chapter.chapter,
            verses: chapter.verses.sort((a, b) => a.verse - b.verse)
          }))
      }))
      .sort((a, b) => a.book.localeCompare(b.book));
  }

  function buildPublishingJson(books) {
    return {
      metadata: {
        translation: 'The Way Translation',
        generatedAtUtc: new Date().toISOString(),
        exportFormat: 'publishing-v1'
      },
      books: normalizeBooks(books)
    };
  }

  function buildEbookText(books) {
    const lines = [];
    for (const book of normalizeBooks(books)) {
      lines.push(book.book.toUpperCase());
      lines.push('');
      for (const chapter of book.chapters) {
        lines.push(`Chapter ${chapter.chapter}`);
        for (const verse of chapter.verses) {
          lines.push(`${verse.verse}. ${verse.text}`);
        }
        lines.push('');
      }
      lines.push('');
    }
    return lines.join('\n');
  }

  function parseAnyJsonShape(obj) {
    if (obj && Array.isArray(obj.books)) {
      return obj.books;
    }

    if (obj && typeof obj === 'object') {
      return Object.entries(obj).map(([book, chaptersValue]) => {
        const chapters = [];
        if (Array.isArray(chaptersValue)) {
          chaptersValue.forEach((chapterObj, idx) => {
            if (chapterObj && Array.isArray(chapterObj.verses)) {
              chapters.push({
                chapter: Number(chapterObj.chapter || idx + 1),
                verses: chapterObj.verses.map((v, vi) => ({
                  verse: Number(v.verse || vi + 1),
                  text: String(v.text || v)
                }))
              });
            }
          });
        } else if (chaptersValue && typeof chaptersValue === 'object') {
          Object.entries(chaptersValue).forEach(([chapterNum, versesObj]) => {
            const verses = [];
            if (Array.isArray(versesObj)) {
              versesObj.forEach((v, i) => verses.push({ verse: i + 1, text: String(v.text || v) }));
            } else if (versesObj && typeof versesObj === 'object') {
              Object.entries(versesObj).forEach(([verseNum, text]) => {
                verses.push({ verse: Number(verseNum), text: String(text) });
              });
            }
            chapters.push({ chapter: Number(chapterNum), verses });
          });
        }
        return { book, chapters };
      });
    }

    throw new Error('Unsupported JSON shape.');
  }

  function combineBooks(bookGroups) {
    const map = new Map();

    for (const group of bookGroups) {
      for (const book of group) {
        if (!map.has(book.book)) {
          map.set(book.book, { book: book.book, chapters: [] });
        }
        const targetBook = map.get(book.book);
        for (const chapter of book.chapters) {
          const existingChapter = targetBook.chapters.find((c) => c.chapter === chapter.chapter);
          if (!existingChapter) {
            targetBook.chapters.push({ chapter: chapter.chapter, verses: [...chapter.verses] });
          } else {
            const verseMap = new Map(existingChapter.verses.map((v) => [v.verse, v]));
            for (const verse of chapter.verses) {
              verseMap.set(verse.verse, verse);
            }
            existingChapter.verses = Array.from(verseMap.values());
          }
        }
      }
    }

    return Array.from(map.values());
  }

  async function loadKnownFiles() {
    resetLog('Loading known TXT files...');
    const loaded = [];

    for (const path of KNOWN_TXT_FILES) {
      try {
        const res = await fetch(path);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const text = await res.text();
        loaded.push({ name: path.split('/').pop(), kind: 'txt', text });
        log(`Loaded: ${path}`);
      } catch (err) {
        log(`Could not load ${path}: ${err.message}`);
      }
    }

    state.loadedFiles = loaded;
    state.parsedBooks = combineBooks(
      loaded.filter((f) => f.kind === 'txt').map((f) => parseBibleText(f.text, f.name))
    );

    log(`Done. Loaded ${loaded.length} files.`);
  }

  async function loadManualFiles(fileList) {
    resetLog('Loading selected files...');
    const loaded = [];

    for (const file of fileList) {
      const text = await file.text();
      const kind = file.name.toLowerCase().endsWith('.json') ? 'json' : 'txt';
      loaded.push({ name: file.name, kind, text });
      log(`Loaded: ${file.name}`);
    }

    state.loadedFiles = loaded;
    state.parsedBooks = combineBooks(
      loaded.filter((f) => f.kind === 'txt').map((f) => parseBibleText(f.text, f.name))
    );

    log(`Done. Loaded ${loaded.length} files.`);
  }

  function ensureTxtLoaded() {
    if (!state.parsedBooks.length) {
      throw new Error('No TXT content loaded. Use auto-load or select TXT files first.');
    }
  }

  loadKnownBtn.addEventListener('click', async () => {
    try {
      await loadKnownFiles();
    } catch (err) {
      log(`Error: ${err.message}`);
    }
  });

  fileInput.addEventListener('change', async (event) => {
    try {
      await loadManualFiles(event.target.files);
    } catch (err) {
      log(`Error: ${err.message}`);
    }
  });

  exportJsonBtn.addEventListener('click', () => {
    try {
      ensureTxtLoaded();
      const payload = buildPublishingJson(state.parsedBooks);
      saveBlob('way-translation-publishing.json', new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' }));
      log('Exported publishing JSON.');
    } catch (err) {
      log(`Error: ${err.message}`);
    }
  });

  exportEbookBtn.addEventListener('click', () => {
    try {
      ensureTxtLoaded();
      const text = buildEbookText(state.parsedBooks);
      saveBlob('way-translation-ebook.txt', new Blob([text], { type: 'text/plain;charset=utf-8' }));
      log('Exported eBook plain text.');
    } catch (err) {
      log(`Error: ${err.message}`);
    }
  });

  exportZipBtn.addEventListener('click', async () => {
    try {
      ensureTxtLoaded();
      if (!window.JSZip) throw new Error('JSZip did not load. Check network or include JSZip locally.');

      const zip = new JSZip();
      const books = normalizeBooks(state.parsedBooks);

      for (const book of books) {
        const folder = zip.folder(`books/${slugify(book.book)}`);
        const chapterFiles = [];

        for (const chapter of book.chapters) {
          const chapterText = [`${book.book} - Chapter ${chapter.chapter}`, '']
            .concat(chapter.verses.map((v) => `${v.verse}. ${v.text}`))
            .join('\n');
          const chapterName = `chapter-${String(chapter.chapter).padStart(3, '0')}.txt`;
          folder.file(chapterName, chapterText);
          chapterFiles.push(chapterText);
        }

        folder.file('book.txt', chapterFiles.join('\n\n'));
      }

      const blob = await zip.generateAsync({ type: 'blob' });
      saveBlob('way-translation-books-ebook-text.zip', blob);
      log('Exported book-folder ZIP.');
    } catch (err) {
      log(`Error: ${err.message}`);
    }
  });

  convertJsonBtn.addEventListener('click', () => {
    try {
      const jsonFiles = state.loadedFiles.filter((f) => f.kind === 'json');
      if (!jsonFiles.length) throw new Error('No JSON file loaded. Select at least one JSON file first.');

      const allBookGroups = jsonFiles.map((f) => parseAnyJsonShape(JSON.parse(f.text)));
      const payload = buildPublishingJson(combineBooks(allBookGroups));
      saveBlob('way-translation-converted-from-json.json', new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' }));
      log(`Converted ${jsonFiles.length} JSON file(s) to publishing JSON.`);
    } catch (err) {
      log(`Error: ${err.message}`);
    }
  });
})();
