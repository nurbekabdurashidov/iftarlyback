from django.db import models
import base64

# Model for Bot Users
class BotUserModel(models.Model):
    languages = (
        ('uz', "O'zbek"),
        ('en', "English"),
        ('ru', "Русский"),
    )



    name = models.CharField(max_length=300, null=True, blank=True, verbose_name="Full Name",
                            help_text="Enter full name")
    telegram_id = models.CharField(max_length=100, unique=True, verbose_name="Telegram ID",
                                   help_text="Enter telegram id")
    language = models.CharField(max_length=5, default='uz', choices=languages, verbose_name="Language",
                                help_text="Choose language")
    region = models.CharField(max_length=50, verbose_name="Region", blank = True,null = True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name or 'User'} - {self.telegram_id}"

    class Meta:
        verbose_name = 'Bot User'
        verbose_name_plural = 'Bot Users'
class TelegramChannelModel(models.Model):
    channel_id = models.CharField(max_length=150,verbose_name="Channel ID",help_text="Enter channel id",unique=True)
    channel_name = models.CharField(max_length=300,verbose_name="Channel Name",help_text="Enter channel name",null=True,blank=True)
    channel_members_count = models.CharField(max_length=200,null=True,blank=True,verbose_name="Channel Memers Count",help_text="Enter channel members count")
    def __str__(self):
        return f"Channel: {self.channel_id}"
    class Meta:
        verbose_name = 'Telegram Channel'
        verbose_name_plural = 'Telegram Channels'


class Dua(models.Model):
    image = models.ImageField(upload_to="duas/")
    caption = models.TextField()

    def __str__(self):
        return self.caption[:50]


class RamadanTime(models.Model):
    region = models.CharField(max_length=100)  # Region stored as text
    date = models.DateField()
    suhoor_time = models.TimeField()  # Suhoor (Sehri) time
    iftar_time = models.TimeField()   # Iftar time
    image = models.ImageField(upload_to="ramadan_posts/")
    caption = models.TextField()

    class Meta:
        unique_together = ('region', 'date')  # Each region should have one entry per day

    def __str__(self):
        return f"{self.region} - {self.date}"

    @property
    def image_base64(self):
        """Convert image to Base64 string."""
        if self.image:
            with self.image.open("rb") as img_file:
                return base64.b64encode(img_file.read()).decode("utf-8")
        return None


class MonthlyRamadanTime(models.Model):
    image = models.ImageField(upload_to="ramadan_images/", verbose_name="Timetable Image")
    caption = models.TextField(verbose_name="Caption with Time Differences")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ramadan Timetable - {self.caption  }"