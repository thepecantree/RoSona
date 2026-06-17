from rosona.core.config import Config


def main() -> None:
    config = Config.from_env()

    print("=" * 50)
    print("RoSona")
    print(f"Environment: {config.environment}")
    print("=" * 50)


if __name__ == "__main__":
    main()