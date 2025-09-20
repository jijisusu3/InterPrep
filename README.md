# InterPrep

**InterPrep** is an AI-powered mock interview coach built with **Django**.  
It helps job candidates prepare more effectively by generating **personalized interview questions** and providing **instant AI-driven feedback**.

---

## 🚀 Features

- **Resume-based question generation**  
  Upload your resume and select a desired role from over **150 predefined roles**.  
  Instantly generate **50 personalized questions** using the OpenAI API.

- **Practice Dashboard**  
  - Switch between multiple saved applications  
  - Delete applications and history with confirmation  
  - Track answered/unanswered questions with live status icons  

- **Answer Management**  
  - Draft, save, and edit responses  
  - Submit answers for **real-time scoring and AI feedback**  
  - AJAX-based updates: no page reloads needed

- **Authentication Flow**  
  - Register with live inline validation  
  - Sign in securely with username and password  
  - Role-based dashboard navigation

---

## 🖼️ App Flow

1. **Home Page**  
   - Visitors see **Sign In** and **Register** buttons  
   - Authenticated users see **My Practice**, **Add a Role**, and **Sign Out**  

2. **Register & Login**  
   - Inline validation for Username, Email, and Password  
   - Secure login with credentials  

3. **Application Upload**  
   - Choose a role from dropdown (150+ roles)  
   - Upload resume in `.txt` format  
   - AI generates 50 tailored interview questions  

4. **Practice Page**  
   - Left panel: question list with status icons  
   - Right panel: answer editor with **Save** and **Submit**  
   - Real-time scoring & feedback displayed instantly  

---

## ⚙️ Tech Stack

- **Backend**: Django  
- **Frontend**: Django templates + Vanilla JavaScript (AJAX)  
- **AI Integration**: OpenAI API  
- **Environment Management**: Python venv + `.env` for secrets  

---

## 🏗️ Installation

```bash
# Clone the repository
git clone https://github.com/your-username/interprep.git
cd interprep

# Create virtual environment
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

# Install dependencies
pip install -r requirements.txt

# Add API key
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Run server
python manage.py runserver
