from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_db: str = "padg"
    postgres_user: str = "padg_user"
    postgres_password: str = "padg_password"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    @property
    def database_url(self) -> str:
        return (
            f"host={self.postgres_host} port={self.postgres_port} "
            f"dbname={self.postgres_db} user={self.postgres_user} "
            f"password={self.postgres_password}"
        )

settings = Settings()
