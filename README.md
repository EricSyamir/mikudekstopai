# 🎌 Hatsune Miku AI Assistant

A beautiful, Hatsune Miku-themed AI chatbot desktop application with a floating widget interface powered by Google's Gemini AI. Chat with the famous virtual singer in different personality modes!


## ✨ Features

### 🤖 **Hatsune Miku Personalities**
- **Genki**: Cheerful and energetic Miku who loves singing and leeks!
- **Tsundere**: Initially cold Miku who gradually warms up to you
- **Kuudere**: Calm, logical Miku who secretly cares but stays composed

### 🎨 **Beautiful Interface**
- **Floating Widget**: Draggable Miku-themed logo that stays on top
- **Modern Chat UI**: Clean, bubble-style messaging interface
- **Miku Blue Theme**: Consistent cyan color scheme throughout
- **Frameless Design**: Sleek, borderless windows

### 🔧 **Interactive Features**
- **Drag & Drop**: Move the floating widget anywhere on your screen
- **Image Analysis**: Upload images for AI description and analysis
- **Real-time Chat**: Instant responses from Hatsune Miku with personality-based replies
- **Auto-positioning**: Chat window follows the floating widget

## 📥 Installation

### **Option 1: Direct Download (Recommended)**
1. Download `HatsuneMikuAssistant_v2.exe` from the releases
2. Place it in any folder you prefer
3. Double-click to run - no installation required!

### **Option 2: From Source**
```bash
git clone <repository-url>
cd desktopassist
pip install -r requirements.txt
python main.py
```

## 🚀 Quick Start

### **1. First Launch**
- Run `HatsuneMikuAssistant_v2.exe`
- Enter your **Google Gemini API Key** when prompted
- The floating Miku widget will appear in the top-right corner

### **2. Getting Your API Key**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new project or select existing one
3. Generate an API key
4. Copy and paste it into the application

### **3. Basic Usage**
- **Click the floating logo**: Open/close chat window
- **Drag the logo**: Move the entire application
- **Select personality**: Choose your preferred Miku personality mode
- **Type messages**: Chat with Hatsune Miku
- **Upload images**: Click 📎 to analyze pictures

## 🎮 How to Use

### **Moving the Application**
- **Left-click and drag** the floating widget to move it anywhere
- The chat window automatically follows the widget

### **Chatting**
1. Click the floating Miku logo to open the chat
2. Select your preferred Miku personality (Genki/Tsundere/Kuudere)
3. Type your message and press Enter or click ▶️
4. Enjoy chatting with the virtual singer Hatsune Miku!

### **Image Analysis**
1. Click the 📎 (paperclip) button
2. Select an image file (PNG, JPG, BMP)
3. The AI will describe and analyze your image

### **Closing the Application**
- Click the **X** button (left side of chat window)
- Or close from the system tray

## ⚙️ Configuration

The application creates a `config.ini` file to store your API key:
```ini
[API]
GEMINI_API_KEY = your_api_key_here
```

## 🎨 Customization

### **Miku Personalities**
- **Genki**: Energetic Miku responses with singing references, Japanese phrases and emoticons
- **Tsundere**: Initially cold Miku responses that warm up over time 
- **Kuudere**: Calm, logical Miku responses with hidden caring

### **Interface Colors**
- Primary: Miku Blue (`#00BCD4`)
- Backgrounds: Clean whites and light blues
- Text: High contrast for readability

## 🔧 System Requirements

- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: ~100MB for the executable
- **Internet**: Required for AI responses

## 🌐 Network Requirements

- Active internet connection for Google Gemini API
- Outbound HTTPS connections (port 443)
- No special firewall configuration needed

## 🛠️ Troubleshooting

### **Application Won't Start**
- Ensure you have an active internet connection
- Check if Windows Defender is blocking the executable
- Run as Administrator if needed

### **API Key Issues**
- Verify your Gemini API key is valid
- Check your Google Cloud billing is active
- Ensure API quotas aren't exceeded

### **Chat Not Responding**
- Check internet connection
- Verify API key in `config.ini`
- Restart the application

### **Widget Not Visible**
- Check if it's moved off-screen
- Delete `config.ini` and restart to reset position
- Ensure display scaling is set to 100%

### **Performance Issues**
- Close other resource-intensive applications
- Check available RAM
- Restart the application

## 📝 File Structure

```
desktopassist/
├── HatsuneMikuAssistant_v2.exe    # Main executable
├── config.ini                     # API key storage (auto-created)
├── mikubg.png                     # Miku widget background image
├── bg.jpg                         # Background image
└── README.md                      # This file
```

## 🔒 Privacy & Security

- **API Key**: Stored locally in `config.ini`
- **Chat Data**: Not stored permanently, only in memory
- **Images**: Processed by Google Gemini, follow their privacy policy
- **No Telemetry**: No usage data collected

## 🆘 Support

### **Common Issues**
- **Blank responses**: Check API quota limits
- **Slow responses**: Normal during high Google API usage
- **Widget disappeared**: Restart application to reset position

### **Getting Help**
1. Check this README first
2. Verify your API key is working
3. Try restarting the application
4. Check internet connectivity

## 📋 Changelog

### **v2.0**
- ✅ Draggable floating widget
- ✅ Repositioned X button and controls
- ✅ Improved chat bubble styling
- ✅ Better image path handling
- ✅ Enhanced personality selection
- 🎤 Rebranded as Hatsune Miku AI Assistant

### **v1.0**
- 🎉 Initial release
- 🤖 Three Miku personality modes
- 🎨 Miku-themed interface
- 📷 Image analysis support

## 🎯 Tips & Tricks

- **Quick Toggle**: Single-click the logo to show/hide chat
- **Smooth Dragging**: Hold and drag from anywhere on the widget
- **Personality Switching**: Change personalities mid-conversation
- **Image Tips**: Works best with clear, well-lit images
- **Positioning**: Widget remembers position between sessions

## 📄 License

This project is for personal use. Respect Google's Gemini API terms of service.

---

**Enjoy chatting with Hatsune Miku! (◕‿◕)♡**

*For the best experience, make sure your Gemini API key has sufficient quota and your internet connection is stable. Let Miku brighten your day with her virtual charm!*
