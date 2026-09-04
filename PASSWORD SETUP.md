# 🔐 Stock EMA Screener - Password Protected

## Installation & Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Passwords

File खोलो: `config.yaml`

**पहले (Default):**
```yaml
credentials:
  usernames:
    sahaz:
      email: sahaz@trading.com
      name: Sahaz
      password: password123
    admin:
      email: admin@trading.com
      name: Admin
      password: admin123
    user:
      email: user@trading.com
      name: User
      password: user123
```

**Apna password set करो:**
```yaml
credentials:
  usernames:
    sahaz:
      email: apka-email@gmail.com
      name: Apka Naam
      password: apka-password-123  # Change this!
```

### Step 3: Run App

```bash
streamlit run stock_ema_screener_auth.py
```

---

## 🔑 **Login Credentials**

| Username | Password | Role |
|----------|----------|------|
| sahaz | password123 | Owner |
| admin | admin123 | Admin |
| user | user123 | User |

**Change करो config.yaml में अपने credentials के साथ!**

---

## 🔒 **Security Tips**

1. **Secret key change करो** (`config.yaml` में `cookie.key`)
2. **Production में:** Hashed passwords use करो
3. **Regular basis पर** password change करो
4. **GitHub पर push न करो** `config.yaml` (private रखो)

---

## 🛡️ **Advanced: .gitignore में add करो**

```
config.yaml
__pycache__/
*.pyc
.streamlit/
venv/
```

---

## 📱 **Multiple Users के लिए:**

```yaml
credentials:
  usernames:
    user1:
      email: user1@gmail.com
      name: User One
      password: pass1
    user2:
      email: user2@gmail.com
      name: User Two
      password: pass2
    user3:
      email: user3@gmail.com
      name: User Three
      password: pass3
```

---

## 🔄 **Features:**

✅ **Login page** - Username और password entry  
✅ **Session management** - 30 दिनों की cookie  
✅ **Logout button** - Sidebar में  
✅ **User name display** - "Logged in as: Sahaz"  
✅ **Multiple users support** - कई users को access दे सकते हो  

---

## 📤 **GitHub पर Push करते समय:**

1. **config.yaml को .gitignore में add करो**
   ```
   echo "config.yaml" >> .gitignore
   ```

2. **config.yaml को remove करो git से**
   ```bash
   git rm --cached config.yaml
   git commit -m "Remove config.yaml from tracking"
   ```

3. **README में example दो लोगों को**
   ```markdown
   ## Setup
   1. config.yaml बनाओ example के आधार पर
   2. Apne passwords set करो
   3. streamlit run stock_ema_screener_auth.py
   ```

---

## 🆘 **Troubleshooting**

### **"No module named streamlit_authenticator"**
```bash
pip install streamlit-authenticator
```

### **"No module named yaml"**
```bash
pip install pyyaml
```

### **Login button काम नहीं कर रहा**
- config.yaml file same folder में है?
- YAML format सही है?
- Indentation सही है?

---

## 🎯 **Next Steps**

1. ✅ App install किया
2. ✅ Password set किया
3. ✅ App चलाया
4. ✅ Login किया
5. **अब stocks add करके analyze करो!**

---

**Happy Secure Trading! 🚀**
