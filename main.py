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

# Resize window for mobile style
Window.size = (390, 844)

# Arabic reshaping
def reshape_arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))

# Color theme
DARK_BLUE = (0.0, 0.08, 0.26, 1)
TEAL = (0.03, 0.33, 0.33, 1)
GRAY = (0.48, 0.48, 0.48, 1)
WHITE = (1, 1, 1, 1)
ORANGE = (1, 0.7, 0.05, 1)

class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.switch_to_surah, 2)

    def switch_to_surah(self, dt):
        self.manager.current = 'surah_list'

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(Label(size_hint_y=None, height=20))  # Spacer
        layout.add_widget(Image(source='logo.png', size_hint=(None, None), size=(200, 200), pos_hint={"center_x": 0.5}))
        layout.add_widget(Label(
            text=reshape_arabic_text("القرآن الكريم"),
            font_size=40,
            font_name="Arial",
            color=ORANGE,
            size_hint_y=None,
            height=80
        ))
        self.add_widget(layout)

class SurahListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reciters = []
        self.selected_reciter = 'ar.abdurrahmaansudais'
        self.spinner = None

    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', spacing=15, padding=15)
        layout.add_widget(self.make_back_button('splash'))

        layout.add_widget(Label(
            text=reshape_arabic_text("اختر القارئ و السورة"),
            font_size=30,
            font_name="Arial",
            color=ORANGE,
            size_hint_y=None,
            height=50
        ))

        self.spinner = Spinner(text='Loading Reciters...', size_hint_y=None, height=44)
        self.spinner.bind(text=self.update_reciter)
        layout.add_widget(self.spinner)

        self.fetch_reciters()

        scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll.add_widget(self.grid)
        layout.add_widget(scroll)
        self.fetch_surahs()

        self.add_widget(layout)

    def make_back_button(self, target):
        return Button(
            text='Back',
            size_hint_y=None,
            height=40,
            background_color=GRAY,
            color=WHITE,
            on_press=lambda x: setattr(self.manager, 'current', target)
        )

    def fetch_reciters(self):
        try:
            url = "https://api.alquran.cloud/v1/edition?format=audio&language=ar&type=versebyverse"
            response = requests.get(url).json()
            self.reciters = response['data']
            self.spinner.values = [r['englishName'] for r in self.reciters]
            self.spinner.text = "Abdurrahmaan As-Sudais"
        except:
            self.spinner.text = "Error loading"

    def update_reciter(self, spinner, text):
        for r in self.reciters:
            if r['englishName'] == text:
                self.selected_reciter = r['identifier']
                break

    def fetch_surahs(self):
        url = "https://api.alquran.cloud/v1/surah"
        res = requests.get(url).json()
        self.grid.clear_widgets()

        for surah in res['data']:
            btn = Button(
                text=reshape_arabic_text(f"{surah['number']}. {surah['englishName']} - {surah['name']}"),
                font_name="Arial",
                size_hint_y=None,
                height=50,
                background_color=TEAL,
                color=WHITE,
                on_press=lambda x, num=surah['number']: self.open_verses(num)
            )
            self.grid.add_widget(btn)

    def open_verses(self, surah_number):
        verse_screen = self.manager.get_screen('verse_audio')
        verse_screen.set_reciter(self.selected_reciter)
        verse_screen.load_verses(surah_number)
        self.manager.current = 'verse_audio'

class VerseAudioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reciter = "ar.abdurrahmaansudais"
        self.audio_thread = None
        self.audio_playing = False  # Flag to check if the audio is playing
        self.audio_url = None  # To store the URL of the currently playing audio
        self.play_pause_button = None  # Button for play/pause

    def set_reciter(self, reciter_id):
        self.reciter = reciter_id

    def load_verses(self, surah_number):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(self.make_back_button('surah_list'))

        scroll = ScrollView()
        grid = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        url = f"https://api.alquran.cloud/v1/surah/{surah_number}/{self.reciter}"
        res = requests.get(url).json()

        for ayah in res['data']['ayahs']:
            ayah_box = BoxLayout(orientation='vertical', size_hint_y=None, height=120, padding=5)
            ayah_text = Label(
                text=reshape_arabic_text(ayah['text']),
                font_name="Arial",
                font_size=26,
                color=WHITE,
                size_hint_y=None,
                height=70
            )
            self.play_pause_button = Button(
                text='Play Audio',
                size_hint_y=None,
                height=40,
                background_color=WHITE,
                color=TEAL,
                on_press=lambda x, audio=ayah['audio']: self.toggle_audio(audio)
            )
            ayah_box.add_widget(ayah_text)
            ayah_box.add_widget(self.play_pause_button)
            grid.add_widget(ayah_box)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def make_back_button(self, target):
        return Button(
            text='Back',
            size_hint_y=None,
            height=40,
            background_color=GRAY,
            color=WHITE,
            on_press=lambda x: setattr(self.manager, 'current', target)
        )

    def toggle_audio(self, audio_url):
        if self.audio_playing and self.audio_url == audio_url:
            self.pause_audio()  # Pause if already playing the same audio
        else:
            self.play_audio(audio_url)  # Play new audio

    def play_audio(self, audio_url):
        if self.audio_thread and self.audio_thread.is_alive():
            return  # Prevent multiple threads running simultaneously
        
        self.audio_playing = True
        self.audio_url = audio_url
        self.play_pause_button.text = 'Pause Audio'
        
        # Start the audio in a separate thread to prevent blocking the UI
        self.audio_thread = Thread(target=self.audio_thread_function, args=(audio_url,), daemon=True)
        self.audio_thread.start()

    def audio_thread_function(self, audio_url):
        playsound(audio_url)  # Play the audio

        # After the audio finishes, set the flag to stop and reset button text
        self.audio_playing = False
        self.play_pause_button.text = 'Play Audio'

    def pause_audio(self):
        # Logic to pause the audio (can be tricky with playsound, this part requires improvement)
        self.audio_playing = False
        self.play_pause_button.text = 'Play Audio'

class QuranApp(App):
    def build(self):
        self.title = "Al-Quran Audio App"
        sm = ScreenManager()
        splash = SplashScreen(name='splash')
        splash.build()
        sm.add_widget(splash)
        sm.add_widget(SurahListScreen(name='surah_list'))
        sm.add_widget(VerseAudioScreen(name='verse_audio'))
        return sm

if __name__ == '__main__':
    QuranApp().run()
