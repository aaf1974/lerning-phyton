"""
Конфигурация приложения через pydantic-settings
================================================
Аналогии C# → Python:
  IConfiguration / appsettings.json  = pydantic-settings + .env
  IOptions<T>                        = Settings класс (синглтон)
  builder.Configuration["key"]       = settings.key (type-safe, validated)
  Environment.GetEnvironmentVariable = os.environ / автоматически в Settings
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Конфигурация приложения.

    pydantic-settings автоматически:
    1. Читает .env файл
    2. Читает переменные окружения
    3. Валидирует типы
    4. Даёт type-safe доступ к настройкам

    C# аналог:
        public class AppSettings {
            public string DatabaseUrl { get; set; }
            public string AppEnv { get; set; } = "development";
            public bool Debug { get; set; } = false;
        }
        // + регистрация через builder.Services.Configure<AppSettings>(...)
    """

    model_config = SettingsConfigDict(
        env_file=".env",          # читать из .env файла
        env_file_encoding="utf-8",
        case_sensitive=False,     # DATABASE_URL == database_url
        extra="ignore",           # игнорировать неизвестные переменные
    )

    # Название и версия
    app_title: str = Field(default="Orders API", description="Название API")
    app_version: str = Field(default="0.1.0", description="Версия API")

    # Среда выполнения
    app_env: str = Field(default="development", description="development | staging | production")
    debug: bool = Field(default=False, description="Debug режим")

    # База данных
    database_url: str = Field(
        default="sqlite+aiosqlite:///./orders.db",
        description="URL подключения к БД (asyncpg или aiosqlite)",
    )
    database_url_test: str = Field(
        default="sqlite+aiosqlite:///./test.db",
        description="URL тестовой БД",
    )

    @property
    def is_production(self) -> bool:
        """
        C# аналог:
            public bool IsProduction => AppEnv == "production";
        """
        return self.app_env.lower() == "production"

    @property
    def is_development(self) -> bool:
        return self.app_env.lower() == "development"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Синглтон настроек через lru_cache.

    C# аналог:
        services.AddSingleton<IOptions<Settings>>(...)

    lru_cache(maxsize=1) кэширует результат — повторные вызовы
    возвращают тот же объект без повторного парсинга .env.

    Использование:
        from src.orders.config import get_settings
        settings = get_settings()
        print(settings.app_title)
    """
    return Settings()


# Удобный синглтон для импорта
settings = get_settings()
