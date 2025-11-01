import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from champions.models import Champion
import time

BASE_URL = "https://wildriftcounter.com"

class Command(BaseCommand):
    help = "Импортирует чемпионов с wildriftcounter.com с ролью и контр-пиками"

    def handle(self, *args, **options):
        self.stdout.write("🔄 Загружаем список чемпионов с главной страницы...")

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(f"{BASE_URL}/champions/", headers=headers)

        if response.status_code != 200:
            self.stderr.write(f"Ошибка загрузки главной страницы: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        figures = soup.select("figure.gallery-item figcaption.wp-caption-text a")

        if not figures:
            self.stderr.write("⚠ Не удалось найти чемпионов на главной странице.")
            return

        self.stdout.write(f"Найдено чемпионов: {len(figures)}")

        for a_tag in figures:
            try:
                champ_name = a_tag.text.strip()
                champ_link = a_tag.get("href")
                if not champ_link.startswith("http"):
                    champ_link = BASE_URL + champ_link

                # Переходим на страницу чемпиона
                champ_page = requests.get(champ_link, headers=headers)
                champ_soup = BeautifulSoup(champ_page.text, "html.parser")

                # Извлекаем роль
                role_tag = champ_soup.select_one("p.has-text-align-center strong")
                role = role_tag.text.strip() if role_tag else "Не указана"

                # Сильные противники
                strong_against = []
                strong_div = champ_soup.find("p", string=lambda t: t and "Strong Against" in t)
                if strong_div:
                    figures_strong = strong_div.find_next_sibling("div").select("figcaption a")
                    strong_against = [f.text.strip() for f in figures_strong]

                # Слабые противники
                weak_against = []
                weak_div = champ_soup.find("p", string=lambda t: t and "Weak Against" in t)
                if weak_div:
                    figures_weak = weak_div.find_next_sibling("div").select("figcaption a")
                    weak_against = [f.text.strip() for f in figures_weak]

                # Сохраняем в базу
                champ_obj, created = Champion.objects.get_or_create(name=champ_name)
                champ_obj.role = role
                champ_obj.save()

                # Очищаем связи ManyToMany
                champ_obj.strong_against.clear()
                champ_obj.weak_against.clear()

                # Добавляем связи
                for s_name in strong_against:
                    target, _ = Champion.objects.get_or_create(name=s_name)
                    champ_obj.strong_against.add(target)

                for w_name in weak_against:
                    target, _ = Champion.objects.get_or_create(name=w_name)
                    champ_obj.weak_against.add(target)

                self.stdout.write(f"✅ Импортирован: {champ_name}")

                time.sleep(0.3)  # чтобы сайт не заблокировал

            except Exception as e:
                self.stderr.write(f"Ошибка при обработке {champ_name}: {e}")

        self.stdout.write("✅ Импорт всех чемпионов завершён!")
