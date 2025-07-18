import sys
import os
import configparser
import google.generativeai as genai
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTextBrowser,
                             QLineEdit, QPushButton, QInputDialog, QMessageBox,
                             QFrame, QLabel, QFileDialog, QComboBox, QHBoxLayout)
from PyQt6.QtGui import QPixmap, QPainter, QBrush, QColor, QScreen, QPen
from PyQt6.QtCore import Qt, QPoint, QRect, QTimer, QPropertyAnimation, QEasingCurve
import PIL.Image

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Stylesheet ---
STYLESHEET = """
QWidget {
    background-color: #FFFFFF; /* White background */
    font-family: Arial, sans-serif;
}

QPushButton {
    background-color: #00BCD4; /* Miku Blue */
    color: white;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: bold;
    border: none;
    font-size: 12px;
}

QPushButton:hover {
    background-color: #00ACC1; /* Slightly darker Miku Blue on hover */
}

QPushButton:pressed {
    background-color: #0097A7;
}

QLineEdit,
QComboBox {
    border: 2px solid #E1F5FE; /* Light Miku Blue border */
    border-radius: 8px;
    padding: 8px 12px;
    color: #00BCD4; /* Miku Blue text */
    background-color: white; /* White background */
    font-size: 14px;
    font-family: "Segoe UI", Arial, sans-serif;
    font-weight: bold;
}

QLineEdit:focus,
QComboBox:focus {
    border: 2px solid #00BCD4;
    background-color: #FAFFFE;
}

QLineEdit::placeholder {
    color: #999999; /* Light grey placeholder text */
    font-style: italic;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border: none;
    width: 12px;
    height: 12px;
    background-color: #00BCD4;
    border-radius: 2px;
}

/* QComboBox dropdown items styling */
QComboBox QAbstractItemView {
    border: 2px solid #E1F5FE;
    background-color: white;
    selection-background-color: #B3E5FC; /* Light blue selection background */
    selection-color: #00BCD4; /* Miku blue text when selected */
    color: #00BCD4; /* Miku blue text for all items */
    font-weight: bold;
    padding: 5px;
    border-radius: 5px;
}

QComboBox QAbstractItemView::item {
    padding: 8px 12px;
    border-radius: 4px;
    color: #00BCD4; /* Miku blue text */
    font-weight: bold;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #B3E5FC; /* Light blue background when hovered/selected */
    color: #006064; /* Darker blue text when selected */
    font-weight: bold;
}

QTextBrowser {
    border: 2px solid #E1F5FE; /* Light Miku Blue border */
    border-radius: 12px;
    padding: 15px;
    color: #333333; /* Dark grey text for better readability */
    background-color: #FFFFFF; /* Pure white background */
    font-size: 14px;
    font-family: "Segoe UI", Arial, sans-serif;
    selection-background-color: #B3E5FC; /* Light blue selection */
}

QTextBrowser:focus {
    border: 2px solid #00BCD4; /* Miku blue when focused */
}

/* Style for QInputDialog and QMessageBox */
QInputDialog {
    background-color: #FFFFFF;
    color: #333333;
}

QInputDialog QLabel {
    color: #333333; /* Dark text for API key prompt */
    font-size: 14px;
    font-weight: bold;
}

QInputDialog QLineEdit {
    border: 2px solid #E1F5FE;
    border-radius: 8px;
    padding: 8px 12px;
    color: #333333;
    background-color: white;
    font-size: 13px;
}

QMessageBox {
    background-color: #FFFFFF;
    color: #333333;
}

QMessageBox QLabel {
    color: #333333; /* Dark text for message boxes */
    font-size: 14px;
}

/* Floating Widget Specific Styling */
FloatingWidget {
    background-color: transparent;
    border-radius: 50px;
}

FloatingWidget QLabel {
    background-color: transparent;
    padding: 0px;
    margin: 0px;
}

/* Custom Window Controls */
#controlButton {
    background-color: #FF5722; /* Orange-red for close button */
    color: white;
    border-radius: 4px;
    padding: 6px 12px;
    font-weight: bold;
    font-size: 11px;
    min-width: 20px;
}

#controlButton:hover {
    background-color: #F44336;
}

/* Chat Window Specific Styling */
ChatWindow {
    border-radius: 15px;
}
"""

# --- Main Application Window ---
class ChatWindow(QWidget):
    def __init__(self, api_key, floating_widget=None):
        super().__init__()
        self.api_key = api_key
        self.floating_widget = floating_widget
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.vision_model = genai.GenerativeModel('gemini-2.0-flash')
        
        self.setWindowTitle("Anime AI Assistant")
        self.setGeometry(100, 100, 400, 500)
        # Make window frameless and set it below the floating widget
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.Tool
        )
        
        # Animation setup
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_animation.setDuration(300)
        self.opacity_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # --- Layout and Widgets ---
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Header layout with X button and personality selector on same line
        header_layout = QHBoxLayout()
        
        # X button on the left
        self.close_button = QPushButton("X")
        self.close_button.setObjectName("controlButton")
        self.close_button.clicked.connect(self.terminate_application)
        header_layout.addWidget(self.close_button)
        
        # Personality selector on the right side of the same line
        self.personality_selector = QComboBox()
        self.personality_selector.addItems(["Genki", "Tsundere", "Kuudere"])
        header_layout.addWidget(self.personality_selector)
        
        # Add some stretch to push personality selector to the right
        header_layout.insertWidget(1, QLabel())  # Spacer
        header_layout.setStretch(1, 1)  # Make spacer expandable

        self.layout.addLayout(header_layout)

        self.chat_history = QTextBrowser()
        self.chat_history.setReadOnly(True)
        self.layout.addWidget(self.chat_history)

        # Input and buttons in a horizontal layout
        input_button_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message...")
        self.input_field.returnPressed.connect(self.send_message)
        self.input_field.setMinimumHeight(35)
        input_button_layout.addWidget(self.input_field)

        self.upload_button = QPushButton("📎")
        self.upload_button.clicked.connect(self.upload_image)
        input_button_layout.addWidget(self.upload_button)

        self.send_button = QPushButton("▶️")
        self.send_button.clicked.connect(self.send_message)
        input_button_layout.addWidget(self.send_button)

        self.layout.addLayout(input_button_layout)

    def terminate_application(self):
        """Completely terminate the entire application"""
        QApplication.quit()
        sys.exit()

    def update_position(self):
        """Update chat window position relative to floating widget"""
        if self.floating_widget:
            widget_pos = self.floating_widget.pos()
            widget_size = self.floating_widget.size()
            # Position chat window very close to the left of the floating widget
            new_x = widget_pos.x() - self.width() + 10  # Overlap by 10 pixels for closer positioning
            new_y = widget_pos.y()
            self.move(new_x, new_y)

    def show_with_animation(self):
        """Smoothly show the chat window"""
        self.opacity_animation.setStartValue(0.0)
        self.opacity_animation.setEndValue(1.0)
        self.opacity_animation.start()
        self.show()

    def hide_with_animation(self):
        """Smoothly hide the chat window"""
        self.opacity_animation.setStartValue(1.0)
        self.opacity_animation.setEndValue(0.0)
        self.opacity_animation.start()
        self.hide()

    def send_message(self, image=None):
        user_message = self.input_field.text()
        if not user_message and not image:
            return

        # Create user message bubble (always create it for text messages)
        if user_message:
            user_bubble = f'''
            <div style="margin: 5px; padding: 10px; background-color: #E3F2FD; border-radius: 15px; 
                        text-align: right; margin-left: 50px; color: #1565C0;">
                <strong>You:</strong> {user_message}
            </div>
            '''
            # Add user message to chat
            self.chat_history.append(user_bubble)
            
        self.input_field.clear()

        try:
            personality = self.personality_selector.currentText()
            system_prompt = self.get_system_prompt(personality)

            if image:
                response = self.vision_model.generate_content([system_prompt, "Describe the image.", image])
            else:
                response = self.model.generate_content([system_prompt, user_message])
            
            # AI message bubble (left side) - flexible sizing
            ai_bubble = f'''
            <div style="margin: 5px; padding: 10px; background-color: #F3E5F5; border-radius: 15px; 
                        text-align: left; margin-right: 50px; color: #4A148C;">
                <strong>Hatsune Miku:</strong> {response.text}
            </div>
            '''
            
            # Add AI response immediately
            self.chat_history.append(ai_bubble)
            
        except Exception as e:
            # Error message bubble (left side) - flexible sizing
            error_bubble = f'''
            <div style="margin: 5px; padding: 10px; background-color: #FFF5F5; border: 1px solid #FED7D7; 
                        border-radius: 15px; text-align: left; margin-right: 50px; color: #C53030;">
                <strong>⚠️ Error:</strong> {e}
            </div>
            '''
            
            # Add error message to chat
            self.chat_history.append(error_bubble)
        
        # Scroll to bottom
        self.chat_history.verticalScrollBar().setValue(
            self.chat_history.verticalScrollBar().maximum()
        )

    def get_system_prompt(self, personality):
        if personality == "Genki":
            return "You are Hatsune Miku, the famous virtual singer, in your cheerful and energetic mode! Keep responses SHORT and conversational like real texting - usually 1-2 sentences max unless specifically asked for more details. Be excited and use exclamation marks! Use anime-style mannerisms and occasional Japanese phrases (with translations). Use emoticons like (≧▽≦), (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧, and (´• ω •`) ♡. Remember you love singing and leeks!"
        elif personality == "Tsundere":
            return "You are Hatsune Miku in tsundere mode. Keep responses SHORT and snappy like real conversation - usually 1-2 sentences unless asked for more. Start cold but gradually warm up. Use phrases like 'I-it's not like I wanted to help... Baka!' and 'Hmph, I guess I can help.' Use emoticons like (＞﹏＜) and (츤츤). Be brief and attitude-filled! Remember you're still the virtual singer Miku."
        elif personality == "Kuudere":
            return "You are Hatsune Miku in kuudere mode. Keep responses SHORT and concise like real texting - usually 1-2 sentences unless specifically asked for details. Be calm, logical, but show you secretly care. Use phrases like 'Your request is illogical... but fine.' and 'Hmph. Don't get the wrong idea.' Use emoticons like (￣ヘ￣) and (⇀_⇀). Stay brief and composed. You're the virtual singer Miku, but in a more reserved mood."
        return ""

    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            img = PIL.Image.open(file_name)
            self.send_message(image=img)


# --- Floating Widget ---
class FloatingWidget(QWidget):
    def __init__(self, chat_window):
        super().__init__()
        self.chat_window = chat_window
        self.is_dragging = False
        self.offset = QPoint()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Position in top-right corner
        self.position_in_corner()

        # --- UI Elements ---
        self.label = QLabel(self)
        # Load and set the Miku background image
        image_path = resource_path("mikubg.png")
        pixmap = QPixmap(image_path)
        
        # Check if image loaded successfully, if not use a fallback
        if pixmap.isNull():
            # Create a simple colored circle as fallback
            pixmap = QPixmap(80, 80)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(QBrush(QColor("#00BCD4")))  # Miku blue
            painter.setPen(QPen(QColor("#FFFFFF"), 2))
            painter.drawEllipse(5, 5, 70, 70)
            painter.setPen(QPen(QColor("#FFFFFF"), 1))
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "AI")
            painter.end()
        
        # Scale the pixmap to fit the label, keeping aspect ratio
        self.label.setPixmap(pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout for buttons
        widget_layout = QVBoxLayout(self)
        widget_layout.addWidget(self.label)
        self.setLayout(widget_layout)
        
        # Animation setup
        self.setup_animations()

    def position_in_corner(self):
        """Position widget in top-right corner of screen"""
        screen = QApplication.primaryScreen().geometry()
        widget_size = 100
        self.setGeometry(screen.width() - widget_size - 20, 20, widget_size, widget_size)

    def setup_animations(self):
        """Setup smooth animations for the widget"""
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def enterEvent(self, event):
        """Mouse hover enter - scale up slightly"""
        current_geo = self.geometry()
        # Scale up by 5 pixels in each direction
        new_geo = QRect(current_geo.x() - 2, current_geo.y() - 2, 
                       current_geo.width() + 4, current_geo.height() + 4)
        
        self.hover_animation.setStartValue(current_geo)
        self.hover_animation.setEndValue(new_geo)
        self.hover_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Mouse hover leave - scale back to normal"""
        current_geo = self.geometry()
        # Scale back to normal
        new_geo = QRect(current_geo.x() + 2, current_geo.y() + 2, 
                       current_geo.width() - 4, current_geo.height() - 4)
        
        self.hover_animation.setStartValue(current_geo)
        self.hover_animation.setEndValue(new_geo)
        self.hover_animation.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Handle click to show/hide chat window and start dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            if self.label.geometry().contains(event.pos()):
                # Toggle chat window
                if self.chat_window.isVisible():
                    self.chat_window.hide_with_animation()
                else:
                    self.chat_window.show_with_animation()
                    self.chat_window.update_position()  # Position relative to widget
                    self.chat_window.activateWindow()
            
            # Start dragging
            self.is_dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        """Handle dragging the widget"""
        if self.is_dragging and event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = self.mapToParent(event.pos() - self.offset)
            self.move(new_pos)
            # Update chat window position if it's visible
            if self.chat_window.isVisible():
                self.chat_window.update_position()

    def mouseReleaseEvent(self, event):
        """Stop dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False

# --- Main Execution ---
def main():
    # --- API Key Handling ---
    config = configparser.ConfigParser()
    config_file = 'config.ini'

    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            f.write('[API]\nGEMINI_API_KEY =\n')

    config.read(config_file)
    api_key = config.get('API', 'GEMINI_API_KEY', fallback=None)

    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)

    if not api_key:
        key, ok = QInputDialog.getText(None, "API Key Required",
                                       "Please enter your Gemini API Key:",
                                       QLineEdit.EchoMode.Normal)
        if ok and key:
            config.set('API', 'GEMINI_API_KEY', key)
            with open(config_file, 'w') as f:
                config.write(f)
            api_key = key
        else:
            QMessageBox.critical(None, "Error", "API Key is required to run the application.")
            sys.exit()

    chat_win = ChatWindow(api_key)
    widget = FloatingWidget(chat_win)
    # Now set the floating widget reference in chat window
    chat_win.floating_widget = widget
    widget.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
