# 📊 Simple CRM - GitHub Pages Version

A browser-based Customer Relationship Manager using localStorage. No backend required!

[![Deploy to GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-blue.svg)](https://pages.github.com/)
[![No Backend Required](https://img.shields.io/badge/Backend-None-green.svg)]()

## ✨ Features

- ✅ **Client Management** - Add, edit, delete clients
- ✅ **Amount Tracking** - Track deal values in AED
- ✅ **Interaction Logs** - Record calls, emails, meetings, notes
- ✅ **Lead Status** - New, Contacted, Uncontactable, Under Nego, Fully Paid, Pullout
- ✅ **Priority Levels** - High, Medium, Low
- ✅ **Filtering & Search** - Filter by status, priority, search by name/email
- ✅ **Sorting** - By date, name, or priority
- ✅ **100% Browser-Based** - No server needed!
- ✅ **Works Offline** - Once loaded, works without internet

## 🚀 Quick Start

### Option 1: Use Directly (No Installation)

Just open `index.html` in your browser! That's it!

### Option 2: Deploy to GitHub Pages

1. **Create a GitHub repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/simple-crm.git
   git push -u origin main
   ```

2. **Enable GitHub Pages**
   - Go to your repository on GitHub
   - Click **Settings** → **Pages**
   - Under "Source", select **main branch**
   - Click **Save**
   - Your CRM will be live at: `https://YOUR_USERNAME.github.io/simple-crm/`

## 📁 Files Needed

```
simple-crm/
├── index.html       # Main HTML file
├── style.css        # Styles
├── script.js        # JavaScript (localStorage)
└── README.md        # This file
```

**That's all you need!** No Python, no database, no server!

## 💾 How Data is Stored

- **Storage:** Browser's localStorage
- **Location:** Stored locally in your browser
- **Persistence:** Data persists until you clear browser data
- **Privacy:** Data never leaves your computer
- **Limit:** ~5-10MB storage

## ⚠️ Important Notes

### Data is Browser-Specific
- Data is saved **only** in the browser you're using
- Different browsers = different data
- Incognito/Private mode = data lost when closed

### No Cloud Sync
- Data is NOT synced across devices
- To backup: Export your browser data
- To share: Each user has their own data

### Backup Your Data

To backup your data:
1. Open browser console (F12)
2. Type: `localStorage.getItem('crmClients')`
3. Copy the output
4. Save to a text file

To restore:
1. Open console (F12)
2. Type: `localStorage.setItem('crmClients', 'PASTE_YOUR_DATA_HERE')`
3. Refresh page

## 🌐 Browser Compatibility

Works on:
- ✅ Chrome/Edge (Recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Opera
- ✅ Any modern browser

## 🔄 Upgrading from Flask Version

If you have the Flask version and want to switch:

1. Keep: `index.html`, `style.css`
2. Replace: `script.js` with this version
3. Delete: `app.py`, `requirements.txt`, `view_database.py`, `instance/`
4. Deploy to GitHub Pages

**Note:** Data from Flask database won't automatically transfer.

## 📝 License

Free to use for personal or commercial projects.

## 🤝 Contributing

Feel free to fork and improve!

---

**No Backend. No Database. Just Works!** ✨
