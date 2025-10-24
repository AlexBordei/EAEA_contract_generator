# ⚡ Demo Data Auto-Fill Feature

## Quick Testing Made Easy

Added a **"Date Demo (Testing)"** button that instantly fills the entire form with realistic test data.

---

## 🎯 How to Use

### Step 1: Click the Button
Look for the white button in the header:
```
┌─────────────────────────────────────┐
│  Contract de Prestări Servicii      │
│  Early Alpha Engineering S.R.L.     │
│                                     │
│  [⚡ Date Demo (Testing)]           │
└─────────────────────────────────────┘
```

### Step 2: Choose Scenario
A dialog appears:
```
Doriți date pentru student ADULT (14+ ani)?

OK     = Adult (16 ani)
Cancel = Minor (12 ani)
```

### Step 3: Form Auto-Fills!
All fields instantly filled with realistic data ✨

---

## 📋 What Gets Filled

### Option 1: Adult Student (16 years)

**Contract:**
- Number: `DEMO-XXX` (random)
- Date: Today's date

**Student:**
- Name: `Ion Popescu`
- Birth: Calculated to be 16 years old
- Age badge: 🟢 `Vârstă: 16 ani`

**Contact (Auto-filled):**
- Name: `Ion Popescu` ← (blue highlight, same as student)
- Address: `Str. Exemplu nr. 123, Sector 1, București`
- Phone: `+40 712 345 678`
- Email: `ion.popescu@example.com`
- ID Series: `RO`
- ID No: `123456`
- CNP: `1990315123456`

**Emergency:**
- Name: `Maria Popescu`
- Phone: `+40 712 345 679`

**Under 14 Section:**
- Hidden ✓ (grayed out)

**Courses:**
```
Robotică Avansată
Programare Python
Electronică și IoT
```

**Schedule:**
```
Marți: 17:00-18:30
Joi: 17:00-18:30
Sâmbătă: 10:00-12:00
```

---

### Option 2: Minor Student (12 years)

**Contract:**
- Number: `DEMO-XXX` (random)
- Date: Today's date

**Student:**
- Name: `Maria Ionescu`
- Birth: Calculated to be 12 years old
- Age badge: 🟡 `Vârstă: 12 ani`

**Contact (Parent/Guardian):**
- Name: `Ana Ionescu` ← (parent, different from student)
- Address: `Str. Demo nr. 456, Sector 2, București`
- Phone: `+40 722 111 222`
- Email: `ana.ionescu@example.com`
- ID Series: `AB`
- ID No: `654321`
- CNP: `2850820123456`

**Emergency:**
- Name: `Mihai Ionescu`
- Phone: `+40 722 333 444`

**Under 14 Section:**
- Visible ✓
- Auto-filled with: `Maria Ionescu` + today's date

**Courses & Schedule:**
- Same as adult scenario

---

## 🎨 Visual Feedback

After clicking, you'll see:
```
ℹ️ Date Demo Încărcate! Formularul a fost completat cu date de test.
   Student adult (16 ani) - nume contact auto-completat.
```
or
```
ℹ️ Date Demo Încărcate! Formularul a fost completat cu date de test.
   Student minor (12 ani) - secțiunea sub 14 ani vizibilă.
```

---

## ⚡ Use Cases

### Perfect For:

**1. Development Testing**
```
Quick iteration: Click button → Test feature → Clear
```

**2. Demo/Presentation**
```
Show clients how the form works without typing everything
```

**3. Feature Testing**
```
Test adult auto-fill: Click Adult → See green badge + auto-fill
Test minor flow: Click Minor → See yellow badge + under 14 section
```

**4. Training**
```
Train staff on how the form works with realistic data
```

**5. Screenshot/Video Creation**
```
Need realistic data for documentation? One click!
```

---

## 🔧 Technical Details

### Random Contract Number
- Format: `DEMO-XXX`
- XXX = random number 000-999
- Makes each test submission unique

### Dynamic Birth Dates
- Adult: `currentYear - 16` years ago
- Minor: `currentYear - 12` years ago
- Ensures age calculation always works correctly

### Triggers Age Logic
After filling, automatically calls `handleAgeChange()`:
- Shows age badge
- Auto-fills contact (if adult)
- Shows/hides under 14 section
- Applies all visual feedback

### Realistic Data
- Valid Romanian addresses
- Proper phone format (+40)
- Valid email addresses
- Realistic CNP format (13 digits)
- ID series/numbers
- Multi-line courses and schedules

---

## 🎯 Testing Workflow

### Efficient Testing Loop

**Standard way (slow):**
```
1. Type contract number
2. Select date
3. Type contact name
4. Type contact address
5. Type contact phone
... (15+ more fields)
Total time: 3-5 minutes
```

**With demo data (fast):**
```
1. Click "Date Demo"
2. Choose adult/minor
3. Done!
Total time: 2 seconds
```

### Quick Test Scenarios

**Test 1: Adult auto-fill**
```bash
1. Refresh page
2. Click "Date Demo" → OK (Adult)
3. Verify: Green badge, contact auto-filled
4. Submit
```

**Test 2: Minor workflow**
```bash
1. Refresh page
2. Click "Date Demo" → Cancel (Minor)
3. Verify: Yellow badge, under 14 section visible
4. Submit
```

**Test 3: PDF generation**
```bash
1. Click "Date Demo" → OK
2. Submit form
3. Check output/ folder for PDF
4. Verify formatting and data
```

**Test 4: Multiple submissions**
```bash
for i in {1..5}; do
  1. Click "Date Demo"
  2. Submit
  3. Check: Different DEMO-XXX number each time
done
```

---

## 💡 Pro Tips

### Tip 1: Modify After Fill
Demo data is a starting point. You can still:
- Edit any field
- Change student name
- Modify courses
- Update schedule

### Tip 2: Quick Reset
Want fresh data?
- Click button again
- Gets new random contract number
- Resets all fields

### Tip 3: Test Both Scenarios
Always test both:
- Adult scenario (auto-fill behavior)
- Minor scenario (under 14 section)

### Tip 4: Production Removal
For production deployment:
- Remove the button
- Or hide it with CSS
- Or check environment variable

---

## 🚀 Benefits

### Development Speed
- ✅ **5-10x faster** testing
- ✅ No repetitive typing
- ✅ Focus on functionality, not data entry

### Consistency
- ✅ Same realistic data every time
- ✅ Valid format for all fields
- ✅ Proper Romanian conventions

### Completeness
- ✅ All required fields filled
- ✅ All optional fields filled
- ✅ Triggers all age logic

### Flexibility
- ✅ Two scenarios (adult/minor)
- ✅ Can still edit after fill
- ✅ New random ID each time

---

## 🎨 Button Styling

The button uses:
- White background (`btn-light`)
- Small size (`btn-sm`)
- Lightning icon (⚡)
- Tooltip on hover
- Positioned in card header

---

## 📊 Data Examples

### Adult Student Demo Data
```json
{
  "no": "DEMO-742",
  "date": "2025-10-24",
  "contact_first_name": "Ion",
  "contact_last_name": "Popescu",
  "contact_address": "Str. Exemplu nr. 123, Sector 1, București",
  "contact_phone": "+40 712 345 678",
  "contact_email": "ion.popescu@example.com",
  "student_first_name": "Ion",
  "student_last_name": "Popescu",
  "student_birth_date": "2009-03-15",
  "subscriptions_types": "Robotică Avansată\nProgramare Python\nElectronică și IoT",
  "timeslots": "Marți: 17:00-18:30\nJoi: 17:00-18:30\nSâmbătă: 10:00-12:00"
}
```

### Minor Student Demo Data
```json
{
  "no": "DEMO-158",
  "date": "2025-10-24",
  "contact_first_name": "Ana",
  "contact_last_name": "Ionescu",
  "student_first_name": "Maria",
  "student_last_name": "Ionescu",
  "student_birth_date": "2013-08-20",
  "if_14_student_first_name": "Maria",
  "if_14_student_last_name": "Ionescu"
}
```

---

## ✅ Ready to Use!

**Try it now:**
1. Open: http://localhost:8000
2. Click: "⚡ Date Demo (Testing)"
3. Choose: Adult or Minor
4. See: Instant form fill!

**Perfect for:**
- ⚡ Fast testing
- 🎬 Demos
- 📸 Screenshots
- 👨‍🏫 Training
- 🐛 Bug reproduction

---

**Development testing just got 10x faster!** 🚀

