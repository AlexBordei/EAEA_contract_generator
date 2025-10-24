# ⚡ Quick Start - Contract Automation System

## 🎯 Everything You Need to Know in 2 Minutes

---

## 🚀 Access the System

```
http://localhost:8000
```

---

## ✨ What's New & Automatic

### 1. 🔢 Contract Number - AUTO
- **Loads automatically** from Google Sheets
- **Format:** 001/2025, 002/2025, 003/2025...
- **Click refresh** (🔄) to reload
- **Resets yearly:** 001/2026, 001/2027...

### 2. 🎂 Age Calculation - AUTO
- **Type birth date** → Age shows instantly
- **Green badge (≥14):** Adult student
- **Yellow badge (<14):** Minor student

### 3. ✨ Name Auto-Fill - AUTO (if ≥14)
- **Adult students:** Contact name = Student name
- **Blue highlight:** Shows what's auto-filled
- **Can edit:** Just type over it

### 4. 👶 Under 14 Section - AUTO
- **Hidden** if student ≥14
- **Visible** if student <14
- **Auto-filled** with student info

### 5. ⚡ Demo Data Button - CLICK
- **One click** fills entire form
- **Choose:** Adult (16) or Minor (12)
- **Real data:** Romanian addresses, phones, etc.

---

## 📝 Quick Form Guide

### Standard Flow (Adult Student)

```
1. Open form
   → Contract number: 001/2025 ✅ (auto-loaded)
   → Date: Today ✅ (auto-set)

2. Fill student info:
   Name: Ion Popescu
   Birth: 2008-03-15
   → Age badge: [Vârstă: 16 ani] 🟢
   → Contact name auto-fills: Ion Popescu (blue)

3. Complete contact details:
   - Address, phone, email, ID, CNP

4. Fill emergency contact

5. Fill course details

6. Submit
   → PDF generated ✅
   → Saved to Google Sheets ✅
   → Email sent ✅
```

### Fast Test Flow

```
1. Click: "⚡ Date Demo (Testing)"
2. Choose: OK (Adult) or Cancel (Minor)
3. Verify: All fields filled
4. Submit: Done!
```

---

## 🎨 Visual Elements

### What You'll See

**Contract Number Field:**
```
┌────────────────────────┐
│ 001/2025          [🔄] │  ← Auto-loaded + Refresh button
└────────────────────────┘
Numărul se generează automat din Excel
```

**Age Badge (Adult):**
```
Date Student [Vârstă: 16 ani] 🟢
```

**Age Badge (Minor):**
```
Date Student [Vârstă: 12 ani] 🟡
```

**Auto-Filled Fields:**
```
┌────────────────────────┐
│ Ion                    │  ← Blue background = auto-filled
└────────────────────────┘
```

**Demo Button:**
```
┌────────────────────────────┐
│  Contract de Prestări      │
│  [⚡ Date Demo (Testing)]  │  ← Click here!
└────────────────────────────┘
```

---

## 🔄 Common Actions

### Refresh Contract Number
```
Click the 🔄 button next to contract number
→ Reloads latest number from Google Sheets
```

### Use Demo Data
```
Click "⚡ Date Demo (Testing)"
→ Choose Adult or Minor
→ Entire form fills instantly
```

### Override Auto-Fill
```
Field auto-fills with "Ion Popescu"
→ Just type your own value
→ Blue highlight disappears
→ Your value is used
```

### Check Age
```
Select birth date
→ Age badge appears immediately
→ Green = Adult (≥14)
→ Yellow = Minor (<14)
```

---

## 📊 Contract Numbering

### How It Works
```
First contract:    001/2025
Second contract:   002/2025
Third contract:    003/2025
...
Next year:         001/2026  ← Automatic reset
```

### Multiple Users
```
You open form:     005/2025
Friend opens:      005/2025  ← Same number!
You submit first:  005/2025 saved ✅
Friend refreshes:  006/2025  ← Updated!
Friend submits:    006/2025 saved ✅
```

---

## ✅ Success Indicators

### Green Badge = Adult
```
[Vârstă: 16 ani] 🟢
→ Contact auto-filled
→ Under 14 section hidden
→ Ready to complete form
```

### Yellow Badge = Minor
```
[Vârstă: 12 ani] 🟡
→ Contact empty (for parent)
→ Under 14 section visible
→ Fill parent info
```

### Blue Fields = Auto-Filled
```
Light blue background
→ System filled this
→ You can edit it
→ Or keep it
```

### Success Message
```
✅ Succes! Contract generat și trimis cu succes!
PDF generat: ✓ | Salvat în Google Sheets: ✓ | Email trimis: ✓
```

---

## 🎯 Pro Tips

### 1. Fill Birth Date Early
```
Birth date → Age calculates → Auto-fill happens
Best order: Student info → Contact → Rest
```

### 2. Use Demo for Testing
```
Testing feature? Click demo button
Saves typing, uses real numbers
```

### 3. Refresh If Unsure
```
Form open a while? Click refresh (🔄)
Gets latest contract number
```

### 4. Manual Override Anytime
```
Don't like auto-fill? Just type
System respects your choice
```

---

## 🐛 Troubleshooting

### Contract Number Stuck?
```
→ Click refresh button (🔄)
→ Or manually type number
```

### Age Not Showing?
```
→ Make sure birth date selected
→ Check date is valid
→ Refresh page if needed
```

### Blue Highlight Won't Go?
```
→ Start typing - it disappears
→ Highlight is just visual feedback
```

### Under 14 Section Hidden?
```
→ Check age badge color
→ Green = Adult = Section hidden (correct!)
→ Yellow = Minor = Section visible
```

---

## 📋 Complete Features List

✅ **Automatic contract numbering** (from Google Sheets)  
✅ **Real-time age calculation** (from birth date)  
✅ **Smart auto-fill** (name for adults ≥14)  
✅ **Visual feedback** (badges, highlights, notices)  
✅ **Section management** (hide/show based on age)  
✅ **Demo data button** (one-click testing)  
✅ **Professional PDF** (preserves formatting)  
✅ **Google Sheets logging** (automatic save)  
✅ **Email delivery** (automatic send)  
✅ **Refresh button** (reload contract number)  
✅ **Responsive design** (works on all devices)  
✅ **Error handling** (fallbacks everywhere)  

---

## 🎬 Try It Now!

### Open the form:
```
http://localhost:8000
```

### Watch these automatic features:
1. Contract number loads: `001/2025`
2. Fill birth date: Age badge appears
3. Adult student: Contact auto-fills (blue)
4. Click demo: Entire form fills
5. Submit: Everything saves automatically

---

## 📚 Full Documentation

For detailed docs, see:
- **`FINAL_SUMMARY.md`** - Complete overview
- **`AUTO_NUMBERING_FEATURE.md`** - Contract numbering
- **`AGE_CALCULATION_FEATURE.md`** - Age & auto-fill
- **`DEMO_DATA_FEATURE.md`** - Demo button
- **`QUICK_FIX.md`** - Google Sheets setup

---

## 🎉 You're Ready!

Everything is automatic. Just:
1. Open form
2. Fill student details
3. Watch auto-fill magic ✨
4. Complete remaining fields
5. Submit

**That's it!** 🚀

