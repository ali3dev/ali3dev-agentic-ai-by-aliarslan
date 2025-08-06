
# 🍽️ Restaurant Booking Agent

An **AI-powered restaurant reservation system** built with **Google Gemini Pro** and modular Python tools.  
The agent can **understand natural language requests**, **search restaurants**, **check availability**, **book tables**, and **send confirmation emails** — all in a conversational, agentic flow.


````markdown
## 📁 Project Structure
```bash
restaurant-booking-agent/
├── .env                           # API key
├── requirements.txt               # Dependencies
├── main.py                        # Run interactive system
├── test_system.py                  # Run all tests
├── agent/
│   ├── __init__.py
│   └── restaurant_agent.py         # Main agent logic
├── tools/
│   ├── __init__.py
│   ├── restaurant_search.py        # Tool 1 - Search restaurants
│   ├── availability_checker.py     # Tool 2 - Check availability
│   ├── booking_manager.py          # Tool 3 - Manage bookings
│   ├── email_sender.py             # Tool 4 - Send confirmation emails
│   └── user_preference.py          # Tool 5 - Extract preferences from text
└── README.md
````

---

## 🧠 How It Works

The Restaurant Booking Agent uses the **Agentic AI pattern**:

1. **GOAL** – Understand user’s intent (e.g., “Book an Italian restaurant for 4 people at 7 PM tomorrow”)
2. **THINK** – Analyze preferences & missing details
3. **PLAN** – Decide which tools to use next
4. **ACT** – Call the relevant tools (search, availability check, booking)
5. **REFLECT** – Confirm success & guide to next step

---

## ⚙️ Functionalities

### 1. **User Preference Extraction** (`tools/user_preference.py`)

* Extracts cuisine, location, party size, date, time, and special requests from text.
* Validates missing info and asks follow-up questions.

**Example:**

```plaintext
User: I want Italian food for 4 people in downtown at 7 PM tomorrow.
Output: {
    cuisine: "italian",
    location: "downtown",
    party_size: 4,
    date: "2025-08-07",
    time: "19:00"
}
```

---

### 2. **Restaurant Search** (`tools/restaurant_search.py`)

* Searches a simulated restaurant database by cuisine, location, price range, and party size.
* Ranks results by match score and rating.

**Example:**

```yaml
Search Params: {cuisine: "italian", location: "downtown", party_size: 4}
Results: Top 6 matching restaurants.
```

---

### 3. **Availability Checker** (`tools/availability_checker.py`)

* Simulates real-time availability based on:

  * Popularity (rating)
  * Time of day (peak hours)
  * Party size
* Suggests alternative time slots if unavailable.

---

### 4. **Booking Manager** (`tools/booking_manager.py`)

* Creates a confirmed booking record with:

  * Restaurant details
  * User details
  * Booking reference number
  * Assigned table type
* Stores bookings in memory for retrieval.

---

### 5. **Email Sender** (`tools/email_sender.py`)

* Sends a professional confirmation email to the user.
* Includes:

  * Booking reference
  * Restaurant details
  * Arrival instructions
  * Special requests (if any)

---

### 6. **Main Agent** (`agent/restaurant_agent.py`)

* Orchestrates the full conversation:

  ```
  User Preference Tool → Restaurant Search → Availability Check → Booking Manager → Email Sender
  ```
* Uses **Google Gemini Pro** for natural language understanding and conversation flow.
* Maintains conversation state between messages.

---

## 🚀 Example Interaction

```plaintext
You: Book an Italian restaurant for 2 people at 7 PM downtown today.
Agent: I found 3 great Italian restaurants nearby...
       Which one would you like to book? (1, 2, 3)
You: 2
Agent: Great choice! Checking availability...
       Your table is confirmed. Email sent to john@example.com.
```

---

## 📦 Installation (Using uv)

1. **Clone the repository**

```bash
git clone https://github.com/ali3dev/ali3dev-agentic-ai-by-aliarslan.git
cd ali3dev-agentic-ai-by-aliarslan/restaurant-booking-agent
```

2. **Create virtual environment**

```bash
uv venv
# Activate environment
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

3. **Install dependencies**

```bash
uv pip install -r requirements.txt
```

---

## 🧪 Testing

```bash
python test_system.py
```

