from datetime import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
import webbrowser
import customtkinter as ctk

GITHUB_PROFILE_URL = "https://github.com/Vazhnyy"
AUTHOR_NICKNAME = "Vazhnyy"
YOUTUBE_CHANNEL_URL = "https://www.youtube.com/@vaznhyy6969"
YOUTUBE_CHANNEL_LABEL = "@vaznhyy6969"
STARTUP_STRATEGY_VBS_NAME = "ZapretPlus_Strategy.vbs"

# --- Базовая тёмная палитра в стиле Google Material You ---
DEFAULT_DARK_PALETTE = {
    "bg": "#121316",
    "sidebar": "#18191D",
    "card": "#1E1F25",
    "nav_active": "#28354A",
    "accent": "#A8C7FA",
    "accent_hover": "#D3E3FD",
    "accent_text": "#0A141D",
    "text": "#E2E2E6",
    "subtext": "#8E9099",
    "danger": "#F2B8B5",
    "danger_hover": "#8C1D18",
    "danger_text": "#601410",
    "disabled_bg": "#332A29",
    "disabled_text": "#685452",
    "toggle_bg": "#2B2E38",
    "toggle_border": "#52586A",
    "seg_unselected": "#17181C",
}

COLOR_ASPECT_ORDER = [
    "bg",
    "sidebar",
    "card",
    "nav_active",
    "accent",
    "accent_hover",
    "accent_text",
    "text",
    "subtext",
    "danger",
    "danger_hover",
    "danger_text",
    "disabled_bg",
    "disabled_text",
    "toggle_bg",
    "toggle_border",
    "seg_unselected",
]

# --- Словари локализации (RU / EN) ---
TRANSLATIONS = {
    "ru": {
        "app_name": "Zapret+",
        "nav_strategies": "Стратегии",
        "nav_list": "Лист",
        "nav_settings": "Настройки",
        "nav_logs": "Логи",
        "nav_about": "О проекте",
        "subtitle_strategies": "Выберите и запустите нужную стратегию",
        "subtitle_list": "Сайты и IP-адреса из папки lists (list-general.txt и ipset-all.txt)",
        "subtitle_settings": "Сборки zapret, режим запуска, автозагрузка стратегии, палитра и язык",
        "subtitle_logs": "Журнал работы приложения и запуска стратегий",
        "subtitle_about": "Краткая информация о приложении и авторе",
        "top_zapret_none": "Папка не выбрана",
        "settings_path_title": "Сборки и версии zapret",
        "settings_path_desc": "Добавьте несколько папок zapret и переключайтесь между ними, если текущая версия барахлит",
        "zapret_name_placeholder": "Название (например, v1.6.4 или резерв)...",
        "path_placeholder": "Путь к папке zapret-winws (или нажмите «Добавить» для выбора папки)...",
        "browse": "Обзор",
        "add_zapret_btn": "Добавить",
        "use_zapret_btn": "Выбрать",
        "active_zapret_badge": "Активен",
        "delete_zapret_btn": "Удалить",
        "no_zapret_profiles": "Пока не добавлено ни одной сборки zapret. Нажмите «Добавить» и выберите папку.",
        "warn_empty_zapret_path": "Укажите путь к папке zapret перед добавлением!",
        "settings_data_title": "Папка данных ZapretPlus",
        "settings_data_desc": "Здесь хранятся настройки и файл логов",
        "open_data_folder": "Открыть папку",
        "settings_run_mode_title": "Режим работы zapret (из утилиты)",
        "settings_run_mode_desc": "Применяется при запуске из Zapret+: В фоне — без окна; Окно — с окном батника",
        "run_mode_background": "В фоне",
        "run_mode_window": "Окно",
        "current_run_mode_bg": "Сейчас при запуске из утилиты: В фоне",
        "current_run_mode_win": "Сейчас при запуске из утилиты: Окно",
        "settings_autostart_title": "Автозагрузка стратегии",
        "settings_autostart_desc": "Отдельные стратегия и режим для старта с системой (не запускает стратегию при открытии Zapret+)",
        "autostart_strategy_label": "Стратегия для автозапуска:",
        "autostart_strategy_none": "Не выбрана",
        "autostart_mode_label": "Режим при автозапуске:",
        "autostart_enable_btn": "Включить",
        "autostart_disable_btn": "Выключить",
        "open_startup_folder_btn": "Папка автозагрузки",
        "current_autostart_on": "Сейчас включена: {strategy} ({mode})",
        "current_autostart_on_no_strat": "Сейчас включена: стратегия не выбрана",
        "current_autostart_off": "Сейчас выключена: Автозагрузка стратегии",
        "warn_no_strategy_for_autostart": "Выберите стратегию для автозапуска (и проверьте путь к папке zapret).",
        "status_idle": "Статус: Не запущен",
        "status_active": "Активно: {name}",
        "stop": "Остановить",
        "start": "Старт",
        "section_strategies": "Стратегии",
        "no_strategies": "В этой папке не найдено файлов стратегий",
        "no_path_configured": "Укажите путь к папке zapret в разделе Настройки",
        "warn_no_path": "Укажите путь к папке с Zapret+ в настройках!",
        "warn_title": "Внимание",
        "err_launch_title": "Ошибка запуска",
        "err_open_folder_title": "Ошибка",
        "err_open_folder": "Не удалось открыть папку: {error}",
        "err_autostart": "Не удалось изменить автозагрузку стратегии: {error}",
        "clear_logs": "Очистить логи",
        "logs_empty": "Лог пока пуст.",
        "list_tab_domains": "Сайты",
        "list_tab_ips": "IP-адреса",
        "list_search_domains_placeholder": "Поиск по сайтам (list-general.txt)...",
        "list_search_ips_placeholder": "Поиск по IP-адресам (ipset-all.txt)...",
        "list_refresh_btn": "Обновить",
        "list_no_path": "Укажите путь к папке zapret в разделе Настройки, чтобы загрузить списки.",
        "list_files_missing": "В папке lists не найдены файлы list-general.txt и ipset-all.txt.",
        "list_tab_empty": "В этом списке пока нет записей.",
        "list_no_matches": "По запросу «{query}» ничего не найдено.",
        "list_stats_domains": "Сайтов найдено: {shown} из {total} (файл: list-general.txt)",
        "list_stats_ips": "IP-адресов найдено: {shown} из {total} (файл: ipset-all.txt)",
        "list_tag_domain": "САЙТ",
        "list_tag_ip": "IP",
        "settings_palette_title": "Палитра цветов интерфейса",
        "settings_palette_desc": "Стартовая тема — тёмная. Настройте цвет каждого элемента в HEX или через палитру выбора",
        "reset_palette_btn": "Сбросить палитру",
        "pick_color_btn": "Цвет",
        "apply_color_btn": "Применить",
        "invalid_hex_msg": "Введите корректный HEX-цвет в формате #RRGGBB (например, #7C3AED).",
        "aspect_bg": "Основной фон окна",
        "aspect_sidebar": "Боковая панель навигации",
        "aspect_card": "Карточки и панели",
        "aspect_nav_active": "Активный пункт меню",
        "aspect_accent": "Акцентный цвет (кнопки/статус)",
        "aspect_accent_hover": "Наведение на акцент",
        "aspect_accent_text": "Текст на акцентных кнопках",
        "aspect_text": "Основной текст",
        "aspect_subtext": "Второстепенный текст / описания",
        "aspect_danger": "Кнопки стоп / очистка",
        "aspect_danger_hover": "Наведение на стоп / очистку",
        "aspect_danger_text": "Текст на стоп / очистке",
        "aspect_disabled_bg": "Фон неактивной кнопки",
        "aspect_disabled_text": "Текст неактивной кнопки",
        "aspect_toggle_bg": "Поля ввода и переключатели",
        "aspect_toggle_border": "Границы переключателей",
        "aspect_seg_unselected": "Неактивные сегменты",
        "settings_lang_title": "Язык приложения",
        "settings_lang_desc": "Выберите язык интерфейса",
        "current_lang_info": "Сейчас выбран: Русский",
        "switch_lang_btn": "English",
        "browse_dialog_title": "Выберите папку с Zapret+",
        "about_card_title": "Zapret+ — лаунчер стратегий",
        "about_card_desc": "Минималистичный интерфейс с кастомной цветовой палитрой для управления стратегиями zapret.",
        "about_lang_label": "Язык разработки:",
        "about_lang_value": "Python (CustomTkinter)",
        "about_ai_label": "Разработано с помощью ИИ:",
        "about_ai_value": "Gemini",
        "about_author_label": "Ник автора:",
        "about_github_label": "GitHub профиль:",
        "about_youtube_label": "YouTube канал:",
        "open_github_btn": "Открыть GitHub",
        "open_youtube_btn": "Открыть YouTube",
        "log_app_started": "Приложение Zapret+ запущено",
        "log_folder_selected": "Выбрана сборка zapret: {name} ({path})",
        "log_zapret_added": "Добавлена сборка zapret: {name} ({path})",
        "log_zapret_removed": "Удалена сборка zapret: {name} ({path})",
        "log_strategy_started": "Запущена стратегия ({mode}): {name}",
        "log_strategy_stopped": "Остановлена стратегия: {name}",
        "log_stopped_all": "Активные процессы остановлены",
        "log_launch_error": "Ошибка запуска {name}: {error}",
        "log_color_changed": "Цвет «{aspect}» изменён на {color}",
        "log_palette_reset": "Палитра цветов сброшена к базовой тёмной",
        "log_lang_changed": "Язык изменён на: {lang}",
        "log_run_mode_changed": "Режим запуска из утилиты изменён на: {mode}",
        "log_autostart_strategy_changed": "Стратегия автозапуска изменена на: {strategy}",
        "log_autostart_mode_changed": "Режим автозапуска изменён на: {mode}",
        "log_autostart_changed": "Автозагрузка стратегии ({strategy}, {mode}): {state}",
        "log_startup_folder_opened": "Открыта папка автозагрузки",
        "log_github_opened": "Открыт профиль GitHub: {url}",
        "log_youtube_opened": "Открыт канал YouTube: {url}",
        "lang_name_ru": "Русский",
        "lang_name_en": "English",
        "mode_label_bg": "В фоне",
        "mode_label_win": "Окно",
        "state_on": "Включена",
        "state_off": "Выключена",
    },
    "en": {
        "app_name": "Zapret+",
        "nav_strategies": "Strategies",
        "nav_list": "List",
        "nav_settings": "Settings",
        "nav_logs": "Logs",
        "nav_about": "About",
        "subtitle_strategies": "Select and launch a strategy",
        "subtitle_list": "Domains and IPs from the lists folder (list-general.txt and ipset-all.txt)",
        "subtitle_settings": "Zapret builds, launch mode, strategy autostart, color palette, and language",
        "subtitle_logs": "Application event log and strategy launch history",
        "subtitle_about": "Brief details about the project and author",
        "top_zapret_none": "No folder selected",
        "settings_path_title": "Zapret Builds & Versions",
        "settings_path_desc": "Add multiple zapret folders and switch between them if one version acts up",
        "zapret_name_placeholder": "Label (e.g. v1.6.4 or backup)...",
        "path_placeholder": "Path to zapret-winws folder (or click Add to pick a folder)...",
        "browse": "Browse",
        "add_zapret_btn": "Add",
        "use_zapret_btn": "Select",
        "active_zapret_badge": "Active",
        "delete_zapret_btn": "Remove",
        "no_zapret_profiles": "No zapret builds added yet. Click Add and choose a folder.",
        "warn_empty_zapret_path": "Enter a zapret folder path before adding!",
        "settings_data_title": "ZapretPlus Data Folder",
        "settings_data_desc": "Stores configuration and log files",
        "open_data_folder": "Open Folder",
        "settings_run_mode_title": "Zapret Launch Mode (From Utility)",
        "settings_run_mode_desc": "Used when launching from Zapret+: Background — no window; Window — batch window",
        "run_mode_background": "Background",
        "run_mode_window": "Window",
        "current_run_mode_bg": "Current launch mode from utility: Background",
        "current_run_mode_win": "Current launch mode from utility: Window",
        "settings_autostart_title": "Strategy Autostart",
        "settings_autostart_desc": "Separate strategy and mode for system startup (does not launch when opening Zapret+)",
        "autostart_strategy_label": "Autostart strategy:",
        "autostart_strategy_none": "Not selected",
        "autostart_mode_label": "Autostart mode:",
        "autostart_enable_btn": "Enable",
        "autostart_disable_btn": "Disable",
        "open_startup_folder_btn": "Startup Folder",
        "current_autostart_on": "Currently enabled: {strategy} ({mode})",
        "current_autostart_on_no_strat": "Currently enabled: no strategy selected",
        "current_autostart_off": "Currently disabled: Strategy autostart",
        "warn_no_strategy_for_autostart": "Select an autostart strategy (and check the zapret folder path).",
        "status_idle": "Status: Stopped",
        "status_active": "Active: {name}",
        "stop": "Stop",
        "start": "Start",
        "section_strategies": "Strategies",
        "no_strategies": "No strategy scripts found in this folder",
        "no_path_configured": "Set the zapret folder path in Settings",
        "warn_no_path": "Please set the Zapret+ folder path in Settings!",
        "warn_title": "Warning",
        "err_launch_title": "Launch error",
        "err_open_folder_title": "Error",
        "err_open_folder": "Could not open folder: {error}",
        "err_autostart": "Could not update strategy autostart: {error}",
        "clear_logs": "Clear Logs",
        "logs_empty": "Log is empty.",
        "list_tab_domains": "Domains",
        "list_tab_ips": "IP Addresses",
        "list_search_domains_placeholder": "Search domains (list-general.txt)...",
        "list_search_ips_placeholder": "Search IP addresses (ipset-all.txt)...",
        "list_refresh_btn": "Refresh",
        "list_no_path": "Set the zapret folder path in Settings to load lists.",
        "list_files_missing": "list-general.txt and ipset-all.txt were not found in the lists folder.",
        "list_tab_empty": "No entries in this list yet.",
        "list_no_matches": "No matches found for \"{query}\".",
        "list_stats_domains": "Matched {shown} of {total} domains (file: list-general.txt)",
        "list_stats_ips": "Matched {shown} of {total} IPs (file: ipset-all.txt)",
        "list_tag_domain": "DOMAIN",
        "list_tag_ip": "IP",
        "settings_palette_title": "Interface Color Palette",
        "settings_palette_desc": "Default theme is dark. Customize every UI element via HEX or color picker",
        "reset_palette_btn": "Reset Palette",
        "pick_color_btn": "Pick",
        "apply_color_btn": "Apply",
        "invalid_hex_msg": "Enter a valid HEX color like #7C3AED.",
        "aspect_bg": "Main window background",
        "aspect_sidebar": "Navigation sidebar",
        "aspect_card": "Cards and panels",
        "aspect_nav_active": "Active navigation item",
        "aspect_accent": "Accent color (buttons/status)",
        "aspect_accent_hover": "Accent hover state",
        "aspect_accent_text": "Accent button text",
        "aspect_text": "Primary text",
        "aspect_subtext": "Secondary text / descriptions",
        "aspect_danger": "Stop / clear buttons",
        "aspect_danger_hover": "Stop / clear hover state",
        "aspect_danger_text": "Stop / clear button text",
        "aspect_disabled_bg": "Disabled button background",
        "aspect_disabled_text": "Disabled button text",
        "aspect_toggle_bg": "Inputs and toggles",
        "aspect_toggle_border": "Toggle borders",
        "aspect_seg_unselected": "Unselected segments",
        "settings_lang_title": "App Language",
        "settings_lang_desc": "Choose interface language",
        "current_lang_info": "Current: English",
        "switch_lang_btn": "Русский",
        "browse_dialog_title": "Select Zapret+ folder",
        "about_card_title": "Zapret+ Strategy Launcher",
        "about_card_desc": "Minimalistic interface with a custom color palette for managing zapret strategies.",
        "about_lang_label": "Language:",
        "about_lang_value": "Python (CustomTkinter)",
        "about_ai_label": "Built with AI:",
        "about_ai_value": "Gemini",
        "about_author_label": "Author nickname:",
        "about_github_label": "GitHub profile:",
        "about_youtube_label": "YouTube channel:",
        "open_github_btn": "Open GitHub",
        "open_youtube_btn": "Open YouTube",
        "log_app_started": "Zapret+ started",
        "log_folder_selected": "Selected zapret build: {name} ({path})",
        "log_zapret_added": "Added zapret build: {name} ({path})",
        "log_zapret_removed": "Removed zapret build: {name} ({path})",
        "log_strategy_started": "Started strategy ({mode}): {name}",
        "log_strategy_stopped": "Stopped strategy: {name}",
        "log_stopped_all": "Active processes stopped",
        "log_launch_error": "Failed to start {name}: {error}",
        "log_color_changed": "Color \"{aspect}\" changed to {color}",
        "log_palette_reset": "Color palette reset to default dark",
        "log_lang_changed": "Language changed to: {lang}",
        "log_run_mode_changed": "Utility launch mode changed to: {mode}",
        "log_autostart_strategy_changed": "Autostart strategy changed to: {strategy}",
        "log_autostart_mode_changed": "Autostart mode changed to: {mode}",
        "log_autostart_changed": "Strategy autostart ({strategy}, {mode}): {state}",
        "log_startup_folder_opened": "Opened Windows Startup folder",
        "log_github_opened": "Opened GitHub profile: {url}",
        "log_youtube_opened": "Opened YouTube channel: {url}",
        "lang_name_ru": "Russian",
        "lang_name_en": "English",
        "mode_label_bg": "Background",
        "mode_label_win": "Window",
        "state_on": "Enabled",
        "state_off": "Disabled",
    },
}

ctk.set_default_color_theme("blue")


def _normalize_hex_color(value):
    if not isinstance(value, str):
        return None
    s = value.strip()
    if not s.startswith("#"):
        s = "#" + s
    if re.fullmatch(r"#[0-9A-Fa-f]{6}", s):
        return s.upper()
    return None


def _folder_basename(path_str):
    if not path_str:
        return ""
    return os.path.basename(path_str.strip().rstrip("/\\")) or path_str.strip()


def _clean_profile_name(raw_name, folder_path):
    fallback = _folder_basename(folder_path)
    if not isinstance(raw_name, str) or not raw_name.strip():
        return fallback
    cleaned = raw_name.strip()
    cleaned = re.sub(r"\s*\([A-Za-z]:[/\\].*\)\s*$", "", cleaned).strip()
    if re.fullmatch(r"[A-Za-z]:[/\\].*", cleaned) or ("/" in cleaned or "\\" in cleaned):
        return _folder_basename(cleaned) or fallback
    return cleaned or fallback


def _norm_path_key(path_str):
    if not path_str:
        return ""
    return os.path.normcase(os.path.abspath(path_str.strip()))


class ZapretPlusApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        user_home = os.path.expanduser("~")
        self.app_data_dir = os.path.join(user_home, "ZapretPlus")
        os.makedirs(self.app_data_dir, exist_ok=True)

        self.config_path = os.path.join(self.app_data_dir, "config.json")
        self.log_path = os.path.join(self.app_data_dir, "zapret_plus.log")
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", encoding="utf-8"):
                pass

        config = self._load_config()

        # Стартовая тема всегда тёмная ("Dark"), без светлой темы
        self.current_mode = "Dark"
        self.current_lang = config.get("lang", "ru") if config.get("lang") in TRANSLATIONS else "ru"
        self.zapret_dir = config.get("zapret_dir", "").strip() if isinstance(config.get("zapret_dir"), str) else ""

        # Список сохранённых сборок zapret: [{"name": "...", "path": "..."}, ...]
        self.zapret_profiles = []
        raw_profiles = config.get("zapret_profiles")
        if isinstance(raw_profiles, list):
            for entry in raw_profiles:
                if isinstance(entry, dict) and isinstance(entry.get("path"), str) and entry["path"].strip():
                    p_path = entry["path"].strip()
                    p_name = _clean_profile_name(entry.get("name"), p_path)
                    if not any(_norm_path_key(x["path"]) == _norm_path_key(p_path) for x in self.zapret_profiles):
                        self.zapret_profiles.append({"name": p_name, "path": p_path})

        if self.zapret_dir and not any(
            _norm_path_key(x["path"]) == _norm_path_key(self.zapret_dir) for x in self.zapret_profiles
        ):
            self.zapret_profiles.insert(0, {"name": _folder_basename(self.zapret_dir), "path": self.zapret_dir})

        if not self.zapret_dir and self.zapret_profiles:
            self.zapret_dir = self.zapret_profiles[0]["path"]

        # Загружаем полную кастомную палитру цветов
        self.palette_colors = dict(DEFAULT_DARK_PALETTE)
        saved_palette = config.get("palette")
        if isinstance(saved_palette, dict):
            for key in COLOR_ASPECT_ORDER:
                norm = _normalize_hex_color(saved_palette.get(key))
                if norm:
                    self.palette_colors[key] = norm

        # Основной режим запуска при клике в самой утилите
        run_mode_cfg = config.get("run_mode", "background")
        self.run_mode = run_mode_cfg if run_mode_cfg in ("background", "window") else "background"

        # Отдельные настройки для автозапуска стратегии с системой
        self.autostart_strategy = config.get("autostart_strategy", "")
        autostart_mode_cfg = config.get("autostart_run_mode", self.run_mode)
        self.autostart_run_mode = (
            autostart_mode_cfg if autostart_mode_cfg in ("background", "window") else "background"
        )
        self.autostart_enabled = self._read_autostart_state()

        self.active_tab = "strategies"
        self.active_list_subtab = "domain"  # "domain" | "ip"
        self._list_search_after_id = None
        self._settings_wheel_bound = False
        self._top_zapret_label_to_path = {}
        self.palette_controls = {}

        ctk.set_appearance_mode("Dark")

        self.title("Zapret+")
        self.geometry("1060x680")
        self.minsize(960, 580)

        self.active_process = None
        self.active_strategy_name = None
        self._temp_bg_script = None
        # [(kind, value, value_lower, source), ...]
        self.list_entries = []

        # Игнорируемые служебные файлы (не являются стратегиями)
        self.ignored_files = {
            "service.bat",
            "service.cmd",
            "service_install.bat",
            "service_remove.bat",
            "service_status.bat",
            "check.bat",
        }

        self._setup_ui()
        if self.zapret_dir:
            self.path_entry.insert(0, self.zapret_dir)

        self.refresh_top_zapret_selector()
        self.refresh_autostart_strategy_options()
        self._write_log(self._tr("log_app_started"))
        self._switch_tab(self.active_tab, apply_only=True)
        self._apply_theme()
        self.refresh_logs()

    def _tr(self, key, **kwargs):
        text = TRANSLATIONS.get(self.current_lang, TRANSLATIONS["ru"]).get(key, key)
        return text.format(**kwargs) if kwargs else text

    def _palette(self):
        return self.palette_colors

    def _get_active_zapret_name(self):
        if not self.zapret_dir:
            return "-"
        norm_active = _norm_path_key(self.zapret_dir)
        for item in self.zapret_profiles:
            if _norm_path_key(item["path"]) == norm_active:
                return item["name"]
        return _folder_basename(self.zapret_dir)

    def _format_top_zapret_label(self, profile):
        folder_name = _folder_basename(profile.get("path", ""))
        return folder_name or self._tr("top_zapret_none")

    def refresh_top_zapret_selector(self):
        if not hasattr(self, "top_zapret_menu"):
            return

        label_map = {}
        values = []
        used_labels = set()

        for profile in self.zapret_profiles:
            base_label = self._format_top_zapret_label(profile)
            label = base_label
            if label in used_labels:
                label = f"{base_label} #{len(values) + 1}"
            used_labels.add(label)
            values.append(label)
            label_map[label] = profile["path"]

        if self.zapret_dir:
            norm_active = _norm_path_key(self.zapret_dir)
            matched_label = None
            for lbl, p_path in label_map.items():
                if _norm_path_key(p_path) == norm_active:
                    matched_label = lbl
                    break
            if matched_label is None:
                folder_only = _folder_basename(self.zapret_dir) or self._tr("top_zapret_none")
                if folder_only in used_labels:
                    folder_only = f"{folder_only} #0"
                values.insert(0, folder_only)
                label_map[folder_only] = self.zapret_dir
                matched_label = folder_only
            selected = matched_label
        else:
            none_lbl = self._tr("top_zapret_none")
            if not values:
                values = [none_lbl]
            selected = values[0] if self.zapret_profiles else none_lbl

        self._top_zapret_label_to_path = label_map
        self.top_zapret_menu.configure(values=values)
        self.top_zapret_var.set(selected)

    def _on_top_zapret_selected(self, choice):
        target_path = self._top_zapret_label_to_path.get(choice)
        if not target_path:
            return
        if self.zapret_dir and _norm_path_key(self.zapret_dir) == _norm_path_key(target_path):
            return
        self._activate_zapret_path(target_path, log_selection=True)

    def _activate_zapret_path(self, new_path, custom_name=None, log_selection=True):
        cleaned = (new_path or "").strip()
        if not cleaned:
            return
        if self.active_strategy_name or self.active_process:
            self.stop_strategy()

        self.zapret_dir = cleaned
        norm_new = _norm_path_key(cleaned)
        matched_name = None
        for item in self.zapret_profiles:
            if _norm_path_key(item["path"]) == norm_new:
                if custom_name:
                    item["name"] = _clean_profile_name(custom_name, cleaned)
                matched_name = item["name"]
                break

        if matched_name is None:
            matched_name = _clean_profile_name(custom_name, cleaned)
            self.zapret_profiles.append({"name": matched_name, "path": cleaned})

        if hasattr(self, "path_entry"):
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, cleaned)

        self._save_config()
        self.refresh_top_zapret_selector()
        self.refresh_autostart_strategy_options()
        self._apply_autostart_ui()
        self._render_zapret_profiles()

        if log_selection:
            self._write_log(self._tr("log_folder_selected", name=matched_name, path=cleaned))

        if self.active_tab == "strategies":
            self.load_strategies()
        elif self.active_tab == "list":
            self.load_lists_data()

    def add_zapret_profile(self):
        folder = filedialog.askdirectory(parent=self, title=self._tr("browse_dialog_title"))
        if not folder:
            return

        raw_path = folder.strip()
        raw_name = self.zapret_name_entry.get().strip() if hasattr(self, "zapret_name_entry") else ""
        name = _clean_profile_name(raw_name, raw_path)

        if hasattr(self, "path_entry"):
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, raw_path)

        norm_new = _norm_path_key(raw_path)
        exists = False
        for item in self.zapret_profiles:
            if _norm_path_key(item["path"]) == norm_new:
                item["name"] = name
                item["path"] = raw_path
                exists = True
                break
        if not exists:
            self.zapret_profiles.append({"name": name, "path": raw_path})

        if hasattr(self, "zapret_name_entry"):
            self.zapret_name_entry.delete(0, tk.END)

        self.zapret_dir = raw_path
        if self.active_strategy_name or self.active_process:
            self.stop_strategy()

        self._save_config()
        self.refresh_top_zapret_selector()
        self.refresh_autostart_strategy_options()
        self._apply_autostart_ui()
        self._render_zapret_profiles()
        self._write_log(self._tr("log_zapret_added", name=name, path=raw_path))

        if self.active_tab == "strategies":
            self.load_strategies()
        elif self.active_tab == "list":
            self.load_lists_data()

    def remove_zapret_profile(self, target_path):
        norm_target = _norm_path_key(target_path)
        removed = None
        remaining = []
        for item in self.zapret_profiles:
            if _norm_path_key(item["path"]) == norm_target and removed is None:
                removed = item
            else:
                remaining.append(item)
        if not removed:
            return

        self.zapret_profiles = remaining
        if self.zapret_dir and _norm_path_key(self.zapret_dir) == norm_target:
            if self.active_strategy_name or self.active_process:
                self.stop_strategy()
            self.zapret_dir = self.zapret_profiles[0]["path"] if self.zapret_profiles else ""
            if hasattr(self, "path_entry"):
                self.path_entry.delete(0, tk.END)
                if self.zapret_dir:
                    self.path_entry.insert(0, self.zapret_dir)

        self._save_config()
        self.refresh_top_zapret_selector()
        self.refresh_autostart_strategy_options()
        self._apply_autostart_ui()
        self._render_zapret_profiles()
        self._write_log(self._tr("log_zapret_removed", name=removed["name"], path=removed["path"]))

        if self.active_tab == "strategies":
            self.load_strategies()
        elif self.active_tab == "list":
            self.load_lists_data()

    def _render_zapret_profiles(self):
        if not hasattr(self, "zapret_profiles_box"):
            return
        for widget in self.zapret_profiles_box.winfo_children():
            widget.destroy()

        p = self._palette()
        if not self.zapret_profiles:
            empty_lbl = ctk.CTkLabel(
                self.zapret_profiles_box,
                text=self._tr("no_zapret_profiles"),
                text_color=p["subtext"],
                font=ctk.CTkFont(family="Segoe UI", size=12),
                anchor="w",
            )
            empty_lbl.pack(fill="x", padx=6, pady=6)
            return

        norm_active = _norm_path_key(self.zapret_dir) if self.zapret_dir else ""
        for idx, profile in enumerate(self.zapret_profiles):
            p_path = profile["path"]
            p_name = _clean_profile_name(profile["name"], p_path)
            is_active = bool(norm_active and _norm_path_key(p_path) == norm_active)
            bottom_pad = 4 if idx == len(self.zapret_profiles) - 1 else 6

            row = ctk.CTkFrame(
                self.zapret_profiles_box,
                fg_color=p["nav_active"] if is_active else p["seg_unselected"],
                corner_radius=14,
            )
            row.pack(fill="x", pady=(0, bottom_pad))

            del_btn = ctk.CTkButton(
                row,
                text=self._tr("delete_zapret_btn"),
                width=82,
                height=30,
                corner_radius=15,
                fg_color=p["toggle_bg"],
                hover_color=p["danger_hover"],
                text_color=p["danger"],
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                command=lambda path=p_path: self.remove_zapret_profile(path),
            )
            del_btn.pack(side="right", padx=(6, 10), pady=8)

            if is_active:
                active_badge = ctk.CTkButton(
                    row,
                    text=self._tr("active_zapret_badge"),
                    width=88,
                    height=30,
                    corner_radius=15,
                    state="disabled",
                    fg_color=p["accent"],
                    text_color=p["accent_text"],
                    font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                )
                active_badge.pack(side="right", padx=(4, 0), pady=8)
            else:
                select_btn = ctk.CTkButton(
                    row,
                    text=self._tr("use_zapret_btn"),
                    width=88,
                    height=30,
                    corner_radius=15,
                    fg_color=p["accent"],
                    hover_color=p["accent_hover"],
                    text_color=p["accent_text"],
                    font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                    command=lambda path=p_path: self._activate_zapret_path(path, log_selection=True),
                )
                select_btn.pack(side="right", padx=(4, 0), pady=8)

            info_box = ctk.CTkFrame(row, fg_color="transparent")
            info_box.pack(side="left", fill="x", expand=True, padx=(12, 8), pady=6)

            title_lbl = ctk.CTkLabel(
                info_box,
                text=p_name,
                text_color=p["accent"] if is_active else p["text"],
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                anchor="w",
            )
            title_lbl.pack(fill="x")

            path_lbl = ctk.CTkLabel(
                info_box,
                text=p_path,
                text_color=p["subtext"],
                font=ctk.CTkFont(family="Consolas", size=11),
                anchor="w",
            )
            path_lbl.pack(fill="x")

    def _set_aspect_color(self, aspect_key, hex_value):
        norm = _normalize_hex_color(hex_value)
        if not norm:
            messagebox.showwarning(self._tr("warn_title"), self._tr("invalid_hex_msg"))
            return False
        self.palette_colors[aspect_key] = norm
        self._save_config()
        aspect_name = self._tr(f"aspect_{aspect_key}")
        self._write_log(self._tr("log_color_changed", aspect=aspect_name, color=norm))
        self._apply_theme()
        if self.active_tab == "strategies":
            self.load_strategies()
        elif self.active_tab == "list":
            self.render_list_results()
        return True

    def _pick_color_for_aspect(self, aspect_key):
        current = self.palette_colors.get(aspect_key, DEFAULT_DARK_PALETTE[aspect_key])
        picked = colorchooser.askcolor(color=current, title=self._tr(f"aspect_{aspect_key}"))
        if picked and picked[1]:
            ctrl = self.palette_controls.get(aspect_key)
            if ctrl:
                ctrl["entry"].delete(0, tk.END)
                ctrl["entry"].insert(0, picked[1].upper())
            self._set_aspect_color(aspect_key, picked[1])

    def _apply_entry_color_for_aspect(self, aspect_key):
        ctrl = self.palette_controls.get(aspect_key)
        if not ctrl:
            return
        self._set_aspect_color(aspect_key, ctrl["entry"].get())

    def reset_palette_colors(self):
        self.palette_colors = dict(DEFAULT_DARK_PALETTE)
        self._save_config()
        self._write_log(self._tr("log_palette_reset"))
        self._apply_theme()
        if self.active_tab == "strategies":
            self.load_strategies()
        elif self.active_tab == "list":
            self.render_list_results()

    def _get_strategy_files(self):
        if not self.zapret_dir or not os.path.isdir(self.zapret_dir):
            return []
        try:
            files = [
                f
                for f in os.listdir(self.zapret_dir)
                if f.lower().endswith((".bat", ".cmd")) and f.lower() not in self.ignored_files
            ]
        except Exception:
            return []
        files.sort(key=lambda x: (not ("alt" in x.lower()), x.lower()))
        return files

    def refresh_autostart_strategy_options(self):
        if not hasattr(self, "autostart_strategy_menu"):
            return
        none_label = self._tr("autostart_strategy_none")
        files = self._get_strategy_files()
        options = files if files else [none_label]

        self.autostart_strategy_menu.configure(values=options)

        if self.autostart_strategy and (not files or self.autostart_strategy in files):
            selected = self.autostart_strategy
        elif files:
            selected = files[0]
        else:
            selected = none_label

        self.autostart_strategy_var.set(selected)

    def _on_autostart_strategy_selected(self, choice):
        none_label = self._tr("autostart_strategy_none")
        if choice == none_label:
            self.autostart_strategy = ""
        else:
            self.autostart_strategy = choice
        self._save_config()
        if self.autostart_enabled and self.autostart_strategy and self.zapret_dir:
            try:
                self._write_strategy_startup_vbs()
            except Exception:
                pass
        if self.autostart_strategy:
            self._write_log(self._tr("log_autostart_strategy_changed", strategy=self.autostart_strategy))
        self._apply_autostart_ui()

    def _get_startup_dir(self):
        if os.name == "nt":
            startup_dir = os.path.join(
                os.environ.get("APPDATA", os.path.expanduser("~")),
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs",
                "Startup",
            )
            os.makedirs(startup_dir, exist_ok=True)
            return startup_dir
        return os.path.expanduser("~/.config/autostart")

    def _get_startup_strategy_vbs_path(self):
        return os.path.join(self._get_startup_dir(), STARTUP_STRATEGY_VBS_NAME)

    def _read_autostart_state(self):
        if os.name != "nt":
            return False
        return os.path.isfile(self._get_startup_strategy_vbs_path())

    def _write_strategy_startup_vbs(self):
        if not self.zapret_dir or not self.autostart_strategy:
            return False
        strategy_path = os.path.join(self.zapret_dir, self.autostart_strategy)
        vbs_path = self._get_startup_strategy_vbs_path()

        escaped_dir = self.zapret_dir.replace('"', '""')
        escaped_bat = strategy_path.replace('"', '""')

        if self.autostart_run_mode == "background":
            cmd_line = f'cmd.exe /d /c ""{escaped_bat}""'
            vbs_content = (
                'Set WshShell = CreateObject("WScript.Shell")\n'
                f'WshShell.CurrentDirectory = "{escaped_dir}"\n'
                f'WshShell.Run "{cmd_line}", 0, False\n'
            )
        else:
            cmd_line = f'cmd.exe /c ""{escaped_bat}""'
            vbs_content = (
                'Set WshShell = CreateObject("WScript.Shell")\n'
                f'WshShell.CurrentDirectory = "{escaped_dir}"\n'
                f'WshShell.Run "{cmd_line}", 1, False\n'
            )

        with open(vbs_path, "w", encoding="utf-8") as f:
            f.write(vbs_content)
        return True

    def _remove_strategy_startup_vbs(self):
        vbs_path = self._get_startup_strategy_vbs_path()
        if os.path.exists(vbs_path):
            os.remove(vbs_path)

    def _set_autostart_state(self, enable):
        if os.name != "nt":
            messagebox.showinfo(self._tr("warn_title"), "Strategy autostart is supported on Windows.")
            return False
        try:
            if enable:
                if not self.zapret_dir or not self.autostart_strategy:
                    messagebox.showwarning(self._tr("warn_title"), self._tr("warn_no_strategy_for_autostart"))
                    return False
                return self._write_strategy_startup_vbs()
            else:
                self._remove_strategy_startup_vbs()
                return True
        except Exception as e:
            messagebox.showerror(
                self._tr("err_open_folder_title"),
                self._tr("err_autostart", error=e),
            )
            return False

    def open_startup_folder(self):
        try:
            if os.name == "nt":
                os.startfile(self._get_startup_dir())
            elif sys.platform == "darwin":
                subprocess.run(["open", os.path.expanduser("~/Library/LaunchAgents")], check=False)
            else:
                subprocess.run(["xdg-open", self._get_startup_dir()], check=False)
            self._write_log(self._tr("log_startup_folder_opened"))
        except Exception as e:
            messagebox.showerror(
                self._tr("err_open_folder_title"),
                self._tr("err_open_folder", error=e),
            )

    def set_run_mode(self, mode):
        if mode not in ("background", "window"):
            return
        self.run_mode = mode
        self._save_config()
        mode_label = self._tr("mode_label_bg") if mode == "background" else self._tr("mode_label_win")
        self._write_log(self._tr("log_run_mode_changed", mode=mode_label))
        self._apply_run_mode_ui()

    def set_autostart_run_mode(self, mode):
        if mode not in ("background", "window"):
            return
        self.autostart_run_mode = mode
        self._save_config()
        if self.autostart_enabled and self.autostart_strategy and self.zapret_dir:
            try:
                self._write_strategy_startup_vbs()
            except Exception:
                pass
        mode_label = self._tr("mode_label_bg") if mode == "background" else self._tr("mode_label_win")
        self._write_log(self._tr("log_autostart_mode_changed", mode=mode_label))
        self._apply_autostart_ui()

    def _apply_run_mode_ui(self):
        p = self._palette()
        self.run_mode_bg_btn.configure(text=self._tr("run_mode_background"))
        self.run_mode_win_btn.configure(text=self._tr("run_mode_window"))

        if self.run_mode == "background":
            self.run_mode_bg_btn.configure(
                fg_color=p["accent"],
                hover_color=p["accent_hover"],
                text_color=p["accent_text"],
            )
            self.run_mode_win_btn.configure(
                fg_color=p["toggle_bg"],
                hover_color=p["seg_unselected"],
                text_color=p["text"],
            )
            self.current_run_mode_label.configure(text=self._tr("current_run_mode_bg"), text_color=p["accent"])
        else:
            self.run_mode_win_btn.configure(
                fg_color=p["accent"],
                hover_color=p["accent_hover"],
                text_color=p["accent_text"],
            )
            self.run_mode_bg_btn.configure(
                fg_color=p["toggle_bg"],
                hover_color=p["seg_unselected"],
                text_color=p["text"],
            )
            self.current_run_mode_label.configure(text=self._tr("current_run_mode_win"), text_color=p["accent"])

    def _apply_autostart_ui(self):
        p = self._palette()
        self.autostart_card.configure(fg_color=p["card"])
        self.settings_autostart_title.configure(text=self._tr("settings_autostart_title"), text_color=p["text"])
        self.settings_autostart_desc.configure(text=self._tr("settings_autostart_desc"), text_color=p["subtext"])
        self.autostart_strategy_lbl.configure(text=self._tr("autostart_strategy_label"), text_color=p["text"])
        self.autostart_mode_lbl.configure(text=self._tr("autostart_mode_label"), text_color=p["text"])

        self.refresh_autostart_strategy_options()
        self.autostart_strategy_menu.configure(
            fg_color=p["toggle_bg"],
            button_color=p["toggle_bg"],
            button_hover_color=p["seg_unselected"],
            dropdown_fg_color=p["toggle_bg"],
            dropdown_hover_color=p["nav_active"],
            dropdown_text_color=p["text"],
            text_color=p["text"],
        )

        self.autostart_bg_btn.configure(text=self._tr("run_mode_background"))
        self.autostart_win_btn.configure(text=self._tr("run_mode_window"))
        if self.autostart_run_mode == "background":
            self.autostart_bg_btn.configure(
                fg_color=p["accent"],
                hover_color=p["accent_hover"],
                text_color=p["accent_text"],
            )
            self.autostart_win_btn.configure(
                fg_color=p["toggle_bg"],
                hover_color=p["seg_unselected"],
                text_color=p["text"],
            )
        else:
            self.autostart_win_btn.configure(
                fg_color=p["accent"],
                hover_color=p["accent_hover"],
                text_color=p["accent_text"],
            )
            self.autostart_bg_btn.configure(
                fg_color=p["toggle_bg"],
                hover_color=p["seg_unselected"],
                text_color=p["text"],
            )

        self.open_startup_folder_btn.configure(
            text=self._tr("open_startup_folder_btn"),
            fg_color=p["toggle_bg"],
            hover_color=p["seg_unselected"],
            text_color=p["text"],
        )

        mode_label = (
            self._tr("mode_label_bg") if self.autostart_run_mode == "background" else self._tr("mode_label_win")
        )

        if self.autostart_enabled:
            self.autostart_toggle_btn.configure(
                text=self._tr("autostart_disable_btn"),
                fg_color=p["accent"],
                hover_color=p["accent_hover"],
                text_color=p["accent_text"],
            )
            if self.autostart_strategy:
                status_txt = self._tr("current_autostart_on", strategy=self.autostart_strategy, mode=mode_label)
            else:
                status_txt = self._tr("current_autostart_on_no_strat")
            self.current_autostart_label.configure(text=status_txt, text_color=p["accent"])
        else:
            self.autostart_toggle_btn.configure(
                text=self._tr("autostart_enable_btn"),
                fg_color=p["accent"],
                hover_color=p["accent_hover"],
                text_color=p["accent_text"],
            )
            self.current_autostart_label.configure(text=self._tr("current_autostart_off"), text_color=p["accent"])

    def _apply_palette_editor_ui(self):
        p = self._palette()
        self.palette_card.configure(fg_color=p["card"])
        self.settings_palette_title.configure(text=self._tr("settings_palette_title"), text_color=p["text"])
        self.settings_palette_desc.configure(text=self._tr("settings_palette_desc"), text_color=p["subtext"])
        self.reset_palette_btn.configure(
            text=self._tr("reset_palette_btn"),
            fg_color=p["toggle_bg"],
            hover_color=p["seg_unselected"],
            text_color=p["text"],
        )

        for aspect_key, ctrl in self.palette_controls.items():
            color_val = p.get(aspect_key, DEFAULT_DARK_PALETTE[aspect_key])
            ctrl["row"].configure(fg_color=p["seg_unselected"])
            ctrl["label"].configure(text=self._tr(f"aspect_{aspect_key}"), text_color=p["text"])
            ctrl["swatch"].configure(fg_color=color_val, border_color=p["toggle_border"], border_width=1)
            ctrl["entry"].configure(
                fg_color=p["toggle_bg"],
                text_color=p["text"],
                placeholder_text_color=p["subtext"],
            )
            if self.focus_get() is not ctrl["entry"]:
                ctrl["entry"].delete(0, tk.END)
                ctrl["entry"].insert(0, color_val)
            ctrl["pick_btn"].configure(
                text=self._tr("pick_color_btn"),
                fg_color=p["toggle_bg"],
                hover_color=p["nav_active"],
                text_color=p["text"],
            )
            ctrl["apply_btn"].configure(
                text=self._tr("apply_color_btn"),
                fg_color=p["accent"],
                hover_color=p["accent_hover"],
                text_color=p["accent_text"],
            )

    def toggle_autostart(self):
        target = not self.autostart_enabled
        if self._set_autostart_state(target):
            self.autostart_enabled = target
            state_label = self._tr("state_on") if target else self._tr("state_off")
            strat_name = self.autostart_strategy or "-"
            mode_label = (
                self._tr("mode_label_bg") if self.autostart_run_mode == "background" else self._tr("mode_label_win")
            )
            self._write_log(
                self._tr("log_autostart_changed", strategy=strat_name, mode=mode_label, state=state_label)
            )
            self._apply_autostart_ui()

    def _bind_settings_mousewheel_once(self):
        if self._settings_wheel_bound:
            return
        canvas = getattr(self.settings_view, "_parent_canvas", None)
        if canvas is None:
            return

        def _scroll_canvas(delta_units):
            canvas.yview_scroll(delta_units, "units")
            return "break"

        def _on_mousewheel(event):
            if isinstance(event.widget, tk.Entry):
                return None
            if getattr(event, "num", None) == 4:
                return _scroll_canvas(-18)
            if getattr(event, "num", None) == 5:
                return _scroll_canvas(18)
            delta = getattr(event, "delta", 0)
            if delta:
                steps = max(1, int(abs(delta) / 120)) * 18
                return _scroll_canvas(-steps if delta > 0 else steps)
            return None

        def _attach(w):
            w.bind("<MouseWheel>", _on_mousewheel, add="+")
            w.bind("<Button-4>", _on_mousewheel, add="+")
            w.bind("<Button-5>", _on_mousewheel, add="+")
            for child in w.winfo_children():
                _attach(child)

        _attach(self.settings_view)
        self._settings_wheel_bound = True

    def _write_log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {message}\n"
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception:
            pass
        if hasattr(self, "logs_textbox"):
            self.refresh_logs()

    def refresh_logs(self):
        if not hasattr(self, "logs_textbox"):
            return
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            content = ""

        self.logs_textbox.configure(state="normal")
        self.logs_textbox.delete("1.0", tk.END)
        self.logs_textbox.insert("1.0", content if content.strip() else self._tr("logs_empty"))
        self.logs_textbox.see(tk.END)
        self.logs_textbox.configure(state="disabled")

    def clear_logs(self):
        try:
            with open(self.log_path, "w", encoding="utf-8"):
                pass
        except Exception:
            pass
        self.refresh_logs()

    def open_data_folder(self):
        try:
            if os.name == "nt":
                os.startfile(self.app_data_dir)
            elif sys.platform == "darwin":
                subprocess.run(["open", self.app_data_dir], check=False)
            else:
                subprocess.run(["xdg-open", self.app_data_dir], check=False)
        except Exception as e:
            messagebox.showerror(
                self._tr("err_open_folder_title"),
                self._tr("err_open_folder", error=e),
            )

    def open_github_profile(self):
        webbrowser.open(GITHUB_PROFILE_URL)
        self._write_log(self._tr("log_github_opened", url=GITHUB_PROFILE_URL))

    def open_youtube_channel(self):
        if not YOUTUBE_CHANNEL_URL.strip():
            return
        webbrowser.open(YOUTUBE_CHANNEL_URL.strip())
        self._write_log(self._tr("log_youtube_opened", url=YOUTUBE_CHANNEL_URL.strip()))

    def _find_lists_dir(self):
        if not self.zapret_dir:
            return None
        candidates = [
            os.path.join(self.zapret_dir, "lists"),
            os.path.join(os.path.dirname(self.zapret_dir), "lists"),
        ]
        for path in candidates:
            if os.path.isdir(path):
                return path
        return None

    def _parse_list_file(self, filepath, kind):
        items = []
        if not filepath or not os.path.isfile(filepath):
            return items
        source_name = os.path.basename(filepath)
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                for raw_line in f:
                    line = raw_line.strip()
                    if not line or line.startswith("#") or line.startswith(";"):
                        continue
                    if "#" in line:
                        line = line.split("#", 1)[0].strip()
                    if line:
                        items.append((kind, line, line.lower(), source_name))
        except Exception:
            pass
        return items

    def load_lists_data(self):
        entries = []
        lists_dir = self._find_lists_dir()
        if lists_dir:
            entries.extend(self._parse_list_file(os.path.join(lists_dir, "list-general.txt"), "domain"))
            entries.extend(self._parse_list_file(os.path.join(lists_dir, "ipset-all.txt"), "ip"))
        self.list_entries = entries
        self.render_list_results()

    def _switch_list_subtab(self, kind):
        if kind in ("domain", "ip"):
            self.active_list_subtab = kind
            self._apply_theme()
            self.render_list_results()

    def _schedule_list_filter(self, _event=None):
        if self._list_search_after_id is not None:
            self.after_cancel(self._list_search_after_id)
        self._list_search_after_id = self.after(120, self.render_list_results)

    def _set_list_textbox_content(self, text):
        self.list_textbox.configure(state="normal")
        self.list_textbox.delete("1.0", tk.END)
        self.list_textbox.insert("1.0", text)
        self.list_textbox.configure(state="disabled")

    def render_list_results(self):
        self._list_search_after_id = None
        if not hasattr(self, "list_textbox"):
            return

        p = self._palette()
        is_domain_tab = self.active_list_subtab == "domain"
        subtab_entries = [item for item in self.list_entries if item[0] == self.active_list_subtab]
        total_in_tab = len(subtab_entries)
        stats_key = "list_stats_domains" if is_domain_tab else "list_stats_ips"

        if not self.zapret_dir or not os.path.exists(self.zapret_dir):
            msg = self._tr("list_no_path")
            self.list_stats_label.configure(text=msg, text_color=p["subtext"])
            self._set_list_textbox_content(msg)
            return

        if not self._find_lists_dir() or len(self.list_entries) == 0:
            msg = self._tr("list_files_missing")
            self.list_stats_label.configure(text=msg, text_color=p["subtext"])
            self._set_list_textbox_content(msg)
            return

        if total_in_tab == 0:
            self.list_stats_label.configure(
                text=self._tr(stats_key, shown=0, total=0),
                text_color=p["subtext"],
            )
            self._set_list_textbox_content(self._tr("list_tab_empty"))
            return

        query = self.list_search_entry.get().strip().lower() if hasattr(self, "list_search_entry") else ""
        if query:
            filtered = [item for item in subtab_entries if query in item[2]]
        else:
            filtered = subtab_entries

        self.list_stats_label.configure(
            text=self._tr(stats_key, shown=len(filtered), total=total_in_tab),
            text_color=p["subtext"],
        )

        if not filtered:
            self._set_list_textbox_content(self._tr("list_no_matches", query=query))
            return

        tag = f"[{self._tr('list_tag_domain') if is_domain_tab else self._tr('list_tag_ip')}]"
        lines = [f"{tag:<8} {value}" for _, value, _, _ in filtered]
        self._set_list_textbox_content("\n".join(lines))

    def _load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
            except Exception:
                pass
        return {}

    def _save_config(self):
        data = {
            "theme": "Dark",
            "lang": self.current_lang,
            "zapret_dir": self.zapret_dir,
            "zapret_profiles": self.zapret_profiles,
            "run_mode": self.run_mode,
            "autostart_strategy": self.autostart_strategy,
            "autostart_run_mode": self.autostart_run_mode,
            "palette": self.palette_colors,
        }
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _setup_ui(self):
        # --- Левая боковая панель навигации (в стиле Happ) ---
        self.sidebar = ctk.CTkFrame(self, width=196, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.brand_label = ctk.CTkLabel(
            self.sidebar,
            text="Zapret+",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
        )
        self.brand_label.pack(anchor="w", padx=22, pady=(26, 24))

        self.nav_strategies_btn = ctk.CTkButton(
            self.sidebar,
            text="",
            height=42,
            corner_radius=16,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=lambda: self._switch_tab("strategies"),
        )
        self.nav_strategies_btn.pack(fill="x", padx=12, pady=4)

        self.nav_list_btn = ctk.CTkButton(
            self.sidebar,
            text="",
            height=42,
            corner_radius=16,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=lambda: self._switch_tab("list"),
        )
        self.nav_list_btn.pack(fill="x", padx=12, pady=4)

        self.nav_settings_btn = ctk.CTkButton(
            self.sidebar,
            text="",
            height=42,
            corner_radius=16,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=lambda: self._switch_tab("settings"),
        )
        self.nav_settings_btn.pack(fill="x", padx=12, pady=4)

        self.nav_logs_btn = ctk.CTkButton(
            self.sidebar,
            text="",
            height=42,
            corner_radius=16,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=lambda: self._switch_tab("logs"),
        )
        self.nav_logs_btn.pack(fill="x", padx=12, pady=4)

        # Кнопка "О проекте" в самом низу боковой панели
        self.nav_about_btn = ctk.CTkButton(
            self.sidebar,
            text="",
            height=42,
            corner_radius=16,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=lambda: self._switch_tab("about"),
        )
        self.nav_about_btn.pack(side="bottom", fill="x", padx=12, pady=(4, 20))

        # --- Правая основная область ---
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.pack(side="right", fill="both", expand=True)

        # Верхняя шапка с заголовком страницы и быстрым выбором папки zapret (только имя папки)
        self.top_header = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.top_header.pack(fill="x", padx=24, pady=(20, 4))

        self.header_titles_box = ctk.CTkFrame(self.top_header, fg_color="transparent")
        self.header_titles_box.pack(side="left", fill="x", expand=True)

        self.page_title = ctk.CTkLabel(
            self.header_titles_box,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
        )
        self.page_title.pack(anchor="w")

        self.page_subtitle = ctk.CTkLabel(
            self.header_titles_box,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=13),
        )
        self.page_subtitle.pack(anchor="w", pady=(2, 0))

        self.top_zapret_var = tk.StringVar(value="")
        self.top_zapret_menu = ctk.CTkOptionMenu(
            self.top_header,
            variable=self.top_zapret_var,
            values=[""],
            width=210,
            height=34,
            corner_radius=16,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self._on_top_zapret_selected,
        )
        self.top_zapret_menu.pack(side="right", anchor="n", padx=(12, 0), pady=(4, 0))

        self.header_spacer = ctk.CTkFrame(self.main_area, height=10, fg_color="transparent")
        self.header_spacer.pack(fill="x")

        # --- Вкладка 1: Стратегии ---
        self.strategies_view = ctk.CTkFrame(self.main_area, fg_color="transparent")

        self.status_card = ctk.CTkFrame(self.strategies_view, corner_radius=24)
        self.status_card.pack(fill="x", padx=20, pady=(0, 8))

        self.status_label = ctk.CTkLabel(
            self.status_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
        )
        self.status_label.pack(side="left", padx=20, pady=14)

        self.stop_btn = ctk.CTkButton(
            self.status_card,
            text="",
            width=114,
            height=36,
            corner_radius=18,
            state="disabled",
            font=ctk.CTkFont(weight="bold", size=13),
            command=self.stop_strategy,
        )
        self.stop_btn.pack(side="right", padx=16, pady=12)

        self.section_label = ctk.CTkLabel(
            self.strategies_view,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
        )
        self.section_label.pack(anchor="w", padx=24, pady=(12, 6))

        self.scroll_frame = ctk.CTkScrollableFrame(
            self.strategies_view,
            corner_radius=20,
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # --- Вкладка 2: Лист ---
        self.list_view = ctk.CTkFrame(self.main_area, fg_color="transparent")

        self.list_search_card = ctk.CTkFrame(self.list_view, corner_radius=20)
        self.list_search_card.pack(fill="x", padx=20, pady=(0, 8))

        self.list_subtabs_row = ctk.CTkFrame(self.list_search_card, fg_color="transparent")
        self.list_subtabs_row.pack(fill="x", padx=12, pady=(12, 6))

        self.list_domains_tab_btn = ctk.CTkButton(
            self.list_subtabs_row,
            text="",
            height=34,
            corner_radius=17,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=lambda: self._switch_list_subtab("domain"),
        )
        self.list_domains_tab_btn.pack(side="left", padx=(4, 6))

        self.list_ips_tab_btn = ctk.CTkButton(
            self.list_subtabs_row,
            text="",
            height=34,
            corner_radius=17,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=lambda: self._switch_list_subtab("ip"),
        )
        self.list_ips_tab_btn.pack(side="left", padx=(0, 6))

        self.list_refresh_btn = ctk.CTkButton(
            self.list_subtabs_row,
            text="",
            width=106,
            height=34,
            corner_radius=17,
            font=ctk.CTkFont(weight="bold", size=12),
            command=self.load_lists_data,
        )
        self.list_refresh_btn.pack(side="right", padx=(0, 4))

        self.list_search_row = ctk.CTkFrame(self.list_search_card, fg_color="transparent")
        self.list_search_row.pack(fill="x", padx=12, pady=(2, 6))

        self.list_search_entry = ctk.CTkEntry(
            self.list_search_row,
            placeholder_text="",
            border_width=0,
            corner_radius=14,
            height=36,
            font=ctk.CTkFont(size=13),
        )
        self.list_search_entry.pack(fill="x", expand=True, padx=4)
        self.list_search_entry.bind("<KeyRelease>", self._schedule_list_filter)

        self.list_stats_label = ctk.CTkLabel(
            self.list_search_card,
            text="",
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=12),
        )
        self.list_stats_label.pack(fill="x", padx=16, pady=(0, 10))

        self.list_content_card = ctk.CTkFrame(self.list_view, corner_radius=22)
        self.list_content_card.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        self.list_textbox = ctk.CTkTextbox(
            self.list_content_card,
            border_width=0,
            corner_radius=16,
            wrap="none",
            font=ctk.CTkFont(family="Consolas", size=12),
            state="disabled",
        )
        self.list_textbox.pack(fill="both", expand=True, padx=12, pady=12)

        # --- Вкладка 3: Настройки ---
        self.settings_view = ctk.CTkScrollableFrame(
            self.main_area,
            fg_color="transparent",
            corner_radius=20,
        )

        # Карточка сборок и переключения версий zapret
        self.path_card = ctk.CTkFrame(self.settings_view, corner_radius=22)
        self.path_card.pack(fill="x", padx=20, pady=(0, 10))

        self.settings_path_title = ctk.CTkLabel(
            self.path_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
        )
        self.settings_path_title.pack(anchor="w", padx=20, pady=(16, 2))

        self.settings_path_desc = ctk.CTkLabel(
            self.path_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
        )
        self.settings_path_desc.pack(anchor="w", padx=20, pady=(0, 10))

        self.zapret_name_row = ctk.CTkFrame(self.path_card, fg_color="transparent")
        self.zapret_name_row.pack(fill="x", padx=14, pady=(0, 8))

        self.zapret_name_entry = ctk.CTkEntry(
            self.zapret_name_row,
            placeholder_text="",
            border_width=0,
            corner_radius=14,
            height=34,
            font=ctk.CTkFont(size=12),
        )
        self.zapret_name_entry.pack(side="left", fill="x", expand=True, padx=(4, 8))

        self.add_zapret_btn = ctk.CTkButton(
            self.zapret_name_row,
            text="",
            width=108,
            height=34,
            corner_radius=17,
            font=ctk.CTkFont(weight="bold", size=12),
            command=self.add_zapret_profile,
        )
        self.add_zapret_btn.pack(side="right", padx=(0, 4))

        self.path_input_row = ctk.CTkFrame(self.path_card, fg_color="transparent")
        self.path_input_row.pack(fill="x", padx=14, pady=(0, 10))

        self.path_entry = ctk.CTkEntry(
            self.path_input_row,
            placeholder_text="",
            border_width=0,
            corner_radius=14,
            height=36,
            font=ctk.CTkFont(size=13),
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(4, 8))
        self.path_entry.bind("<Return>", lambda _e: self.add_zapret_profile())

        self.browse_btn = ctk.CTkButton(
            self.path_input_row,
            text="",
            width=92,
            height=36,
            corner_radius=18,
            font=ctk.CTkFont(weight="bold", size=13),
            command=self.browse_folder,
        )
        self.browse_btn.pack(side="right", padx=(0, 4))

        self.zapret_profiles_box = ctk.CTkFrame(self.path_card, fg_color="transparent")
        self.zapret_profiles_box.pack(fill="x", padx=16, pady=(0, 12))

        # Карточка режима работы zapret при запуске из утилиты (В фоне / Окно)
        self.run_mode_card = ctk.CTkFrame(self.settings_view, corner_radius=22)
        self.run_mode_card.pack(fill="x", padx=20, pady=6)

        self.run_mode_row = ctk.CTkFrame(self.run_mode_card, fg_color="transparent")
        self.run_mode_row.pack(fill="x", padx=20, pady=(16, 6))

        self.run_mode_text_box = ctk.CTkFrame(self.run_mode_row, fg_color="transparent")
        self.run_mode_text_box.pack(side="left", fill="x", expand=True)

        self.settings_run_mode_title = ctk.CTkLabel(
            self.run_mode_text_box,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
        )
        self.settings_run_mode_title.pack(anchor="w")

        self.settings_run_mode_desc = ctk.CTkLabel(
            self.run_mode_text_box,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
        )
        self.settings_run_mode_desc.pack(anchor="w", pady=(2, 0))

        self.run_mode_btns_box = ctk.CTkFrame(self.run_mode_row, fg_color="transparent")
        self.run_mode_btns_box.pack(side="right", padx=(12, 0))

        self.run_mode_bg_btn = ctk.CTkButton(
            self.run_mode_btns_box,
            text="",
            width=102,
            height=36,
            corner_radius=18,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=lambda: self.set_run_mode("background"),
        )
        self.run_mode_bg_btn.pack(side="left", padx=(0, 6))

        self.run_mode_win_btn = ctk.CTkButton(
            self.run_mode_btns_box,
            text="",
            width=92,
            height=36,
            corner_radius=18,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=lambda: self.set_run_mode("window"),
        )
        self.run_mode_win_btn.pack(side="left")

        self.current_run_mode_label = ctk.CTkLabel(
            self.run_mode_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            anchor="w",
        )
        self.current_run_mode_label.pack(fill="x", padx=20, pady=(0, 14))

        # Карточка автозагрузки стратегии (отдельные стратегия и режим для автозапуска)
        self.autostart_card = ctk.CTkFrame(self.settings_view, corner_radius=22)
        self.autostart_card.pack(fill="x", padx=20, pady=6)

        self.autostart_row = ctk.CTkFrame(self.autostart_card, fg_color="transparent")
        self.autostart_row.pack(fill="x", padx=20, pady=(16, 8))

        self.autostart_text_box = ctk.CTkFrame(self.autostart_row, fg_color="transparent")
        self.autostart_text_box.pack(side="left", fill="x", expand=True)

        self.settings_autostart_title = ctk.CTkLabel(
            self.autostart_text_box,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
        )
        self.settings_autostart_title.pack(anchor="w")

        self.settings_autostart_desc = ctk.CTkLabel(
            self.autostart_text_box,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
        )
        self.settings_autostart_desc.pack(anchor="w", pady=(2, 0))

        self.autostart_toggle_btn = ctk.CTkButton(
            self.autostart_row,
            text="",
            width=144,
            height=36,
            corner_radius=18,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=self.toggle_autostart,
        )
        self.autostart_toggle_btn.pack(side="right", padx=(12, 0))

        # Отдельный выбор стратегии для автозапуска
        self.autostart_strategy_row = ctk.CTkFrame(self.autostart_card, fg_color="transparent")
        self.autostart_strategy_row.pack(fill="x", padx=20, pady=(2, 8))

        self.autostart_strategy_lbl = ctk.CTkLabel(
            self.autostart_strategy_row,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        )
        self.autostart_strategy_lbl.pack(side="left")

        self.autostart_strategy_var = tk.StringVar(value="")
        self.autostart_strategy_menu = ctk.CTkOptionMenu(
            self.autostart_strategy_row,
            variable=self.autostart_strategy_var,
            values=[""],
            width=300,
            height=34,
            corner_radius=16,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            command=self._on_autostart_strategy_selected,
        )
        self.autostart_strategy_menu.pack(side="right")

        # Отдельный выбор режима (В фоне / Окно) именно для автозапуска
        self.autostart_mode_row = ctk.CTkFrame(self.autostart_card, fg_color="transparent")
        self.autostart_mode_row.pack(fill="x", padx=20, pady=(2, 10))

        self.autostart_mode_lbl = ctk.CTkLabel(
            self.autostart_mode_row,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        )
        self.autostart_mode_lbl.pack(side="left")

        self.autostart_mode_btns_box = ctk.CTkFrame(self.autostart_mode_row, fg_color="transparent")
        self.autostart_mode_btns_box.pack(side="right")

        self.autostart_bg_btn = ctk.CTkButton(
            self.autostart_mode_btns_box,
            text="",
            width=102,
            height=32,
            corner_radius=16,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=lambda: self.set_autostart_run_mode("background"),
        )
        self.autostart_bg_btn.pack(side="left", padx=(0, 6))

        self.autostart_win_btn = ctk.CTkButton(
            self.autostart_mode_btns_box,
            text="",
            width=92,
            height=32,
            corner_radius=16,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=lambda: self.set_autostart_run_mode("window"),
        )
        self.autostart_win_btn.pack(side="left")

        self.autostart_bottom_row = ctk.CTkFrame(self.autostart_card, fg_color="transparent")
        self.autostart_bottom_row.pack(fill="x", padx=20, pady=(0, 14))

        self.current_autostart_label = ctk.CTkLabel(
            self.autostart_bottom_row,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            anchor="w",
        )
        self.current_autostart_label.pack(side="left")

        self.open_startup_folder_btn = ctk.CTkButton(
            self.autostart_bottom_row,
            text="",
            height=30,
            corner_radius=15,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self.open_startup_folder,
        )
        self.open_startup_folder_btn.pack(side="right")

        # Карточка папки данных ZapretPlus
        self.data_folder_card = ctk.CTkFrame(self.settings_view, corner_radius=22)
        self.data_folder_card.pack(fill="x", padx=20, pady=6)

        self.data_top_row = ctk.CTkFrame(self.data_folder_card, fg_color="transparent")
        self.data_top_row.pack(fill="x", padx=20, pady=(16, 6))

        self.data_text_box = ctk.CTkFrame(self.data_top_row, fg_color="transparent")
        self.data_text_box.pack(side="left", fill="x", expand=True)

        self.settings_data_title = ctk.CTkLabel(
            self.data_text_box,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
        )
        self.settings_data_title.pack(anchor="w")

        self.settings_data_desc = ctk.CTkLabel(
            self.data_text_box,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
        )
        self.settings_data_desc.pack(anchor="w", pady=(2, 0))

        self.open_data_btn = ctk.CTkButton(
            self.data_top_row,
            text="",
            width=136,
            height=36,
            corner_radius=18,
            font=ctk.CTkFont(weight="bold", size=13),
            command=self.open_data_folder,
        )
        self.open_data_btn.pack(side="right", padx=(12, 0))

        self.data_path_label = ctk.CTkLabel(
            self.data_folder_card,
            text=self.app_data_dir,
            font=ctk.CTkFont(family="Consolas", size=12),
            anchor="w",
        )
        self.data_path_label.pack(fill="x", padx=20, pady=(0, 16))

        # Карточка полноценной палитры цветов каждого аспекта интерфейса
        self.palette_card = ctk.CTkFrame(self.settings_view, corner_radius=22)
        self.palette_card.pack(fill="x", padx=20, pady=6)

        self.palette_header_row = ctk.CTkFrame(self.palette_card, fg_color="transparent")
        self.palette_header_row.pack(fill="x", padx=20, pady=(16, 8))

        self.palette_title_box = ctk.CTkFrame(self.palette_header_row, fg_color="transparent")
        self.palette_title_box.pack(side="left", fill="x", expand=True)

        self.settings_palette_title = ctk.CTkLabel(
            self.palette_title_box,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
        )
        self.settings_palette_title.pack(anchor="w")

        self.settings_palette_desc = ctk.CTkLabel(
            self.palette_title_box,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
        )
        self.settings_palette_desc.pack(anchor="w", pady=(2, 0))

        self.reset_palette_btn = ctk.CTkButton(
            self.palette_header_row,
            text="",
            width=144,
            height=34,
            corner_radius=17,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self.reset_palette_colors,
        )
        self.reset_palette_btn.pack(side="right", padx=(12, 0))

        for idx, aspect_key in enumerate(COLOR_ASPECT_ORDER):
            bottom_pad = 16 if idx == len(COLOR_ASPECT_ORDER) - 1 else 6
            row = ctk.CTkFrame(self.palette_card, corner_radius=14)
            row.pack(fill="x", padx=16, pady=(0, bottom_pad))

            lbl = ctk.CTkLabel(
                row,
                text="",
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                anchor="w",
            )
            lbl.pack(side="left", padx=(14, 10), pady=8)

            apply_btn = ctk.CTkButton(
                row,
                text="",
                width=92,
                height=30,
                corner_radius=15,
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                command=lambda k=aspect_key: self._apply_entry_color_for_aspect(k),
            )
            apply_btn.pack(side="right", padx=(6, 10), pady=8)

            pick_btn = ctk.CTkButton(
                row,
                text="",
                width=74,
                height=30,
                corner_radius=15,
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                command=lambda k=aspect_key: self._pick_color_for_aspect(k),
            )
            pick_btn.pack(side="right", padx=(6, 0), pady=8)

            entry = ctk.CTkEntry(
                row,
                width=102,
                height=30,
                border_width=0,
                corner_radius=12,
                font=ctk.CTkFont(family="Consolas", size=12),
            )
            entry.pack(side="right", padx=(8, 0), pady=8)
            entry.bind("<Return>", lambda _e, k=aspect_key: self._apply_entry_color_for_aspect(k))

            swatch = ctk.CTkFrame(
                row,
                width=24,
                height=24,
                corner_radius=8,
            )
            swatch.pack(side="right", pady=8)
            swatch.pack_propagate(False)

            self.palette_controls[aspect_key] = {
                "row": row,
                "label": lbl,
                "swatch": swatch,
                "entry": entry,
                "pick_btn": pick_btn,
                "apply_btn": apply_btn,
            }

        # Карточка выбора языка (кнопка + текущий язык под ней)
        self.lang_card = ctk.CTkFrame(self.settings_view, corner_radius=22)
        self.lang_card.pack(fill="x", padx=20, pady=(6, 16))

        self.lang_row = ctk.CTkFrame(self.lang_card, fg_color="transparent")
        self.lang_row.pack(fill="x", padx=20, pady=(16, 6))

        self.lang_text_box = ctk.CTkFrame(self.lang_row, fg_color="transparent")
        self.lang_text_box.pack(side="left", fill="x", expand=True)

        self.settings_lang_title = ctk.CTkLabel(
            self.lang_text_box,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
        )
        self.settings_lang_title.pack(anchor="w")

        self.settings_lang_desc = ctk.CTkLabel(
            self.lang_text_box,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
        )
        self.settings_lang_desc.pack(anchor="w", pady=(2, 0))

        self.lang_toggle_btn = ctk.CTkButton(
            self.lang_row,
            text="",
            width=144,
            height=36,
            corner_radius=18,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=self._toggle_language,
        )
        self.lang_toggle_btn.pack(side="right", padx=(12, 0))

        self.current_lang_label = ctk.CTkLabel(
            self.lang_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            anchor="w",
        )
        self.current_lang_label.pack(fill="x", padx=20, pady=(0, 14))

        self._bind_settings_mousewheel_once()

        # --- Вкладка 4: Логи ---
        self.logs_view = ctk.CTkFrame(self.main_area, fg_color="transparent")

        self.logs_toolbar = ctk.CTkFrame(self.logs_view, fg_color="transparent")
        self.logs_toolbar.pack(fill="x", padx=20, pady=(0, 10))

        self.clear_logs_btn = ctk.CTkButton(
            self.logs_toolbar,
            text="",
            width=140,
            height=36,
            corner_radius=18,
            font=ctk.CTkFont(weight="bold", size=13),
            command=self.clear_logs,
        )
        self.clear_logs_btn.pack(side="right")

        self.logs_card = ctk.CTkFrame(self.logs_view, corner_radius=22)
        self.logs_card.pack(fill="both", expand=True, padx=20, pady=(0, 18))

        self.logs_textbox = ctk.CTkTextbox(
            self.logs_card,
            border_width=0,
            corner_radius=16,
            font=ctk.CTkFont(family="Consolas", size=12),
            state="disabled",
        )
        self.logs_textbox.pack(fill="both", expand=True, padx=12, pady=12)

        # --- Вкладка 5: О проекте ---
        self.about_view = ctk.CTkFrame(self.main_area, fg_color="transparent")

        self.about_card = ctk.CTkFrame(self.about_view, corner_radius=24)
        self.about_card.pack(fill="x", padx=20, pady=(0, 14))

        self.about_title_lbl = ctk.CTkLabel(
            self.about_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            anchor="w",
        )
        self.about_title_lbl.pack(fill="x", padx=22, pady=(20, 4))

        self.about_desc_lbl = ctk.CTkLabel(
            self.about_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            anchor="w",
            justify="left",
        )
        self.about_desc_lbl.pack(fill="x", padx=22, pady=(0, 16))

        # Строка: язык разработки
        self.about_lang_row = ctk.CTkFrame(self.about_card, fg_color="transparent")
        self.about_lang_row.pack(fill="x", padx=22, pady=4)
        self.about_lang_key = ctk.CTkLabel(
            self.about_lang_row,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=13),
        )
        self.about_lang_key.pack(side="left")
        self.about_lang_val = ctk.CTkLabel(
            self.about_lang_row,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        )
        self.about_lang_val.pack(side="right")

        # Строка: ИИ
        self.about_ai_row = ctk.CTkFrame(self.about_card, fg_color="transparent")
        self.about_ai_row.pack(fill="x", padx=22, pady=4)
        self.about_ai_key = ctk.CTkLabel(
            self.about_ai_row,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=13),
        )
        self.about_ai_key.pack(side="left")
        self.about_ai_val = ctk.CTkLabel(
            self.about_ai_row,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        )
        self.about_ai_val.pack(side="right")

        # Строка: ник автора
        self.about_author_row = ctk.CTkFrame(self.about_card, fg_color="transparent")
        self.about_author_row.pack(fill="x", padx=22, pady=4)
        self.about_author_key = ctk.CTkLabel(
            self.about_author_row,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=13),
        )
        self.about_author_key.pack(side="left")
        self.about_author_val = ctk.CTkLabel(
            self.about_author_row,
            text=AUTHOR_NICKNAME,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        )
        self.about_author_val.pack(side="right")

        # Строка: GitHub профиль + кнопка открытия
        self.about_gh_row = ctk.CTkFrame(self.about_card, fg_color="transparent")
        self.about_gh_row.pack(fill="x", padx=22, pady=(8, 6))
        self.about_gh_key = ctk.CTkLabel(
            self.about_gh_row,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=13),
        )
        self.about_gh_key.pack(side="left")

        self.open_github_btn = ctk.CTkButton(
            self.about_gh_row,
            text="",
            width=144,
            height=34,
            corner_radius=17,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self.open_github_profile,
        )
        self.open_github_btn.pack(side="right")

        self.about_gh_url_lbl = ctk.CTkLabel(
            self.about_gh_row,
            text=GITHUB_PROFILE_URL,
            font=ctk.CTkFont(family="Consolas", size=12),
        )
        self.about_gh_url_lbl.pack(side="right", padx=(0, 12))

        # Строка: YouTube канал + кнопка открытия
        self.about_yt_row = ctk.CTkFrame(self.about_card, fg_color="transparent")
        self.about_yt_row.pack(fill="x", padx=22, pady=(6, 22))
        self.about_yt_key = ctk.CTkLabel(
            self.about_yt_row,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=13),
        )
        self.about_yt_key.pack(side="left")

        self.open_youtube_btn = ctk.CTkButton(
            self.about_yt_row,
            text="",
            width=144,
            height=34,
            corner_radius=17,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self.open_youtube_channel,
        )
        self.open_youtube_btn.pack(side="right")

        yt_display = YOUTUBE_CHANNEL_URL.strip() or YOUTUBE_CHANNEL_LABEL
        self.about_yt_url_lbl = ctk.CTkLabel(
            self.about_yt_row,
            text=yt_display,
            font=ctk.CTkFont(family="Consolas", size=12),
        )
        self.about_yt_url_lbl.pack(side="right", padx=(0, 12))

    def _switch_tab(self, tab_name, apply_only=False):
        self.active_tab = tab_name
        self.strategies_view.pack_forget()
        self.list_view.pack_forget()
        self.settings_view.pack_forget()
        self.logs_view.pack_forget()
        self.about_view.pack_forget()

        if tab_name == "strategies":
            self.strategies_view.pack(fill="both", expand=True)
            self.load_strategies()
        elif tab_name == "list":
            self.list_view.pack(fill="both", expand=True)
            self.load_lists_data()
        elif tab_name == "settings":
            self.settings_view.pack(fill="both", expand=True, padx=4, pady=(0, 8))
            self.refresh_autostart_strategy_options()
            self._render_zapret_profiles()
            self._bind_settings_mousewheel_once()
        elif tab_name == "logs":
            self.logs_view.pack(fill="both", expand=True)
            self.refresh_logs()
        else:
            self.about_view.pack(fill="both", expand=True)

        if not apply_only:
            self._apply_theme()

    def _toggle_language(self):
        self.current_lang = "en" if self.current_lang == "ru" else "ru"
        self._save_config()
        lang_label = self._tr("lang_name_ru") if self.current_lang == "ru" else self._tr("lang_name_en")
        self._write_log(self._tr("log_lang_changed", lang=lang_label))
        self._apply_theme()
        if self.active_tab == "strategies":
            self.load_strategies()
        elif self.active_tab == "list":
            self.render_list_results()
        elif self.active_tab == "logs":
            self.refresh_logs()

    def _apply_theme(self):
        p = self._palette()

        self.configure(fg_color=p["bg"])
        self.sidebar.configure(fg_color=p["sidebar"])
        self.brand_label.configure(text_color=p["accent"])

        # Навигационные кнопки в стиле Happ
        self.nav_strategies_btn.configure(text=f"  ⚡  {self._tr('nav_strategies')}")
        self.nav_list_btn.configure(text=f"  📋  {self._tr('nav_list')}")
        self.nav_settings_btn.configure(text=f"  ⚙  {self._tr('nav_settings')}")
        self.nav_logs_btn.configure(text=f"  📜  {self._tr('nav_logs')}")
        self.nav_about_btn.configure(text=f"  ℹ  {self._tr('nav_about')}")

        self.nav_strategies_btn.configure(fg_color="transparent", text_color=p["subtext"])
        self.nav_list_btn.configure(fg_color="transparent", text_color=p["subtext"])
        self.nav_settings_btn.configure(fg_color="transparent", text_color=p["subtext"])
        self.nav_logs_btn.configure(fg_color="transparent", text_color=p["subtext"])
        self.nav_about_btn.configure(fg_color="transparent", text_color=p["subtext"])

        if self.active_tab == "strategies":
            self.nav_strategies_btn.configure(fg_color=p["nav_active"], text_color=p["accent"])
            self.page_title.configure(text=self._tr("nav_strategies"))
            self.page_subtitle.configure(text=self._tr("subtitle_strategies"))
        elif self.active_tab == "list":
            self.nav_list_btn.configure(fg_color=p["nav_active"], text_color=p["accent"])
            self.page_title.configure(text=self._tr("nav_list"))
            self.page_subtitle.configure(text=self._tr("subtitle_list"))
        elif self.active_tab == "settings":
            self.nav_settings_btn.configure(fg_color=p["nav_active"], text_color=p["accent"])
            self.page_title.configure(text=self._tr("nav_settings"))
            self.page_subtitle.configure(text=self._tr("subtitle_settings"))
        elif self.active_tab == "logs":
            self.nav_logs_btn.configure(fg_color=p["nav_active"], text_color=p["accent"])
            self.page_title.configure(text=self._tr("nav_logs"))
            self.page_subtitle.configure(text=self._tr("subtitle_logs"))
        else:
            self.nav_about_btn.configure(fg_color=p["nav_active"], text_color=p["accent"])
            self.page_title.configure(text=self._tr("nav_about"))
            self.page_subtitle.configure(text=self._tr("subtitle_about"))

        self.page_title.configure(text_color=p["text"])
        self.page_subtitle.configure(text_color=p["subtext"])
        self.refresh_top_zapret_selector()
        self.top_zapret_menu.configure(
            fg_color=p["toggle_bg"],
            button_color=p["toggle_bg"],
            button_hover_color=p["seg_unselected"],
            dropdown_fg_color=p["toggle_bg"],
            dropdown_hover_color=p["nav_active"],
            dropdown_text_color=p["text"],
            text_color=p["accent"] if self.zapret_dir else p["subtext"],
        )
        self.section_label.configure(text=self._tr("section_strategies"), text_color=p["text"])

        self.status_card.configure(fg_color=p["card"])
        if self.active_strategy_name:
            self.status_label.configure(
                text=self._tr("status_active", name=self.active_strategy_name),
                text_color=p["accent"],
            )
            self.stop_btn.configure(
                text=self._tr("stop"),
                state="normal",
                fg_color=p["danger"],
                hover_color=p["danger_hover"],
                text_color=p["danger_text"],
            )
        else:
            self.status_label.configure(
                text=self._tr("status_idle"),
                text_color=p["subtext"],
            )
            self.stop_btn.configure(
                text=self._tr("stop"),
                state="disabled",
                fg_color=p["disabled_bg"],
                text_color=p["disabled_text"],
            )

        self.scroll_frame.configure(
            fg_color=p["bg"],
            scrollbar_button_color=p["card"],
            scrollbar_button_hover_color=p["accent"],
        )
        if hasattr(self.scroll_frame, "_parent_canvas"):
            self.scroll_frame._parent_canvas.configure(bg=p["bg"])

        # Вкладка "Лист"
        self.list_search_card.configure(fg_color=p["card"])
        self.list_domains_tab_btn.configure(text=self._tr("list_tab_domains"))
        self.list_ips_tab_btn.configure(text=self._tr("list_tab_ips"))
        if self.active_list_subtab == "domain":
            self.list_domains_tab_btn.configure(
                fg_color=p["accent"],
                hover_color=p["accent_hover"],
                text_color=p["accent_text"],
            )
            self.list_ips_tab_btn.configure(
                fg_color=p["toggle_bg"],
                hover_color=p["seg_unselected"],
                text_color=p["text"],
            )
            self.list_search_entry.configure(
                placeholder_text=self._tr("list_search_domains_placeholder"),
            )
        else:
            self.list_ips_tab_btn.configure(
                fg_color=p["accent"],
                hover_color=p["accent_hover"],
                text_color=p["accent_text"],
            )
            self.list_domains_tab_btn.configure(
                fg_color=p["toggle_bg"],
                hover_color=p["seg_unselected"],
                text_color=p["text"],
            )
            self.list_search_entry.configure(
                placeholder_text=self._tr("list_search_ips_placeholder"),
            )

        self.list_search_entry.configure(
            fg_color=p["toggle_bg"],
            text_color=p["text"],
            placeholder_text_color=p["subtext"],
        )
        self.list_refresh_btn.configure(
            text=self._tr("list_refresh_btn"),
            fg_color=p["accent"],
            hover_color=p["accent_hover"],
            text_color=p["accent_text"],
        )
        self.list_content_card.configure(fg_color=p["card"])
        self.list_textbox.configure(
            fg_color=p["toggle_bg"],
            text_color=p["text"],
            scrollbar_button_color=p["card"],
            scrollbar_button_hover_color=p["accent"],
        )

        # Вкладка логов
        self.clear_logs_btn.configure(
            text=self._tr("clear_logs"),
            fg_color=p["danger"],
            hover_color=p["danger_hover"],
            text_color=p["danger_text"],
        )
        self.logs_card.configure(fg_color=p["card"])
        self.logs_textbox.configure(
            fg_color=p["toggle_bg"],
            text_color=p["text"],
            scrollbar_button_color=p["card"],
            scrollbar_button_hover_color=p["accent"],
        )

        # Вкладка настроек
        self.settings_view.configure(
            fg_color=p["bg"],
            scrollbar_button_color=p["card"],
            scrollbar_button_hover_color=p["accent"],
        )
        if hasattr(self.settings_view, "_parent_canvas"):
            self.settings_view._parent_canvas.configure(bg=p["bg"])

        self.path_card.configure(fg_color=p["card"])
        self.settings_path_title.configure(text=self._tr("settings_path_title"), text_color=p["text"])
        self.settings_path_desc.configure(text=self._tr("settings_path_desc"), text_color=p["subtext"])
        self.zapret_name_entry.configure(
            fg_color=p["toggle_bg"],
            placeholder_text=self._tr("zapret_name_placeholder"),
            text_color=p["text"],
            placeholder_text_color=p["subtext"],
        )
        self.add_zapret_btn.configure(
            text=self._tr("add_zapret_btn"),
            fg_color=p["accent"],
            hover_color=p["accent_hover"],
            text_color=p["accent_text"],
        )
        self.path_entry.configure(
            fg_color=p["toggle_bg"],
            placeholder_text=self._tr("path_placeholder"),
            text_color=p["text"],
            placeholder_text_color=p["subtext"],
        )
        self.browse_btn.configure(
            text=self._tr("browse"),
            fg_color=p["toggle_bg"],
            hover_color=p["seg_unselected"],
            text_color=p["text"],
        )
        self._render_zapret_profiles()

        self.run_mode_card.configure(fg_color=p["card"])
        self.settings_run_mode_title.configure(text=self._tr("settings_run_mode_title"), text_color=p["text"])
        self.settings_run_mode_desc.configure(text=self._tr("settings_run_mode_desc"), text_color=p["subtext"])
        self._apply_run_mode_ui()
        self._apply_autostart_ui()

        self.data_folder_card.configure(fg_color=p["card"])
        self.settings_data_title.configure(text=self._tr("settings_data_title"), text_color=p["text"])
        self.settings_data_desc.configure(text=self._tr("settings_data_desc"), text_color=p["subtext"])
        self.data_path_label.configure(text=self.app_data_dir, text_color=p["subtext"])
        self.open_data_btn.configure(
            text=self._tr("open_data_folder"),
            fg_color=p["accent"],
            hover_color=p["accent_hover"],
            text_color=p["accent_text"],
        )

        self._apply_palette_editor_ui()

        self.lang_card.configure(fg_color=p["card"])
        self.settings_lang_title.configure(text=self._tr("settings_lang_title"), text_color=p["text"])
        self.settings_lang_desc.configure(text=self._tr("settings_lang_desc"), text_color=p["subtext"])

        self.lang_toggle_btn.configure(
            text=self._tr("switch_lang_btn"),
            fg_color=p["accent"],
            hover_color=p["accent_hover"],
            text_color=p["accent_text"],
        )
        self.current_lang_label.configure(text=self._tr("current_lang_info"), text_color=p["accent"])

        # Вкладка "О проекте"
        self.about_card.configure(fg_color=p["card"])
        self.about_title_lbl.configure(text=self._tr("about_card_title"), text_color=p["text"])
        self.about_desc_lbl.configure(text=self._tr("about_card_desc"), text_color=p["subtext"])
        self.about_lang_key.configure(text=self._tr("about_lang_label"), text_color=p["subtext"])
        self.about_lang_val.configure(text=self._tr("about_lang_value"), text_color=p["text"])
        self.about_ai_key.configure(text=self._tr("about_ai_label"), text_color=p["subtext"])
        self.about_ai_val.configure(text=self._tr("about_ai_value"), text_color=p["accent"])
        self.about_author_key.configure(text=self._tr("about_author_label"), text_color=p["subtext"])
        self.about_author_val.configure(text=AUTHOR_NICKNAME, text_color=p["text"])
        self.about_gh_key.configure(text=self._tr("about_github_label"), text_color=p["subtext"])
        self.about_gh_url_lbl.configure(text=GITHUB_PROFILE_URL, text_color=p["accent"])
        self.open_github_btn.configure(
            text=self._tr("open_github_btn"),
            fg_color=p["accent"],
            hover_color=p["accent_hover"],
            text_color=p["accent_text"],
        )
        self.about_yt_key.configure(text=self._tr("about_youtube_label"), text_color=p["subtext"])
        has_yt = bool(YOUTUBE_CHANNEL_URL.strip())
        self.about_yt_url_lbl.configure(
            text=YOUTUBE_CHANNEL_URL.strip() if has_yt else YOUTUBE_CHANNEL_LABEL,
            text_color=p["accent"] if has_yt else p["subtext"],
        )
        self.open_youtube_btn.configure(
            text=self._tr("open_youtube_btn"),
            state="normal" if has_yt else "disabled",
            fg_color=p["accent"] if has_yt else p["disabled_bg"],
            hover_color=p["accent_hover"] if has_yt else p["disabled_bg"],
            text_color=p["accent_text"] if has_yt else p["disabled_text"],
        )

    def browse_folder(self):
        folder = filedialog.askdirectory(parent=self, title=self._tr("browse_dialog_title"))
        if folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)
            if hasattr(self, "zapret_name_entry") and not self.zapret_name_entry.get().strip():
                self.zapret_name_entry.insert(0, _folder_basename(folder))

    def load_strategies(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        p = self._palette()

        if not self.zapret_dir or not os.path.exists(self.zapret_dir):
            hint_lbl = ctk.CTkLabel(
                self.scroll_frame,
                text=self._tr("no_path_configured"),
                text_color=p["subtext"],
                font=ctk.CTkFont(size=14),
            )
            hint_lbl.pack(pady=30)
            return

        files = self._get_strategy_files()

        if not files:
            empty_lbl = ctk.CTkLabel(
                self.scroll_frame,
                text=self._tr("no_strategies"),
                text_color=p["subtext"],
                font=ctk.CTkFont(size=14),
            )
            empty_lbl.pack(pady=30)
            return

        for file_name in files:
            card = ctk.CTkFrame(
                self.scroll_frame,
                fg_color=p["card"],
                corner_radius=20,
            )
            card.pack(fill="x", padx=6, pady=5)

            name_lbl = ctk.CTkLabel(
                card,
                text=file_name,
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                text_color=p["text"],
            )
            name_lbl.pack(side="left", padx=18, pady=14)

            start_btn = ctk.CTkButton(
                card,
                text=self._tr("start"),
                width=80,
                height=34,
                corner_radius=17,
                fg_color=p["accent"],
                hover_color=p["accent_hover"],
                text_color=p["accent_text"],
                font=ctk.CTkFont(weight="bold", size=12),
                command=lambda f=file_name: self.start_strategy(f),
            )
            start_btn.pack(side="right", padx=14, pady=10)

    def _build_background_bat(self, source_bat_path):
        try:
            with open(source_bat_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception:
            with open(source_bat_path, "r", encoding="cp866", errors="replace") as f:
                content = f.read()

        patched = re.sub(
            r'(?im)^(\s*)start\s+(?:/\w+\s+)*"[^"]*"',
            r'\1start /b ""',
            content,
        )
        patched = re.sub(r'(?im)^\s*pause\s*$', "", patched)

        fd, temp_path = tempfile.mkstemp(prefix=".zapretplus_bg_", suffix=".bat", dir=self.zapret_dir)
        os.close(fd)
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(patched)
        return temp_path

    def _cleanup_temp_bg_script(self):
        if self._temp_bg_script and os.path.exists(self._temp_bg_script):
            try:
                os.remove(self._temp_bg_script)
            except Exception:
                pass
        self._temp_bg_script = None

    def start_strategy(self, bat_filename):
        if not self.zapret_dir or not os.path.exists(self.zapret_dir):
            messagebox.showwarning(self._tr("warn_title"), self._tr("warn_no_path"))
            return

        if self.active_process:
            self.stop_strategy()

        full_path = os.path.join(self.zapret_dir, bat_filename)

        try:
            if os.name == "nt":
                if self.run_mode == "background":
                    bg_script = self._build_background_bat(full_path)
                    self._temp_bg_script = bg_script
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = subprocess.SW_HIDE
                    self.active_process = subprocess.Popen(
                        ["cmd.exe", "/d", "/c", bg_script],
                        cwd=self.zapret_dir,
                        startupinfo=startupinfo,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                    )
                else:
                    self.active_process = subprocess.Popen(
                        ["cmd.exe", "/c", "start", "", "/wait", full_path],
                        cwd=self.zapret_dir,
                        creationflags=subprocess.CREATE_NEW_CONSOLE,
                    )
            else:
                self.active_process = subprocess.Popen(
                    [full_path],
                    cwd=self.zapret_dir,
                    shell=True,
                )

            self.active_strategy_name = bat_filename
            mode_label = self._tr("mode_label_bg") if self.run_mode == "background" else self._tr("mode_label_win")
            self._write_log(self._tr("log_strategy_started", mode=mode_label, name=bat_filename))
            self._apply_theme()
        except Exception as e:
            self._cleanup_temp_bg_script()
            self._write_log(self._tr("log_launch_error", name=bat_filename, error=e))
            messagebox.showerror(self._tr("err_launch_title"), str(e))

    def stop_strategy(self):
        previous_name = self.active_strategy_name
        try:
            subprocess.run(
                "taskkill /F /IM winws.exe",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if self.active_process:
                self.active_process.terminate()
                self.active_process = None
        except Exception:
            pass
        finally:
            self._cleanup_temp_bg_script()

        if previous_name:
            self._write_log(self._tr("log_strategy_stopped", name=previous_name))
        else:
            self._write_log(self._tr("log_stopped_all"))

        self.active_strategy_name = None
        self._apply_theme()


if __name__ == "__main__":
    app = ZapretPlusApp()
    app.mainloop()