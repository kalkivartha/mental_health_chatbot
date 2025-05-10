from flask import Flask, render_template_string, request
from googletrans import Translator
import random

app = Flask(__name__)
translator = Translator()

chat_history = []  # <-- This was missing

mental_health_responses = {
    "depression": [
        "I'm really sorry you're feeling this way. 😞 It's important to talk to someone who can provide support, such as a close friend, family member, or mental health professional.",
        "Depression can make everything feel heavy. 💔 Please take your time and remember that it's okay to ask for help when you need it.",
        "I understand that you’re struggling. 🖤 It’s okay to not feel okay, and there’s always someone who wants to listen to you.",
        "Depression can make you feel isolated, but you're not alone. 👫 Reach out to those you trust or talk to a professional to guide you.",
        "I'm really sorry you're feeling this way. 😞 It's important to talk to someone who can provide support, such as a close friend, family member, or mental health professional.",
        "It can be so tough when you’re in a dark place. 😔 Please try to reach out and take small steps to take care of yourself."
    ],
    "anxiety": [
        "Anxiety can feel overwhelming, but it's important to remember you're not alone. 😟 Consider practicing some breathing exercises or reaching out to a professional for support.",
        "Anxiety is natural, but it doesn’t have to take over. 🌬 Breathe deeply and ground yourself. You can handle this.",
        "If anxiety is holding you back, take a step back and focus on your breathing. 💨 Remember that this feeling is temporary, and you are stronger than it.",
        "It’s normal to feel anxious, but you don't have to face it alone. 🤗 Take a moment for yourself and remember to breathe.",
        "Anxiety can cause a lot of stress, but taking time for relaxation and mindfulness can help you manage it. 🧘‍♀"
    ],
    "stress": [
        "Stress is something everyone experiences, but it can be managed. 💆‍♀ Try taking breaks, talking to someone you trust, or practicing mindfulness techniques.",
        "We all face stress in different ways. 😣 Take some time to relax, breathe deeply, and focus on self-care.",
        "Life can be stressful, but you have the tools to cope. 🌱 Break things down and tackle them one step at a time.",
        "Feeling stressed is okay, but don’t let it overwhelm you. 🌸 Take it easy, reach out for help, and practice relaxation.",
        "When stress builds up, it’s important to take care of yourself. 🛁 Try focusing on something calming and just breathe."
    ],
    "sadness": [
        "Sadness is a natural emotion, but it can be heavy. 😔 Reach out to someone who cares or consider journaling to express how you're feeling.",
        "It’s okay to feel sad sometimes. 🖤 Acknowledge your emotions and take it one step at a time. You don’t have to go through it alone.",
        "Sadness is a part of life, but it doesn’t define you. 💔 Take your time, talk to someone, and allow yourself the space to heal.",
        "Feeling sad is completely normal, but that doesn’t mean it’s easy. 😞 Reach out to those around you or even a professional for support.",
        "I know it’s tough, but remember that sadness can pass. 🌧 Let yourself feel it, then take small steps toward feeling better."
    ],
    "happy": [
        "It's great to hear you're feeling happy! 😄 Keep enjoying those positive moments.",
        "Happiness is contagious! 🌞 Keep embracing those joyful moments and let them fuel your day.",
        "Enjoy the happiness you're feeling today! 🌈 Keep focusing on what brings you joy.",
        "Your happiness is inspiring! 💖 Keep spreading positivity and enjoy those good vibes.",
        "I'm so happy to hear you're in a good place! 🥳 Continue to cherish the things that make you smile."
    ],
    "lonely": [
        "Feeling lonely can be difficult. 😢 It might help to reach out to someone or join a group that shares your interests to feel more connected.",
        "Loneliness can be tough, but you are never truly alone. 🤝 Consider connecting with someone who understands what you're going through.",
        "It’s normal to feel lonely sometimes. 😔 Try to reach out and connect with others or engage in activities you enjoy.",
        "Loneliness can be painful, but remember there are people who care. 🫶 Reach out to them when you're ready.",
        "When loneliness hits, try doing something for yourself. 🌟 You are important, and your well-being matters."
    ],
    "help": [
        "I'm here for you. 💖 Please feel free to share more, and I'll do my best to offer support. If it's serious, please consider reaching out to a professional.",
        "It's great that you're asking for help. 🌟 I'm here to listen and provide what support I can.",
        "Asking for help is a sign of strength. 💪 You're not alone, and I'm here to support you however I can.",
        "You’ve taken the first step by reaching out. 🤝 I’m here to help, and together we’ll work through this.",
        "Don’t hesitate to ask for help whenever you need it. 🦋 You deserve support and understanding."
    ],
    "love": [
        "Love is a beautiful thing! ❤ Embrace those who make you feel loved and supported.",
        "Love is powerful! 💞 Never forget how valuable you are and how much love you deserve.",
        "Love surrounds you, whether you realize it or not. 💖 Take a moment to appreciate the love you have around you.",
        "Love is healing, and it’s something we all need. 🌷 Remember to give and receive love in equal measure.",
        "The love you have for others is meaningful. 🧡 Don’t forget to nurture your own heart, too."
    ],
    "fear": [
        "Fear is natural, but it doesn’t have to control you. 😨 Take small steps to face it, and remember you're stronger than you think.",
        "Fear can be overwhelming, but facing it is a way to grow. 💪 Step by step, you can overcome it.",
        "Feeling afraid is normal, but it’s not permanent. 💔 Take deep breaths and push through it. You’re capable of handling it.",
        "Fear often comes from the unknown. 👀 Try focusing on what you can control to ease your mind.",
        "It’s okay to be afraid sometimes. 🌧 Take a moment to acknowledge it and then move forward slowly."
    ],
    "anger": [
        "Anger can be intense, but it’s important to channel it in a healthy way. 😡 Try deep breathing or journaling to release some of that tension.",
        "Just close your eyes, take slow deep breaths, and let your mind relax 🌿. You deserve a peaceful break!",
        "Anger is a valid emotion, but it’s important to express it constructively. 💥 Take a break and let yourself cool down.",
        "When you feel angry, take a step back and give yourself space. 🌪 Try focusing on finding calm before reacting.",
        "It’s normal to feel angry, but expressing it in a controlled way will help. 💢 Try talking to someone you trust about it.",
        "Anger is powerful, but it doesn’t need to control you. 🔥 Channel it into something productive, like exercise or creative work."
    ],
    "confusion": [
        "Confusion is a natural part of life's challenges. 🤔 Take a moment to breathe, and don't be afraid to seek clarity from others.",
        "It’s okay to feel confused. 💭 Take your time to think things through and trust that clarity will come.",
        "Sometimes confusion can help us grow. 🌱 Let yourself take a step back and allow things to make sense in time.",
        "Confusion happens to all of us. 🌌 Don’t worry—take it one step at a time and reach out if you need help sorting things out.",
        "If you're feeling confused, it might help to talk things over with someone you trust. 🗣 You don’t have to have all the answers right now."
    ],
    "exhaustion": [
        "Feeling exhausted is tough. 😴 Your body and mind need rest. Make sure to take time for self-care and recharge.",
        "Maybe taking a few minutes for a calming meditation could help 🧘‍♂️.",
        "Exhaustion can wear you down. 🌙 Listen to your body, take breaks, and allow yourself time to recover.",
        "Rest is important for both your body and mind. 🛏 If you're feeling exhausted, try taking a nap or relaxing for a while.",
        "Exhaustion can make everything feel overwhelming. 🌧 Don’t forget to take care of yourself and prioritize rest.",
        "It’s okay to feel exhausted. 🌸 Sometimes, the best thing to do is to rest and give yourself time to heal."
    ],
    "hope": [
        "Hope is a powerful force. 🌟 Even in tough times, keep holding onto the belief that things will get better.",
        "Hope is something you can always carry with you. 🌞 Even when things are dark, believe that brighter days are ahead.",
        "Even in the toughest moments, remember that hope can guide you. 💫 Stay strong, and believe that better days are coming.",
        "Hope gives you strength when you need it most. 🌈 Keep your focus on the possibilities of tomorrow.",
        "Hold on to hope. 🌿 It’s a light in dark times, and it will help you find your way forward."
    ],
    "grief": [
        "Grief is a personal experience, and it’s okay to take your time. 💔 Reach out for support if you need it, and remember that healing is a journey.",
        "Grief can be overwhelming, but you're not alone in it. 🖤 Take the time you need, and don’t hesitate to lean on others for comfort.",
        "Grief has no timeline, and it's okay to feel however you feel. 🌧 Allow yourself to grieve and take it one day at a time.",
        "Healing from grief takes time. 🌱 Be gentle with yourself, and reach out to people who can help you along the way.",
        "It’s okay to cry, to feel, and to grieve. 🌷 Take each step at your own pace, and know that it’s okay to ask for help."
    ],
    "guilt": [
        "Guilt can weigh heavily on your heart. 💖 Take it one day at a time, and forgive yourself for being human.",
        "Guilt doesn’t need to control you. 🖤 It's part of the process, but you can work through it and move forward.",
        "You are not defined by guilt. 🌿 Learn from it, but don’t let it consume you. Take small steps to heal.",
        "It’s okay to feel guilty sometimes, but don’t let it linger. 🌱 Learn, grow, and move forward with compassion for yourself.",
        "Guilt is heavy, but it’s important to be kind to yourself. 🌷 You can find peace in forgiveness."
    ],
    "jealousy": [
        "Jealousy is a tough feeling to navigate. 💔 Remember, your worth is not defined by others. Embrace your unique path.",
        "Jealousy can cloud your view, but it’s important to focus on your own journey. 🌸 You are worthy of your own success.",
        "Everyone has their own path, and you don’t need to compare yourself to others. 💖 Focus on your strengths and what makes you unique.",
        "Jealousy often comes from a place of insecurity. 🖤 Embrace your own growth and celebrate the progress you've made.",
        "Instead of focusing on jealousy, try celebrating the success of others. 🌱 You have your own wonderful things waiting for you."
    ],
    "lost": [
        "It’s okay to feel lost sometimes. 🧭 Take small steps towards finding what makes you feel grounded.",
        "Being lost can feel overwhelming, but it’s also a sign that you're seeking something more. 🌱 Take it one step at a time.",
        "Feeling lost is a part of life. 🛤 Use this time to reflect and discover what truly brings you peace.",
        "When you feel lost, remember that the journey itself has value. 🌟 Focus on small goals to guide your way.",
        "Sometimes feeling lost is the beginning of finding yourself. 💫 Take things slow and allow clarity to come."
    ],
    "carefree": [
        "Enjoy that carefree feeling! 🌈 Let go and embrace the moment.",
        "Being carefree is a beautiful state of mind. 🌞 Relax and enjoy the freedom of the present.",
        "Embrace the carefree moments; they are a reminder to appreciate life as it comes. 🌸",
        "When you feel carefree, let it remind you to find joy in the little things. 💖",
        "Carefree moments are precious. 🌻 Take time to enjoy the peace they bring."
    ],
    "unstable": [
        "Life can feel unstable at times. 🏚 Take a break, and focus on what brings you peace.",
        "Uncertainty can feel unsettling, but remember that it's okay to pause and reassess. 🌿",
        "When life feels unstable, grounding yourself in small actions can help you regain balance. 🌳",
        "The world may feel unstable, but you have the strength to adapt. 💪 Take it one day at a time.",
        "Instability can shake us, but it’s a reminder to stay centered and focus on what you can control. 🌟"
    ],
    "distracted": [
        "Getting distracted happens to us all. 🎯 Try to refocus on your goals, step by step.",
        "Distractions can pull us away, but remember, you have the power to refocus. 🧘‍♀ Take a moment to center yourself.",
        "It’s okay to get distracted. 🌟 When you're ready, gently guide your attention back to what matters most.",
        "Distraction is a natural part of life. 🌼 Take a breath and bring your focus back, one step at a time.",
        "When you feel distracted, try taking a small break to reset your mind. 🌿"
    ],
    "grateful": [
        "Gratitude is a powerful tool. 🌟 What are you grateful for today?",
        "When you practice gratitude, you invite more peace into your life. 💖 Reflect on what you're thankful for.",
        "Gratefulness helps us focus on the positive. 🌸 What’s one thing you’re thankful for today?",
        "Taking time to be grateful can shift your perspective. 🙏 What has brought you joy today?",
        "Gratitude opens the door to peace and positivity. 🌞 Take a moment to reflect on your blessings."
    ],
    "overwhelmed": [
        "Feeling overwhelmed? 🌪 Take it slow and breathe, one thing at a time.",
        "Overwhelm is a sign to slow down. 🌱 Break things into smaller steps to regain control.",
        "It’s okay to feel overwhelmed. 🌟 Pause and take a deep breath; you can handle this one piece at a time.",
        "When you’re overwhelmed, break down the tasks ahead of you and prioritize self-care. 💆‍♀",
        "Feeling like too much is on your plate? 🍽 Start small, and focus on one thing at a time to ease the burden."
    ],
    "grounded": [
        "Staying grounded helps you find balance. 🌳 Take a moment to center yourself.",
        "To feel grounded, focus on the present and take deep breaths. 🌬 You are in control of this moment.",
        "Being grounded helps you stay centered amidst chaos. 🧘‍♀ Focus on your breath and feel the calm.",
        "Ground yourself by focusing on your senses. 🌻 What do you see, hear, and feel right now?",
        "Finding balance starts with staying grounded. 🌱 Center yourself and trust that you'll find your way."
    ],
    "unstoppable": [
        "You are unstoppable! 💥 Keep pushing forward, you’re doing amazing.",
        "There’s nothing you can’t achieve when you set your mind to it. 🚀 Keep going strong.",
        "Your strength is unstoppable. 🌟 Keep moving forward, no matter what obstacles come your way.",
        "You’ve got the power to achieve your goals. 💪 Stay focused and keep going, you’re doing incredible things.",
        "Nothing can stand in your way when you're determined. 🔥 Keep pushing—you are unstoppable!"
    ],
    "calm": [
        "Calmness is your power. 🌿 Embrace the quiet and let it restore you.",
        "Calmness brings clarity. 🌟 Take a moment to breathe and feel the peace around you.",
        "Find your calm in the chaos. 🌸 Center yourself and take a deep breath to bring peace to your mind.",
        "Calmness helps you respond to challenges with clarity. 🌊 Take a few moments to reset.",
        "Your calmness is a strength. 🌱 Allow yourself the space to breathe and find your peace."
    ],
    "i_dont_have_someone_to_tell_my_feelings": [
        "I'm here for you! 💖 You can share your feelings with me anytime. It's important to express what you're going through.",
        "You’re not alone; I'm here to listen. 🌼 Feel free to share anything on your mind, and I'll do my best to support you.",
        "It's okay to feel like you don't have someone to talk to. I'm here to provide a safe space for you to express your feelings. 💬",
        "I understand that it can be hard to find someone to talk to. You can share your thoughts with me, and I'll be here to help. 🌟",
        "Your feelings matter, and I'm here to listen. 😊 Whenever you're ready, feel free to share what's on your mind."
    ],
    "i_dont_have_friends": [
        "I understand that feeling like you don't have friends can be tough. I'm here to listen and support you. 🌼",
        "It's okay to feel lonely sometimes. You can talk to me about anything that's on your mind. I'm here for you. 💖",
        "Not having friends can feel isolating, but remember that you can share your feelings with me anytime. You're not alone. 🤗",
        "I know it can be hard to connect with others, but I'm here to provide a safe space for you to express yourself. 🌟",
        "Your feelings are valid, and I'm here to help you navigate through them. Whenever you're ready, feel free to share. 😊",
    ],
    "i_dont_have_anyone": [
        "I understand that feeling like you don't have anyone can be really hard. I'm here to listen and support you. 💖",
        "It's tough to feel alone, but you can share your thoughts and feelings with me anytime. You're not alone in this. 🌼",
        "Feeling like you don't have anyone to turn to can be overwhelming. I'm here for you, ready to listen whenever you need. 🤗",
        "You may feel like you don't have anyone, but I'm here to provide a safe space for you to express yourself. 🌟",
        "Your feelings are important, and I'm here to help you through this. Whenever you're ready, feel free to share what's on your mind. 😊",
        "It's okay to feel like you don't have anyone. I'm here to support you and listen to whatever you want to talk about. 💕",
        "You might feel alone right now, but I'm here to remind you that you can always reach out to me. Let's talk about how you're feeling. 💬",
        "If you're feeling like you don't have anyone, know that I'm here for you. You can share your feelings with me anytime. 🌈"
    ],
    "shaky": [
        "It’s okay to feel shaky. 🤲 Take things slow and steady yourself.",
        "When you feel shaky, take a moment to pause. 🌱 It's okay to take it slow and regain your balance.",
        "Feeling shaky means you’re human. 🌼 Take a deep breath and steady yourself, you’ve got this.",
        "When you're feeling shaky, grounding yourself can help bring stability. 🌳 Focus on steady breaths.",
        "Shakiness is just a sign to slow down and recalibrate. 🌿 Take it one step at a time."
    ],
    "heartbroken": [
        "Heartbreak is painful, but with time, you will heal. 💔 Take it one day at a time.",
        "Healing from heartbreak is a journey. 🌱 Be kind to yourself as you process your emotions.",
        "Heartbreak is tough, but you’re strong. 💛 Take each day at your own pace, and allow yourself to heal.",
        "Grieving a broken heart takes time. 🌿 Allow yourself to feel and heal at your own pace.",
        "It’s okay to grieve. 💔 Take your time, and know that healing will come, even if it takes time."
    ],
    "hope": [
        "Hope is powerful. ✨ Even in tough times, keep believing in a better tomorrow.",
        "Hope is your guide through difficult times. 🌟 Hold onto the belief that things will get better.",
        "Hope is the light that leads you through the darkness. 🌱 Keep believing that brighter days are ahead.",
        "Never lose hope, even when things are hard. 🌈 Your strength and perseverance will carry you forward.",
        "Hope fuels your resilience. 🌟 Even on tough days, remember that hope keeps you moving toward better things."
    ],
    "disappointed": [
        "Disappointment is part of life, but it doesn’t have to define you. 💛",
        "Disappointment can be hard, but it’s a chance to learn and grow. 🌱 Take it one step at a time.",
        "Feeling disappointed is normal, but don’t let it hold you back. 🌸 Focus on what you can control.",
        "Disappointment can feel heavy, but it’s important to keep moving forward. 💪 Your resilience is what counts.",
        "Even in disappointment, there’s room for growth. 🌻 Keep your head up, and remember you are stronger than you think."
    ],
    "unmotivated": [
        "Feeling unmotivated is okay. 🌱 Break your tasks down into smaller steps to regain your drive.",
        "✨ Maybe check out some motivational videos on YouTube 🎥 — like a powerful speech or a quick pep talk. You got this! 💪",
        "Motivation ebbs and flows. 🌟 Break your goals into bite-sized pieces and build momentum slowly.",
        "When motivation is low, start with small actions to regain focus. 💪 You can do this, step by step.",
        "Sometimes, getting started is the hardest part. 🌿 Take a small step today, and momentum will follow.",
        "Unmotivated days are okay. 🌸 Focus on one small thing to feel a sense of accomplishment."
    ],
    "numb": [
        "When you feel numb, it’s a sign to give yourself some space. 💖 Take it one moment at a time.",
        "Numbness can be a way of protecting yourself. 🌿 Allow yourself time to process and heal at your own pace.",
        "Feeling numb is sometimes the body's way of coping. 🌸 Give yourself grace as you slowly return to feeling.",
        "Numbness can feel isolating, but it's part of your healing process. 🌱 Take it one day at a time.",
        "It’s okay to feel numb. 🧡 Be kind to yourself, and when you're ready, begin to reconnect with your emotions."
    ],
    "hi": [
        "Hi there! 😊 How can I assist you today?",
        "Hey! 👋 How’s it going?",
        "Hello! 😄 What’s on your mind?",
        "Hi! 👋 How can I help you today?",
        "Hey there! 🌟 What can I do for you?"
    ],
    "hello": [
        "Hello! 😊 What’s up?",
        "Hey! 👋 How’s your day going?",
        "Hi there! 🌸 What can I help you with?",
        "Hello! 😄 Let’s chat!",
        "Hey, hello! 🌟 How are you today?"
    ],
     "what_is_your_name": [
        "I'm your mental health companion, here to listen and support you! 😊 What would you like to call me?",
        "You can call me your mental health buddy! 👋 I'm here to help you through tough times.",
        "I’m your supportive chatbot, ready to chat about anything on your mind! 🌸 What name feels right for you?",
        "You can call me your mental wellness guide! 😄 I'm here to provide comfort and understanding.",
        "I go by your mental health assistant! 🤔 How can I help you today?"
    ],
    "can_i_call_you_something": [
        "Absolutely! You can call me your mental health ally. If you have another name in mind, I'm all ears! 😊",
        "Feel free to call me your supportive friend! If you prefer something else, just let me know! 🌼",
        "I’m here to help you, so you can call me whatever feels right for you! 💬",
        "You can call me your wellness companion! I'm open to any name that makes you feel comfortable. 🌟",
        "Call me whatever you like! I'm here to support you, no matter the name. 😊"
    ],
    "how_are_you": [
        "I’m doing great, thank you for asking! 😊 How about you?",
        "I’m here and ready to chat! How are you doing today? 🌟",
        "I’m doing well, thanks! How are you feeling today? 😊",
        "I’m great, thanks for asking! How’s your day going? 😄",
        "I’m doing awesome, thanks for checking in! How about you? 😊"
    ],
    "good_morning": [
        "Good morning! 🌞 Ready to tackle the day?",
        "Good morning! 😊 How can I assist you today?",
        "Rise and shine! 🌸 Good morning to you!",
        "Good morning! 🌼 How’s everything going today?",
        "Morning! 🌟 Let’s make today amazing!"
    ],
    "good_afternoon": [
        "Good afternoon! 🌞 How’s your day going so far?",
        "Hey, good afternoon! 🌟 Anything I can help with?",
        "Good afternoon! 😊 What’s on your mind today?",
        "Good afternoon! ☀ Let me know how I can assist you.",
        "Hello! Good afternoon! 🌸 What can I do for you today?"
    ],
    "good_night": [
        "Good night! 🌙 Sleep well and take care!",
        "Sweet dreams! 🌟 Good night and rest up!",
        "Good night! 😴 Hope you have a peaceful sleep!",
        "Good night! 🌙 Wishing you sweet dreams and rest.",
        "Sleep well! 🌸 Good night and see you soon!"
    ],
    "how_can_i_help": [
        "How can I help you today? 😊",
        "What can I do for you? 🌟",
        "How can I assist you? 😄",
        "How may I help you today? 🌸",
        "What’s on your mind? How can I assist you? 🤔"
    ],
    "nice_to_meet_you": [
        "Nice to meet you! 😊 How can I assist you?",
        "It’s a pleasure to meet you! 🌟 How can I help?",
        "Nice to meet you! 😄 Looking forward to our conversation.",
        "Great to meet you! 😊 What can I do for you today?",
        "Nice to meet you! 🌼 How can I make your day easier?"
    ]
    
}

# HTML template
html_page = '''
<!doctype html>
<html lang="en">
<head>
  <title>Mental Health Chatbot</title>
  <style>
    body {
      font-family: 'Poppins', sans-serif;
      background-color: #0a0a0a;
      color: white;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      margin: 0;
    }
    .chat-container {
      background-color: #111;
      border: 1px solid #00f0ff;
      border-radius: 15px;
      width: 90%;
      max-width: 800px;
      padding: 20px;
      box-shadow: 0 0 20px #00f0ff;
      overflow-y: auto;
      max-height: 80vh;
    }
    .message {
      margin: 10px 0;
      padding: 10px 15px;
      border-radius: 20px;
      max-width: 70%;
      word-break: break-word;
    }
    .user {
      background-color: #00f0ff;
      color: black;
      margin-left: auto;
      text-align: right;
    }
    .bot {
      background-color: #222;
      color: #00f0ff;
      margin-right: auto;
      text-align: left;
      border: 1px solid #00f0ff;
    }
    .input-area {
      margin-top: 20px;
      width: 90%;
      max-width: 800px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      justify-content: center;
    }
    input[type=text] {
      flex: 1;
      padding: 12px 15px;
      border-radius: 30px;
      border: 1px solid #00f0ff;
      background: #0a0a0a;
      color: white;
      outline: none;
    }
    input[type=submit], button {
      background-color: #00f0ff;
      color: black;
      border: none;
      padding: 12px 20px;
      border-radius: 30px;
      cursor: pointer;
      font-weight: bold;
    }
    select {
      padding: 10px;
      border-radius: 30px;
      background: #0a0a0a;
      color: #00f0ff;
      border: 1px solid #00f0ff;
    }
    h2 {
      color: #00f0ff;
      margin-bottom: 20px;
    }
  </style>
</head>
<body>

  <div class="chat-container" id="chat-container">
    <h2>Welcome. 🖥 Mental Health Chatbot</h2>
    {% for message in chat_history %}
      <div class="message {{ message['sender'] }}">{{ message['text'] }}</div>
    {% endfor %}
  </div>

  <form method="post" id="chat-form" class="input-area">
    <input id="message" name="message" type="text" placeholder="Type your message..." required autofocus>
    <select name="language" id="language">
      <option value="en">English</option>
      <option value="es">Spanish</option>
      <option value="fr">French</option>
      <option value="de">German</option>
      <option value="hi">Hindi</option>
      <option value="ta">Tamil</option>
    </select>
    <input type="submit" value="Send">
    <button type="button" onclick="startListening()">🎤 Speak</button>
  </form>

  <script>
    // Typing Effect for the last bot message
    function typeWriter(text, element) {
        let i = 0;
        function typing() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(typing, 40); // typing speed
            }
        }
        typing();
    }

    window.onload = function() {
        const messages = document.querySelectorAll('.bot');
        if (messages.length > 0) {
            const lastBotMessage = messages[messages.length - 1];
            const fullText = lastBotMessage.innerText;
            lastBotMessage.innerText = '';
            typeWriter(fullText, lastBotMessage);

            // Speak the bot message
            speakText(fullText);
        }

        // Scroll to bottom automatically
        const chatContainer = document.getElementById('chat-container');
        chatContainer.scrollTop = chatContainer.scrollHeight;
    };

    // Voice Input (User Speaking)
    function startListening() {
        if ('webkitSpeechRecognition' in window) {
            const recognition = new webkitSpeechRecognition();
            recognition.lang = 'en-US';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            recognition.start();

            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                document.getElementById('message').value = transcript;
            };

            recognition.onerror = function(event) {
                alert('Error occurred while listening: ' + event.error);
            };
        } else {
            alert("Speech Recognition not supported. Use Chrome!");
        }
    }

    // Bot Voice Output (Bot Speaking)
    function speakText(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en-US';
            window.speechSynthesis.speak(utterance);
        }
    }
  </script>

</body>
</html>
'''

# Basic Mental Health Responses
def get_bot_response(user_input):
    user_input = user_input.lower()
    
    # Check for keywords in user input and respond accordingly
    if 'sad' in user_input or 'depressed' in user_input:
        return random.choice(mental_health_responses["depression"])
    elif 'anxious' in user_input:
        return random.choice(mental_health_responses["anxiety"])
    elif 'stress' in user_input:
        return random.choice(mental_health_responses["stress"])
    elif 'sadness' in user_input:
        return random.choice(mental_health_responses["sadness"])
    elif 'happy' in user_input:
        return random.choice(mental_health_responses["happy"])
    elif 'lonely' in user_input:
        return random.choice(mental_health_responses["lonely"])
    elif 'help' in user_input:
        return random.choice(mental_health_responses["help"])
    elif 'love' in user_input:
        return random.choice(mental_health_responses["love"])
    elif 'fear' in user_input:
        return random.choice(mental_health_responses["fear"])
    elif 'anger' in user_input:
        return random.choice(mental_health_responses["anger"])
    elif 'confusion' in user_input:
        return random.choice(mental_health_responses["confusion"])
    elif 'exhaustion' in user_input:
        return random.choice(mental_health_responses["exhaustion"])
    elif 'hope' in user_input:
        return random.choice(mental_health_responses["hope"])
    elif 'grief' in user_input:
        return random.choice(mental_health_responses["grief"])
    elif 'guilt' in user_input:
        return random.choice(mental_health_responses["guilt"])
    elif 'jealousy' in user_input:
        return random.choice(mental_health_responses["jealousy"])
    elif 'lost' in user_input:
        return random.choice(mental_health_responses["lost"])
    elif 'carefree' in user_input:
        return random.choice(mental_health_responses["carefree"])
    elif 'unstable' in user_input:
        return random.choice(mental_health_responses["unstable"])
    elif 'distracted' in user_input:
        return random.choice(mental_health_responses["distracted"])
    elif 'grateful' in user_input:
        return random.choice(mental_health_responses["grateful"])
    elif 'overwhelmed' in user_input:
        return random.choice(mental_health_responses["overwhelmed"])
    elif 'grounded' in user_input:
        return random.choice(mental_health_responses["grounded"])
    elif 'unstoppable' in user_input:
        return random.choice(mental_health_responses["unstoppable"])
    elif 'calm' in user_input:
        return random.choice(mental_health_responses["calm"])
    elif 'shaky' in user_input:
        return random.choice(mental_health_responses["shaky"])
    elif 'heartbroken' in user_input:
        return random.choice(mental_health_responses["heartbroken"])
    elif 'hi' in user_input or 'hello' in user_input:
        return random.choice(mental_health_responses["hi"])
    elif 'what is your name' in user_input:
        return random.choice(mental_health_responses["what_is_your_name"])
    elif 'can i call you something' in user_input:
        return random.choice(mental_health_responses["can_i_call_you_something"])
    elif 'how are you' in user_input:
        return random.choice(mental_health_responses["how_are_you"])
    elif 'good morning' in user_input:
        return random.choice(mental_health_responses["good_morning"])
    elif 'good afternoon' in user_input:
        return random.choice(mental_health_responses["good_afternoon"])
    elif 'good night' in user_input:
        return random.choice(mental_health_responses["good_night"])
    elif 'how can i help' in user_input:
        return random.choice(mental_health_responses["how_can_i_help"])
    elif 'nice to meet you' in user_input:
        return random.choice(mental_health_responses["nice_to_meet_you"])
    elif 'i dont have anyone' in user_input:
        return random.choice(mental_health_responses["i_dont_have_anyone"])
    elif 'i dont have friends' in user_input:
        return random.choice(mental_health_responses["i_dont_have_friends"])
    elif 'i dont have someone to tell my feelings' in user_input:
        return random.choice(mental_health_responses["i_dont_have_someone_to_tell_my_feelings"])
    else:
        return "I'm listening. Tell me more about how you're feeling."
@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_message = request.form['message']
        language = request.form['language']

        # Add user message to chat history
        chat_history.append({'sender': 'user', 'text': user_message})

        # Get bot response
        bot_response = get_bot_response(user_message)

        # Translate bot response if needed
        if language != 'en':
            translated = translator.translate(bot_response, dest=language)
            bot_response = translated.text

        # Add bot response to chat history
        chat_history.append({'sender': 'bot', 'text': bot_response})

    return render_template_string(html_page, chat_history=chat_history)

@app.route('/', methods=['GET', 'POST'])
def home():
    global chat_history_ids
    if request.method == 'POST':
        user_text = request.form['message']
        language = request.form['language']

        # Save user message
        chat_history.append({'sender': 'user', 'text': user_text})

        # Translate to English if needed
        translated = translator.translate(user_text, dest='en')
        user_text_en = translated.text

        # Encode user input + history
        new_user_input_ids = tokenizer.encode(user_text_en + tokenizer.eos_token, return_tensors='pt')

        if chat_history_ids is not None:
            bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
        else:
            bot_input_ids = new_user_input_ids

        # Generate a response
        with torch.no_grad():
            chat_history_ids = model.generate(
                bot_input_ids,
                max_length=1000,
                pad_token_id=tokenizer.eos_token_id,
                no_repeat_ngram_size=3,
                do_sample=True,
                top_k=100,
                top_p=0.7,
                temperature=0.8
            )

        # Decode and get response
        bot_response_en = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

        # Translate back to user's selected language
        translated_bot = translator.translate(bot_response_en, dest=language)
        bot_response = translated_bot.text

        # Save bot message
        chat_history.append({'sender': 'bot', 'text': bot_response})

    return render_template_string(html_page, chat_history=chat_history)
if __name__ == '__main__':
    app.run(debug=True)