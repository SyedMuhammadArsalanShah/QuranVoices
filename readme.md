

# **أصوات القرآن – Quran Voices**

A beautiful, easy-to-use Kivy app for listening to the Quran with audio playback of verses. This app allows users to choose a reciter and listen to audio for each Surah and its verses.

## **Features**

* **Splash Screen**: Welcome screen showing the Quran logo.
* **Surah List**: Displays a list of Surahs with the option to select a reciter.
* **Reciter Selection**: Choose a reciter to listen to (e.g., Abdurrahmaan As-Sudais).
* **Verse-Level Audio**: Play individual verses from any Surah.
* **Responsive UI**: Clean and minimalistic interface suitable for mobile devices.
* **Audio Playback**: Play, pause, and toggle audio for each verse.
* **Arabic Text Support**: Correctly displays Arabic text, reshaped for proper display in Kivy.

---

## **Installation & Requirements**

To run this app, you'll need the following dependencies installed:

1. **Kivy**: A Python library for building mobile applications.
2. **requests**: To make HTTP requests to fetch Surah and reciter data.
3. **playsound**: For audio playback.
4. **arabic\_reshaper & bidi.algorithm**: For reshaping and displaying Arabic text properly.

You can install the dependencies using:

```bash
pip install kivy requests playsound arabic-reshaper python-bidi
```

---

## **App Overview**

### **Splash Screen**

* When you open the app, it shows a splash screen with the Quran logo.
* After a short delay (2 seconds), it automatically transitions to the Surah list screen.

### **Surah List Screen**

* Displays a list of Surahs and allows the user to select a reciter (e.g., Abdurrahman As-Sudais).
* The user can select the reciter from a dropdown (Spinner).
* After selecting a reciter, the user can see a list of Surahs, and upon selecting a Surah, the app will take them to the Verse Audio screen.

### **Verse Audio Screen**

* On this screen, each verse of the selected Surah is listed along with an option to play its audio.
* The user can play or pause the audio for individual verses by pressing the corresponding button next to each verse.

---

## **Code Explanation**

### **1. Import Statements**

```python
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from threading import Thread
import requests
from playsound import playsound
import arabic_reshaper
from bidi.algorithm import get_display
import os
```

This section imports all the necessary libraries:

* **Kivy**: For building the app's UI.
* **requests**: To fetch Surah and reciter data from the Quran API.
* **playsound**: To play audio files.
* **arabic\_reshaper and bidi.algorithm**: To properly display Arabic text.

### **2. Window Configuration**

```python
Window.size = (390, 844)
```

This line configures the window size to mimic a mobile device's screen.

### **3. Arabic Text Reshaping**

```python
def reshape_arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))
```

This function reshapes Arabic text so that it displays correctly in the app.

### **4. Splash Screen Class**

```python
class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.switch_to_surah, 2)
```

* The **SplashScreen** class shows a splash screen with the Quran logo.
* It transitions to the Surah list screen after 2 seconds using **Clock.schedule\_once**.

### **5. Surah List Screen Class**

```python
class SurahListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reciters = []
        self.selected_reciter = 'ar.abdurrahmaansudais'
        self.spinner = None
```

* This class is responsible for displaying the Surah list and allowing users to choose a reciter.
* The **Spinner** widget is used for selecting the reciter.

### **6. Fetching Reciters and Surahs**

```python
def fetch_reciters(self):
    url = "https://api.alquran.cloud/v1/edition?format=audio&language=ar&type=versebyverse"
    response = requests.get(url).json()
    self.reciters = response['data']
```

* **fetch\_reciters** function fetches a list of available reciters from the Quran API.
* **fetch\_surahs** fetches a list of Surahs and displays them as buttons.

### **7. Audio Playback in Verse Screen**

```python
def toggle_audio(self, audio_url):
    if self.audio_playing and self.audio_url == audio_url:
        self.pause_audio()
    else:
        self.play_audio(audio_url)
```

* This function controls the playback of audio. If the same audio is clicked again, it pauses; otherwise, it plays the selected verse's audio.

### **8. Audio in a Separate Thread**

```python
def audio_thread_function(self, audio_url):
    playsound(audio_url)
```

* Audio is played in a separate thread using the **Thread** class to avoid blocking the UI.

---

## **How to Use**

1. Open the app.
2. Select a reciter from the dropdown menu.
3. Choose a Surah.
4. Tap a verse to listen to its audio.
5. You can pause or play the audio for each verse.

---

## **Future Enhancements**

* **Offline Playback**: Store audio files locally for offline listening.
* **Repeat Function**: Add a repeat option for continuous listening of a verse.
* **Search Function**: Allow users to search for specific verses or Surahs.

---

## **Contributing**

Feel free to contribute by opening pull requests, reporting issues, or suggesting improvements.

---

## **License**

This project is open-source and available under the MIT License.


