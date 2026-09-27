import os
import sys

import django
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


load_dotenv()

USER_PASSWORD = os.getenv("E2E_USER_PASSWORD")
ADMIN_PASSWORD = os.getenv("E2E_ADMIN_PASSWORD")

if not USER_PASSWORD or not ADMIN_PASSWORD:
    sys.exit("E2E_USER_PASSWORD dan E2E_ADMIN_PASSWORD belum diisi di berkas .env.")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio.settings")
django.setup()

from django.contrib.auth.models import User  # noqa: E402


BASE_URL = "http://127.0.0.1:8000"
USER_USERNAME = "burhan_test"
ADMIN_USERNAME = "admin_test"


def setup_users():
    """Create deterministic accounts used only by this E2E smoke test."""
    user, _ = User.objects.get_or_create(username=USER_USERNAME)
    user.set_password(USER_PASSWORD)
    user.is_superuser = False
    user.is_staff = False
    user.save()

    admin, _ = User.objects.get_or_create(username=ADMIN_USERNAME)
    admin.set_password(ADMIN_PASSWORD)
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()


def login_as(driver, wait, username, password):
    driver.get(f"{BASE_URL}/login/")
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "form.project-form button[type='submit']").click()
    wait.until(EC.url_to_be(f"{BASE_URL}/"))
    wait.until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "p.last-login"), username
        )
    )


def logout(driver, wait):
    driver.get(f"{BASE_URL}/logout/")
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a[href='/login/']")
        )
    )


def main():
    setup_users()

    options = webdriver.ChromeOptions()
    if "--headless" in sys.argv:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    else:
        options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException as error:
        sys.exit(f"ChromeDriver tidak dapat dijalankan: {error}")

    wait = WebDriverWait(driver, 10)

    try:
        # login.html harus merender CSRF hidden input dan cookie.
        try:
            driver.get(f"{BASE_URL}/login/")
        except WebDriverException:
            sys.exit(
                f"Server belum berjalan di {BASE_URL}. "
                "Jalankan 'python3 manage.py runserver' terlebih dahulu."
            )

        csrf = wait.until(
            EC.presence_of_element_located((By.NAME, "csrfmiddlewaretoken"))
        )
        assert csrf.get_attribute("value")
        assert driver.get_cookie("csrftoken")
        print("[PASS] CSRF token dan cookie terverifikasi")

        # index.html menampilkan username hanya ketika user terautentikasi.
        login_as(driver, wait, USER_USERNAME, USER_PASSWORD)
        assert driver.get_cookie("sessionid")
        assert driver.get_cookie("last_login")
        assert "Terakhir Login" in driver.page_source
        assert "Logout" in driver.page_source
        print("[PASS] Login user biasa dan cookie sesi berhasil")

        # create_project tidak dibatasi role. POST-nya dilindungi
        # PORTFOLIO_EDIT_SECRET, sesuai implementasi views.py saat ini.
        driver.get(f"{BASE_URL}/projects/add/")
        wait.until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, "h1"), "Add New Projects"
            )
        )
        wait.until(EC.presence_of_element_located((By.NAME, "edit_secret")))
        print("[PASS] User biasa dapat membuka form proyek")

        # Secret salah harus ditolak tanpa membuat project baru.
        driver.find_element(By.NAME, "title").send_keys("E2E invalid secret")
        driver.find_element(By.NAME, "description").send_keys("E2E validation")
        driver.find_element(By.NAME, "edit_secret").send_keys("invalid-e2e-secret")
        driver.find_element(
            By.CSS_SELECTOR, "form.project-form button[type='submit']"
        ).click()
        wait.until(EC.presence_of_element_located((By.NAME, "edit_secret")))
        assert "Kode rahasia salah!" in driver.page_source
        print("[PASS] Secret proyek yang salah ditolak")

        logout(driver, wait)
        cookie_last_login = driver.get_cookie("last_login")
        assert cookie_last_login is None or cookie_last_login["value"] == ""
        print("[PASS] Logout dan pembersihan cookie berhasil")

        # Tidak ada route project khusus admin; superuser mengikuti flow yang sama.
        login_as(driver, wait, ADMIN_USERNAME, ADMIN_PASSWORD)
        driver.get(f"{BASE_URL}/projects/add/")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "project-form")))
        wait.until(EC.presence_of_element_located((By.NAME, "edit_secret")))
        print("[PASS] Superuser login dan form proyek berhasil")

        logout(driver, wait)
        print("\nSemua pengujian E2E berhasil!")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
